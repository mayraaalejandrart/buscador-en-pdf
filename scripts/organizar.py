import streamlit as st
import zipfile
import tempfile
import os
from pathlib import Path
import shutil
from scripts.organizar import organizar_pdfs

st.set_page_config(page_title="🗂️ Organizador de PDFs", layout="centered")

st.title("🗂️ Organizador de PDFs")

# Crear pestañas

tab1, tab2 = st.tabs(["ℹ️ Instrucciones", "📁 Organizar PDFs"])

with tab1:
    st.markdown("""
    ### ¿Qué hace esta herramienta?
    Esta sección te permite organizar múltiples archivos PDF en carpetas con nombres personalizados, según sus nombres.

    **¿Cómo funciona?**
    - Sube los archivos PDF generados previamente.
    - El sistema creará una carpeta por cada archivo PDF (según su nombre base).
    - Dentro de cada carpeta se ubicará su respectivo archivo.

    Al final podrás descargar todos los archivos organizados en un único archivo `.zip`.
    """)

with tab2:
    archivos_para_organizar = st.file_uploader("Sube los PDFs a organizar", type=["pdf"], accept_multiple_files=True)
    ruta_salida = st.text_input("Ruta de salida donde organizar los PDFs", value="organizados")

    if st.button("📁 Organizar PDFs"):
        if not archivos_para_organizar:
            st.warning("Por favor, sube al menos un archivo PDF.")
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                pdf_paths = []
                for archivo in archivos_para_organizar:
                    temp_path = Path(temp_dir) / archivo.name
                    with open(temp_path, "wb") as f:
                        f.write(archivo.read())
                    pdf_paths.append(temp_path)

                # Ejecutar función organizadora
                resultado = organizar_pdfs(pdf_paths, ruta_salida)
                st.success(resultado)

                # Crear archivo ZIP
                zip_path = Path(temp_dir) / "organizados.zip"
                with zipfile.ZipFile(zip_path, "w") as zipf:
                    for folder, _, files in os.walk(ruta_salida):
                        for file in files:
                            file_path = Path(folder) / file
                            zipf.write(file_path, arcname=file_path.relative_to(ruta_salida))

                # Botón de descarga
                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="📦 Descargar PDFs organizados (.zip)",
                        data=f,
                        file_name="organizados.zip",
                        mime="application/zip"
                    )
