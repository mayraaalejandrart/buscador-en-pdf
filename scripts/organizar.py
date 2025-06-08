import os
import shutil

def organizar_pdfs(pdf_paths, carpeta_destino, opcion_nombres, nombre_comun="resultado"):
    os.makedirs(carpeta_destino, exist_ok=True)

    for ruta_original in pdf_paths:
        archivo = os.path.basename(ruta_original)
        nombre_sin_extension = os.path.splitext(archivo)[0]
        carpeta_subdestino = os.path.join(carpeta_destino, nombre_sin_extension)
        os.makedirs(carpeta_subdestino, exist_ok=True)

        if opcion_nombres == "conservar":
            nuevo_nombre = archivo
        elif opcion_nombres == "mismo":
            if not nombre_comun:
                return "Error: Debes proporcionar un nombre común válido."
            nuevo_nombre = f"{nombre_comun}.pdf"
        elif opcion_nombres == "diferente":
            # Aquí puedes implementar una lógica para pedir nombres individuales
            # Para la demo, usaré el nombre original, pero podrías modificar esto.
            nuevo_nombre = archivo
        else:
            return "Opción de nombre no válida."

        ruta_destino = os.path.join(carpeta_subdestino, nuevo_nombre)
        shutil.move(ruta_original, ruta_destino)

    return f"Archivos organizados correctamente en '{carpeta_destino}'."
