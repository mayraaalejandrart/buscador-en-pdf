import os
import shutil
import tempfile
import zipfile
import streamlit as st
from pathlib import Path

def organizar_pdfs_web():
    st.header("Organizar PDFs")

    archivos_pdf = st.file_uploader(
        "Sube los archivos PDF a organizar",
        type=["pdf"],
        accept_multiple_files=True
    )

    if not archivos_pdf:
        st.info("Sube uno o más archivos PDF para comenzar.")
        return

    opciones = {
        "1": "Conservar el nombre original",
        "2": "Usar el mismo nuevo nombre para todos",
        "3": "Especificar un nombre diferente para cada archivo"
    }

    opcion = st.selectbox("¿Cómo deseas nombrar los archivos PDF?", list(opciones.values()))

    nuevo_nombre_comun = None
    nuevos_nombres_individuales = {}

    if opcion == opciones["2"]:
        nuevo_nombre_comun = st.text_input("Ingresa el nuevo nombre común para todos (sin .pdf)", value="resultado")

    if opcion == opciones["3"]:
        st.write("Ingresa el nuevo nombre para cada archivo (sin extensión .pdf):")
        for archivo in archivos_pdf:
            nombre_sin_ext = os.path.splitext(archivo.name)[0]
            nuevos_nombres_individuales[archivo.name] = st.text_input(f"Nuevo nombre para '{archivo.name}'", value=nombre_sin_ext)

    if st.button("Organizar y descargar ZIP"):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Guardar y renombrar archivos según opción
            for archivo in archivos_pdf:
                contenido = archivo.read()
                nombre_original = archivo.name
                nombre_sin_ext = os.path.splitext(nombre_original)[0]
                carpeta_destino = Path(temp_dir) / nombre_sin_ext
                carpeta_destino.mkdir(parents=True, exist_ok=True)

                if opcion == opciones["1"]:
                    nuevo_nombre = nombre_original
                elif opcion == opciones["2"]:
                    if not nuevo_nombre_comun:
                        st.error("Debes ingresar un nombre común válido.")
                        return
                    nuevo_nombre = f"{nuevo_nombre_comun}.pdf"
                elif opcion == opciones["3"]:
                    nuevo_nombre = nuevos_nombres_individuales.get(nombre_original, nombre_sin_ext)
                    if not nuevo_nombre:
                        st.error(f"Nombre inválido para el archivo '{nombre_original}'.")
                        return
                    nuevo_nombre = f"{nuevo_nombre}.pdf"
                else:
                    st.error("Opción no válida.")
                    return

                ruta_destino = carpeta_destino / nuevo_nombre
                with open(ruta_destino, "wb") as f:
                    f.write(contenido)

            # Crear ZIP con todo lo organizado
            zip_path = Path(temp_dir) / "archivos_organizados.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for carpeta in Path(temp_dir).iterdir():
                    if carpeta.is_dir():
                        for archivo in carpeta.iterdir():
                            # El arcname para mantener estructura carpeta/archivo
                            arcname = f"{carpeta.name}/{archivo.name}"
                            zipf.write(archivo, arcname=arcname)

            with open(zip_path, "rb") as fzip:
                st.download_button(
                    label="📦 Descargar archivos organizados (.zip)",
                    data=fzip,
                    file_name="archivos_organizados.zip",
                    mime="application/zip"
                )

        st.success("Proceso finalizado.")

