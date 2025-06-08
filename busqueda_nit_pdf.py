import fitz  # PyMuPDF
import os
import re
from datetime import datetime

def limpiar_nombre_archivo(nombre):
    # Reemplaza caracteres inválidos para nombres de archivo por guion bajo
    nombre_limpio = re.sub(r'[\\/*?:"<>|#]', '_', nombre)
    nombre_limpio = nombre_limpio.strip()
    if not nombre_limpio:
        nombre_limpio = "archivo_sin_nombre"
    return nombre_limpio

def buscar_por_nit_y_nombre(archivo_txt, archivos_pdf, carpeta_resultados="resultados"):
    os.makedirs(carpeta_resultados, exist_ok=True)

    # Leer líneas y extraer (NIT, Nombre)
    if isinstance(archivo_txt, str):
        with open(archivo_txt, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    else:
        lineas = archivo_txt.read().decode("utf-8").splitlines()

    nombres_nits = []
    for linea in lineas:
        partes = [p.strip() for p in linea.split("\t")]
        if len(partes) == 2:
            nit, nombre = partes
            nombres_nits.append((nombre, nit))

    # Extraer texto de cada PDF (guardando con nombre original)
    pdf_textos = {}
    for pdf in archivos_pdf:
        texto_total = ""
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
            for pagina in doc:
                texto_total += pagina.get_text()
        pdf_textos[pdf.name] = texto_total.lower()

    resultados_paths = []
    for nombre, nit in nombres_nits:
        nombre_lower = nombre.lower()
        nit_lower = nit.lower()

        # Buscar coincidencias en textos PDF
        resultados = [
            archivo for archivo, texto in pdf_textos.items()
            if nombre_lower in texto or nit_lower in texto
        ]

        # Crear PDF con resultados
        doc = fitz.open()
        page = doc.new_page()
        x, y = 50, 50
        line_spacing = 16
        rojo = (1, 0, 0)

        page.insert_text((x, y), "Resultados de la búsqueda", fontsize=18, fontname="helv", fill=(0, 0, 0))
        y += 6
        page.draw_line(p1=(x, y), p2=(550, y), color=(0, 0, 0), width=2)
        y += line_spacing

        # Aquí ponemos el nombre y el nit claramente separados, como quieres
        page.insert_text((x, y), "Resumen", fontsize=10, fontname="helv", fill=(0, 0, 0))
        y += line_spacing
        page.insert_text((x, y), f"Nombre de empresa : {nombre}", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        page.insert_text((x, y), f"NIT               : {nit}", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        page.insert_text((x, y), "Se buscó en los documentos:", fontsize=9, fontname="helv", fill=(0, 0, 0))
        y += line_spacing

        # Listar PDFs revisados, pintando en rojo los que dieron resultado
        for archivo in pdf_textos:
            color = rojo if archivo in resultados else (0, 0, 0)
            page.insert_text((x + 20, y), archivo, fontsize=9, fontname="helv", fill=color)
            y += line_spacing

        y += 5
        page.insert_text((x, y), f"Resultados : {len(resultados)} documento(s) con al menos una coincidencia", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        fecha_actual = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p").lower()
        page.insert_text((x, y), f"Se guardó en : {fecha_actual}", fontsize=9, fontname="helv", fill=(0, 0, 0))

        # Nombre del archivo solo con el nombre de la empresa, limpio para evitar errores
        nombre_archivo = limpiar_nombre_archivo(nombre)
        if resultados:
            nombre_archivo += "_coincidencia"

        ruta_salida = os.path.join(carpeta_resultados, f"{nombre_archivo}.pdf")

        doc.save(ruta_salida)
        doc.close()
        resultados_paths.append(ruta_salida)

    return resultados_paths
