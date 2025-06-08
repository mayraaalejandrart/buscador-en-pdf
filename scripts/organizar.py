import os
import shutil
import zipfile
import tempfile
from pathlib import Path
import streamlit as st

def organizar_pdfs(pdf_paths, ruta_salida, opcion_nombres, nombres_personalizados=None, nombre_comun=None):
    """
    Organiza PDFs en subcarpetas según nombre base y renombra según opción.

    Args:
        pdf_paths (list): Rutas de PDFs a organizar.
        ruta_salida (str): Carpeta destino.
        opcion_nombres (str): "original", "comun", "personalizado"
        nombres_personalizados (dict): {nombre_original: nuevo_nombre} (solo si opcion="personalizado")
        nombre_comun (str): Nombre común para todos (solo si opcion="comun")

    Returns:
        str: Mensaje de éxito.
        str: Ruta al archivo ZIP generado con PDFs organizados.
    """
    os.makedirs(ruta_salida, exist_ok=True)

    for ruta_original in pdf_paths:
        archivo = os.path.basename(ruta_original)
        nombre_sin_ext = os.path.splitext(archivo)[0]
        carpeta_destino = os.path.join(ruta_salida, nombre_sin_ext)
        os.makedirs(carpeta_destino, exist_ok=True)

        if opcion_nombres == "original":
            nuevo_nombre = archivo
        elif opcion_nombres == "comun":
            nuevo_nombre = f"{nombre_comun}.pdf"
        elif opcion_nombres == "personalizado":
            nuevo_nombre = nombres_personalizados.get(archivo, archivo)
            if not nuevo_nombre.lower().endswith(".pdf"):
                nuevo_nombre += ".pdf"
        else:
            nuevo_nombre = archivo  # fallback

        ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
        shutil.move(ruta_original, ruta_destino)

    # Crear ZIP con los archivos organizados
    zip_path = os.path.join(ruta_salida, "organizados.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(ruta_salida):
            for file in files:
                if file == "organizados.zip":
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, ruta_salida)
                zipf.write(file_path, arcname)

    return f"Archivos organizados correctamente en '{ruta_salida}'.", zip_path


# Ejemplo para usar en Streamlit:

def streamlit_organizador():
    st.header("Organizar PDFs")

    archivos_subidos = st.file_uploader(
        "Sube los archivos PDF para organizar",
        type=["pdf"],
        accept_multiple_files=True
    )

    ruta_salida = st.text_input("Ruta de salida donde organizar los PDFs", value="organizados")

    opciones = {
        "original": "Conservar el nombre original",
        "comun": "Usar el mismo nuevo nombre para todos",
        "personalizado": "Especificar un nombre diferente para cada archivo"
    }

    opcion = st.selectbox("¿Cómo deseas nombrar los archivos PDF?", list(opciones.values()))

    if opcion == opciones["comun"]:
        nombre_comun = st.text_input("Ingresa el nuevo nombre común para todos (sin .pdf)", value="resultado")
    else:
        nombre_comun = None

    nombres_personalizados = {}
    if opcion == opciones["personalizado"] and archivos_subidos:
        for archivo in archivos_subidos:
            nuevo_nombre = st.text_input(f"Nuevo nombre para '{archivo.name}' (sin .pdf)", value=os.path.splitext(archivo.name)[0])
            nombres_personalizados[archivo.name] = nuevo_nombre + ".pdf"

    if st.button("📁 Organizar PDFs"):
        if not archivos_subidos:
            st.warning("Por favor, sube al menos un archivo PDF.")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_paths = []
                    for archivo in archivos_subidos:
                        temp_path = Path(temp_dir) / archivo.name
                        with open(temp_path, "wb") as f:
                            f.write(archivo.read())
                        pdf_paths.append(str(temp_path))

                    # Map selected option to code
                    opcion_code = None
                    for k, v in opciones.items():
                        if v == opcion:
                            opcion_code = k

                    mensaje, zip_path = organizar_pdfs(
                        pdf_paths,
                        ruta_salida,
                        opcion_code,
                        nombres_personalizados if opcion_code == "personalizado" else None,
                        nombre_comun if opcion_code == "comun" else None
                    )
                    st.success(mensaje)
                    with open(zip_path, "rb") as fzip:
                        st.download_button(
                            label="📦 Descargar ZIP con archivos organizados",
                            data=fzip,
                            file_name="organizados.zip",
                            mime="application/zip"
                        )
            except Exception as e:
                st.error(f"Ocurrió un error al organizar los PDFs: {e}")

