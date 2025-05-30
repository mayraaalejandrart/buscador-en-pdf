from fpdf import FPDF
import os
from datetime import datetime
import fitz  # PyMuPDF

def buscar_por_nit_y_nombre(ruta_txt, pdf_paths, output_dir):
    with open(ruta_txt, "r", encoding="utf-8") as f:
        entradas = [line.strip() for line in f if line.strip()]

    generados = []

    for entrada in entradas:
        partes = entrada.split(",", 1)
        if len(partes) != 2:
            continue
        nit, empresa = partes[0].strip(), partes[1].strip()
        coincidencias = []

        for path_pdf in pdf_paths:
            doc = fitz.open(path_pdf)
            for num_pagina, pagina in enumerate(doc, start=1):
                texto = pagina.get_text()
                if nit.lower() in texto.lower() and empresa.lower() in texto.lower():
                    coincidencias.append((os.path.basename(path_pdf), num_pagina))
            doc.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informe de Búsqueda por NIT y Empresa", ln=True, align="C")
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"NIT: {nit}", ln=True)
        pdf.cell(200, 10, txt=f"Empresa: {empresa}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha y hora: {datetime.now()}", ln=True)
        pdf.ln(10)

        if coincidencias:
            pdf.set_text_color(0, 100, 0)
            pdf.multi_cell(0, 10, txt="Coincidencias encontradas:")
            for archivo, pagina in coincidencias:
                pdf.cell(200, 10, txt=f"- {archivo}, página {pagina}", ln=True)
        else:
            pdf.set_text_color(200, 0, 0)
            pdf.cell(200, 10, txt="No se encontraron coincidencias.", ln=True)

        pdf.set_text_color(0, 0, 0)
        nombre_archivo = f"{nit}_{empresa}".replace(" ", "_").replace(",", "")
        salida = os.path.join(output_dir, f"{nombre_archivo}{'*' if coincidencias else ''}.pdf")
        pdf.output(salida)
        generados.append(salida)

    return generados
