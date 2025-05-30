import os
from pathlib import Path
import shutil

def organizar_pdfs(lista_pdfs, ruta_salida, opcion_renombrado='1'):
    """
    Organiza y renombra PDFs.

    lista_pdfs: lista de rutas a archivos PDF (str o Path)
    ruta_salida: carpeta donde se organizarán los PDFs
    opcion_renombrado: '1' conservar nombre original
                       '2' usar mismo nombre para todos (por ahora fijo)
                       '3' (no implementado) nombre diferente para cada archivo
    """
    os.makedirs(ruta_salida, exist_ok=True)

    nombre_global = None
    if opcion_renombrado == '2':
        # Por ejemplo, nombre fijo para todos
        nombre_global = "archivo_unico.pdf"

    for pdf_path in lista_pdfs:
        pdf = Path(pdf_path)
        folder_name = pdf.stem
        folder_path = Path(ruta_salida) / folder_name
        folder_path.mkdir(exist_ok=True)

        if opcion_renombrado == '1':
            new_file_name = pdf.name
        elif opcion_renombrado == '2':
            new_file_name = nombre_global
        elif opcion_renombrado == '3':
            # Aquí podrías implementar lógica para pedir nombres distintos
            # Por ahora dejamos el nombre original
            new_file_name = pdf.name
        else:
            new_file_name = pdf.name

        destino = folder_path / new_file_name

        # Copiar para no perder original
        shutil.copy2(pdf, destino)

    return f"Archivos organizados y renombrados en {len(lista_pdfs)} carpetas."
