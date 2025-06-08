import os
import shutil
import zipfile

def organizar_pdfs(archivos_pdf, carpeta_salida, opcion_nombres="conservar"):
    """
    Organiza PDFs en carpetas y los comprime en un ZIP.

    archivos_pdf: lista de rutas absolutas a PDFs.
    carpeta_salida: ruta donde se guardarán organizados.
    opcion_nombres: "conservar", "nombre_comun" o "nombre_individual" (para futuras mejoras).

    Retorna:
        mensaje (str), ruta_zip (str)
    """

    os.makedirs(carpeta_salida, exist_ok=True)

    for archivo in archivos_pdf:
        nombre_archivo = os.path.basename(archivo)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        carpeta_destino = os.path.join(carpeta_salida, nombre_sin_ext)
        os.makedirs(carpeta_destino, exist_ok=True)

        # Por ahora solo conserva el nombre original
        ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
        shutil.move(archivo, ruta_destino)

    # Crear ZIP con todos los PDFs organizados
    zip_path = os.path.join(carpeta_salida, "organizados.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(carpeta_salida):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, carpeta_salida)
                    zipf.write(file_path, arcname)

    return f"Archivos organizados correctamente en '{carpeta_salida}'.", zip_path
