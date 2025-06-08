import fitz  # PyMuPDF
import os
from datetime import datetime

def leer_nits_y_nombres(archivo_txt):
    """
    Lee un archivo .txt con líneas en formato 'NIT<TAB>NOMBRE'
    y devuelve una lista de tuplas (nit, nombre).
    """
    lista_nit_nombre = []
    with open(archivo_txt, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split("\t")
            if len(partes) == 2:
                nit, nombre = partes
                lista_nit_nombre.append((nit.strip(), nombre.strip()))
    return lista_nit_nombre

def buscar_por_nit_y_nombre(archivo_txt, archivos_pdf, carpeta_resultados="resultados"):
    os.makedirs(carpeta_resultados, exist_ok=True)

    # Leer el .txt y obtener lista de (nit, nombre)
    nits_nombres = leer_nits_y_nombres(archivo_txt)

    # Extraer texto de cada PDF y almacenarlo con clave: nombre archivo
    pdf_textos = {}
    for pdf in archivos_pdf:
        pdf.seek(0)  # importante, reinicia puntero del archivo
        texto_total = ""
        try:
            with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
                for pagina in doc:
                    texto_total += pagina.get_text()
            pdf_textos[pdf.name] = texto_total.lower()
        except Exception as e:
            print(f"Error al leer PDF {pdf.name}: {e}")

    resultados_paths = []

    for nit, nombre in nits_nombres:
        nombre_lower = nombre.lower()
        nit_lower = nit.lower()

        # Buscar coincidencias por nombre o NIT en los textos de PDFs
        resultados = [
            archivo for archivo, texto in pdf_textos.items()
            if nombre_lower in texto or nit_lower in texto
        ]

        # Crear nuevo PDF para resumen
        doc = fitz.open()
        page = doc.new_page()
        x, y = 50, 50
        line_spacing = 16
        rojo = (1, 0, 0)

        page.insert_text((x, y), "Resultados de la búsqueda", fontsize=18, fontname="helv", fill=(0, 0, 0))
        y += 6
        page.draw_line(p1=(x, y), p2=(550, y), color=(0, 0, 0), width=2)
        y += line_spacing

        page.insert_text((x, y), "Resumen", fontsize=10, fontname="helv", fill=(0, 0, 0))
        y += line_spacing
        page.insert_text((x, y), f"Nombre de empresa : {nombre}", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        page.insert_text((x, y), f"NIT               : {nit}", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        page.insert_text((x, y), "Se buscó en los documentos:", fontsize=9, fontname="helv", fill=(0, 0, 0))
        y += line_spacing

        for archivo in pdf_textos:
            color = rojo if archivo in resultados else (0, 0, 0)
            page.insert_text((x + 20, y), archivo, fontsize=9, fontname="helv", fill=color)
            y += line_spacing

        y += 5
        page.insert_text((x, y), f"Resultados : {len(resultados)} documento(s) con al menos una coincidencia", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        fecha_actual = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p").lower()
        page.insert_text((x, y), f"Se guardó en : {fecha_actual}", fontsize=9, fontname="helv", fill=(0, 0, 0))

        # Guardar PDF con solo el nombre de la empresa, limpiando caracteres inválidos
        nombre_archivo = nombre.replace("/", "-").replace("\\", "-")
        if resultados:
            nombre_archivo += "_coincidencia"
        ruta_salida = os.path.join(carpeta_resultados, f"{nombre_archivo}.pdf")

        try:
            doc.save(ruta_salida)
            doc.close()
            resultados_paths.append(ruta_salida)
        except Exception as e:
            print(f"Error al guardar PDF {ruta_salida}: {e}")

    return resultados_paths
