import os
from pathlib import Path

def organizar_pdfs():
    # Obtener la ruta donde está el script
    script_path = Path(__file__).parent.resolve()

    # Cambiar al directorio del script
    os.chdir(script_path)

    # Obtener todos los PDFs de esa carpeta
    pdfs = list(script_path.glob("*.pdf"))

    if not pdfs:
        return "No se encontraron archivos PDF en la carpeta."

    # Opciones de renombrado, simulamos pedir opción (puedes adaptar para Streamlit)
    opcion = input("¿Cómo deseas nombrar los archivos PDF?\n"
                   "1. Conservar el nombre original\n"
                   "2. Usar el mismo nuevo nombre para todos\n"
                   "3. Especificar un nombre diferente para cada archivo\n"
                   "Ingresa 1, 2 o 3: ")

    nombre_global = None

    for pdf in pdfs:
        folder_name = pdf.stem
        folder_path = script_path / folder_name
        folder_path.mkdir(exist_ok=True)

        if opcion == '1':
            new_file_name = pdf.name
        elif opcion == '2':
            if not nombre_global:
                nombre_global = input("Ingresa el nombre que deseas usar para todos los archivos (sin .pdf): ")
                if not nombre_global.endswith(".pdf"):
                    nombre_global += ".pdf"
            new_file_name = nombre_global
        elif opcion == '3':
            nuevo_nombre = input(f"Ingresa el nuevo nombre para '{pdf.name}' (sin .pdf): ")
            if not nuevo_nombre.endswith(".pdf"):
                nuevo_nombre += ".pdf"
            new_file_name = nuevo_nombre
        else:
            return "Opción inválida."

        destino = folder_path / new_file_name
        pdf.rename(destino)

    return f"Archivos organizados y renombrados en {len(pdfs)} carpetas."
