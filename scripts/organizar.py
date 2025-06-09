import os
import shutil
import zipfile
from pathlib import Path
import tempfile

def organizar_pdfs_zip(pdf_paths, opcion_nombres, nombre_comun="", nombres_individuales=None):
    nombres_individuales = nombres_individuales or {}

    salida_temp = tempfile.mkdtemp()
    
    for pdf in pdf_paths:
        nombre_original = Path(pdf).stem
        carpeta_destino = Path(salida_temp) / nombre_original
        carpeta_destino.mkdir(parents=True, exist_ok=True)

        if opcion_nombres == "Conservar el nombre original":
            nuevo_nombre = Path(pdf).name
        elif opcion_nombres == "Usar el mismo nuevo nombre para todos":
            nuevo_nombre = f"{nombre_comun}.pdf"
        elif opcion_nombres == "Especificar un nombre diferente para cada archivo":
            nuevo_nombre = f"{nombres_individuales.get(Path(pdf).name, nombre_original)}.pdf"
        else:
            nuevo_nombre = Path(pdf).name

        shutil.copy2(pdf, carpeta_destino / nuevo_nombre)

    # Crear ZIP con todo
    zip_path = os.path.join(salida_temp, "organizados.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for carpeta, _, archivos in os.walk(salida_temp):
            for archivo in archivos:
                if archivo != "organizados.zip":
                    full_path = os.path.join(carpeta, archivo)
                    relative_path = os.path.relpath(full_path, salida_temp)
                    zipf.write(full_path, relative_path)

    return zip_path
