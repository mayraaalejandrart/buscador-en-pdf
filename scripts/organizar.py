import os
import shutil
import zipfile
from pathlib import Path

def organizar_pdfs_zip(pdf_paths, opcion_nombres, nombre_comun=None, nombres_individuales=None):
    temp_output_dir = Path("temp_organizados")
    temp_output_dir.mkdir(exist_ok=True)

    for i, pdf_path in enumerate(pdf_paths):
        nombre_original = Path(pdf_path).stem
        carpeta_destino = temp_output_dir / nombre_original
        carpeta_destino.mkdir(exist_ok=True)

        # Nombre del PDF dentro de la carpeta
        if opcion_nombres == "Conservar el nombre original":
            nuevo_nombre = Path(pdf_path).name
        elif opcion_nombres == "Usar el mismo nuevo nombre para todos":
            nuevo_nombre = f"{nombre_comun}.pdf"
        elif opcion_nombres == "Especificar un nombre diferente para cada archivo":
            nuevo_nombre = f"{nombres_individuales[i]}.pdf"
        else:
            raise ValueError("Opción de nombre inválida.")

        destino = carpeta_destino / nuevo_nombre
        shutil.copy2(pdf_path, destino)

    # Crear ZIP con todas las carpetas
    zip_path = Path("organizados.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder, _, files in os.walk(temp_output_dir):
            for file in files:
                file_path = Path(folder) / file
                zipf.write(file_path, arcname=file_path.relative_to(temp_output_dir))

    # Limpiar carpeta temporal
    shutil.rmtree(temp_output_dir)

    return zip_path
