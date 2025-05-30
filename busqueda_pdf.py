from fpdf import FPDF
import os

def buscar_por_nombres(archivo_txt, archivos_pdf, output_dir):
    nombres = archivo_txt.read().decode("utf-8").splitlines()
    nombres = [n.strip() for n in nombres if n.strip()]

    resultados = []

    for nombre in nombres:
        nombre_archivo = f"{nombre.replace(' ', '_')}.pdf"
        if not nombre_archivo.endswith(".pdf"):
            nombre_archivo += ".pdf"
        path_salida = os.path.join(output_dir, nombre_archivo)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Resultado de búsqueda para: {nombre}", ln=True)

        coincidencias = []

        for archivo in archivos_pdf:
            contenido = archivo.read().decode("latin-1", errors="ignore")
            archivo.seek(0)
            if nombre.lower() in contenido.lower():
                coincidencias.append(archivo.name)

        for c in coincidencias:
            pdf.cell(200, 10, txt=f"- Coincidencia en: {c}", ln=True)

        if not coincidencias:
            pdf.cell(200, 10, txt="No se encontraron coincidencias.", ln=True)
        else:
            path_salida = path_salida.replace(".pdf", "* .pdf")  # Marca con asterisco

        pdf.output(path_salida)
        resultados.append(path_salida)

    return resultados
