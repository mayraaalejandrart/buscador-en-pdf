from fpdf import FPDF
import os

def buscar_por_nit_y_nombre(archivo_txt, archivos_pdf, output_dir):
    lineas = archivo_txt.read().decode("utf-8").splitlines()
    lineas = [l.strip() for l in lineas if l.strip() and ";" in l]

    resultados = []

    for linea in lineas:
        nit, nombre_empresa = map(str.strip, linea.split(";"))
        nombre_archivo = f"{nit}_{nombre_empresa.replace(' ', '_')}.pdf"
        if not nombre_archivo.endswith(".pdf"):
            nombre_archivo += ".pdf"
        path_salida = os.path.join(output_dir, nombre_archivo)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"NIT: {nit}", ln=True)
        pdf.cell(200, 10, txt=f"Empresa: {nombre_empresa}", ln=True)

        coincidencias = []

        for archivo in archivos_pdf:
            contenido = archivo.read().decode("latin-1", errors="ignore")
            archivo.seek(0)
            if nit in contenido and nombre_empresa.lower() in contenido.lower():
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
