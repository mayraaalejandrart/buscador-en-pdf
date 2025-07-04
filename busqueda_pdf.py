import fitz  # PyMuPDF
import os
from datetime import datetime

def buscar_por_nombres(archivo_txt, archivos_pdf_paths, archivos_pdf_nombres, carpeta_resultados="resultados"):
    os.makedirs(carpeta_resultados, exist_ok=True)

    # Leer líneas del TXT
    if isinstance(archivo_txt, str):
        with open(archivo_txt, "r", encoding="utf-8") as f:
            nombres = [line.strip() for line in f if line.strip()]
    else:
        nombres = [line.strip() for line in archivo_txt.read().decode("utf-8").splitlines() if line.strip()]

    # Extraer texto de PDFs usando rutas temporales, claves con nombres originales
    pdf_textos = {}
    for ruta_pdf, nombre_pdf in zip(archivos_pdf_paths, archivos_pdf_nombres):
        texto_total = ""
        with fitz.open(ruta_pdf) as doc:
            for pagina in doc:
                texto_total += pagina.get_text()
        pdf_textos[nombre_pdf] = texto_total.lower()

    resultados_paths = []
    for nombre in nombres:
        nombre_lower = nombre.lower()
        resultados = [archivo for archivo, texto in pdf_textos.items() if nombre_lower in texto]

        # Crear documento de resultado
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
        page.insert_text((x, y), f"Se buscó : {nombre}", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        page.insert_text((x, y), "En documento :", fontsize=9, fontname="helv", fill=(0, 0, 0))
        y += line_spacing

        # Mostrar nombres originales con color rojo si hay coincidencia
        for archivo in pdf_textos:
            color = rojo if archivo in resultados else (0, 0, 0)
            page.insert_text((x + 20, y), archivo, fontsize=9, fontname="helv", fill=color)
            y += line_spacing

        y += 5
        page.insert_text((x, y), f"Resultados : {len(resultados)} documento(s) con {len(resultados)} instancia(s)", fontsize=9, fontname="helv", fill=rojo)
        y += line_spacing
        fecha_actual = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p").lower()
        page.insert_text((x, y), f"Se guardó en : {fecha_actual}", fontsize=9, fontname="helv", fill=(0, 0, 0))

        nombre_archivo = f"{nombre}"
        if resultados:
            nombre_archivo += "_coincidencia"
        ruta_salida = os.path.join(carpeta_resultados, f"{nombre_archivo}.pdf")
        doc.save(ruta_salida)
        doc.close()
        resultados_paths.append(ruta_salida)

    return resultados_paths
