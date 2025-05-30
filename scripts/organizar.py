import os
from pathlib import Path
import shutil

def organizar_pdfs(lista_pdfs, ruta_salida):
    if not lista_pdfs:
        return "No se encontraron archivos para organizar."

    for ruta_pdf in lista_pdfs:
        ruta_pdf = Path(ruta_pdf)
        folder_name = ruta_pdf.stem.replace("*", "").strip()
        folder_path = Path(ruta_salida) / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        nuevo_nombre = ruta_pdf.name.replace("*", "").strip()
        nuevo_path = folder_path / nuevo_nombre

        shutil.copy2(ruta_pdf, nuevo_path)

    return f"Organizados {len(lista_pdfs)} archivos PDF en carpetas."
