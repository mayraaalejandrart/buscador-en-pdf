import os
import shutil
from pathlib import Path
import zipfile
import tempfile

def organizar_pdfs(archivos_pdf, opcion_nombres, nombre_comun=None, nombres_individuales=None):
    """
    Organiza archivos PDF en una carpeta temporal y devuelve la ruta
    del archivo ZIP con todos los PDFs renombrados según la opción seleccionada.

    Parámetros:
    - archivos_pdf: lista de paths (str) a los PDFs en disco.
    - opcion_nombres: str, una de "1", "2", o "3"
        "1" = conservar nombre original
        "2" = usar mismo nombre para todos (nombre_comun debe estar)
        "3" = usar nombres individuales (nombres_individuales debe estar)
    - nombre_comun: str, nombre común para opción "2"
    - nombres_individuales: dict {nombre_archivo_original: nuevo_nombre} para opción "3"

    Retorna:
    - ruta al archivo ZIP con PDFs organizados
    """
    if opcion_nombres not in {"1", "2", "3"}:
        raise ValueError("Opción de nombres inválida")

    with tempfile.TemporaryDirectory() as temp_dir:
        for archivo in archivos_pdf:
            archivo_path = Path(archivo)
            nombre_original = archivo_path.name
            nombre_sin_ext = archivo_path.stem

            if opcion_nombres == "1":
                nuevo_nombre = nombre_original
            elif opcion_nombres == "2":
                if not nombre_comun:
                    raise ValueError("Debe proporcionar un nombre común para la opción 2")
                nuevo_nombre = f"{nombre_comun}.pdf"
            else:  # opcion_nombres == "3"
                if not nombres_individuales or nombre_original not in nombres_individuales:
                    raise ValueError(f"Falta nuevo nombre para {nombre_original} en opción 3")
                nuevo_nombre = f"{nombres_individuales[nombre_original]}.pdf"

            destino = Path(temp_dir) / nuevo_nombre
            shutil.copy2(archivo, destino)

        # Crear ZIP con todo lo organizado
        zip_path = Path(temp_dir) / "organizados.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in Path(temp_dir).glob("*.pdf"):
                zipf.write(file, arcname=file.name)

        # Leer el archivo zip para devolver bytes y que Streamlit pueda usarlo
        with open(zip_path, "rb") as f:
            zip_bytes = f.read()

    return zip_bytes
