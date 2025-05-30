import streamlit as st
import zipfile
import tempfile
import os
from pathlib import Path

from busqueda_pdf import buscar_por_nombres
from busqueda_nit_pdf import buscar_por_nit_y_nombre
from scripts.organizar import organizar_pdfs  # Asegúrate que esta ruta es correcta

st.set_page_config(page_title="🔎 Buscador PDF + Organizador", layout="centered")

st.title("🧰 Herramienta PDF: Búsqueda y Organización")

# Crear pestañas
tab1, tab2 = st.tabs(["🔍 Buscar en PDFs", "🗂️ Organizar PDFs"])

# ----- TAB 1: BUSCAR EN PDF -----
with tab1:
    tipo_busqueda = st.radio("¿Qué tipo de búsqueda deseas hacer?", 
                              ("Por nombre de persona", "Por NIT y nombre de empresa"))

    archivo_txt = st.file_uploader("Sube el archivo de nombres o NITs (formato .TXT)", type=["txt"])
    archivos_pdf = st.file_uploader("Sube los archivos PDF", type=["pdf"], accept_multiple_files=True)

    if st.button("🔎 Iniciar búsqueda"):
        if not archivo_txt or not archivos_pdf:
            st.warning("Debes subir el archivo TXT y al menos un archivo PDF.")
        else:
            with st.spinner("Procesando archivos..."):
                if tipo_busqueda == "Por nombre de persona":
                    paths = buscar_por_nombres(archivo_txt, archivos_pdf)
                else:
                    paths = buscar_por_nit_y_nombre(archivo_txt, archivos_pdf)

                # Crear archivo ZIP con los resultados
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                    with zipfile.ZipFile(tmp_zip.name, "w") as zf:
                        for path in paths:
                            zf.write(path, arcname=os.path.basename(path))

                    st.success("¡Búsqueda completada!")
                    with open(tmp_zip.name, "rb") as f:
                        st.download_button(
                            label="📦 Descargar resultados (.zip)",
                            data=f,
                            file_name="resultados.zip",
                            mime="application/zip"
                        )

# ----- TAB 2: ORGANIZAR PDFS -----
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

                resultado = organizar_pdfs(pdf_paths, ruta_salida)
                st.success(resultado)
