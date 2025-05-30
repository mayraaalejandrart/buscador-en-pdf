from pathlib import Path
import shutil

def organizar_pdfs(pdfs_paths, output_dir, opcion, nombre_global=None, nombres_individuales=None):
    """
    Organiza y renombra PDFs según la opción elegida.
    
    Args:
        pdfs_paths (list of str): Lista de rutas a archivos PDF a organizar.
        output_dir (str): Carpeta donde se crearán las subcarpetas y se guardarán los archivos.
        opcion (str): '1', '2' o '3' para seleccionar tipo de renombrado.
        nombre_global (str, opcional): Nombre global para opción '2', sin extensión .pdf.
        nombres_individuales (list of str, opcional): Lista de nombres para opción '3', sin extensión .pdf.
    
    Retorna:
        str: Mensaje resumen o error.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if opcion not in ('1', '2', '3'):
        return "Opción inválida."

    if opcion == '2' and not nombre_global:
        return "Se requiere un nombre global para la opción 2."

    if opcion == '3' and (not nombres_individuales or len(nombres_individuales) != len(pdfs_paths)):
        return "Se requieren nombres individuales para todos los archivos en la opción 3."

    for i, pdf_path in enumerate(pdfs_paths):
        pdf_path = Path(pdf_path)
        # Crear carpeta con el nombre base del archivo PDF
        folder_path = output_dir / pdf_path.stem
        folder_path.mkdir(exist_ok=True)

        # Definir nuevo nombre según opción
        if opcion == '1':
            new_file_name = pdf_path.name
        elif opcion == '2':
            new_file_name = nombre_global
            if not new_file_name.endswith(".pdf"):
                new_file_name += ".pdf"
        elif opcion == '3':
            new_file_name = nombres_individuales[i]
            if not new_file_name.endswith(".pdf"):
                new_file_name += ".pdf"

        destino = folder_path / new_file_name
        # Copiar el PDF al nuevo destino con el nombre definido
        shutil.copy(pdf_path, destino)

    return f"Archivos organizados y renombrados en {len(pdfs_paths)} carpetas."
