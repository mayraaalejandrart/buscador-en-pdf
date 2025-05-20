
import streamlit as st
import zipfile
import tempfile
import os
from busqueda_pdf import buscar_por_nombres
from busqueda_nit_pdf import buscar_por_nit_y_nombre

st.set_page_config(page_title="🔎 Buscador PDF", layout="centered")

st.title("🔎 Buscador de nombres / NIT en PDFs")

tipo_busqueda = st.radio("¿Qué tipo de búsqueda deseas hacer?", ("Por nombre de persona", "Por NIT y nombre de empresa"))

archivo_txt = st.file_uploader("Sube el archivo de nombres o NITs (formato .TXT)", type=["txt"])

archivos_pdf = st.file_uploader("Sube los archivos PDF", type=["pdf"], accept_multiple_files=True)

iniciar = st.button("Iniciar búsqueda")

if iniciar:
    if not archivo_txt or not archivos_pdf:
        st.warning("Debes subir el archivo TXT y al menos un archivo PDF.")
    else:
        with st.spinner("Procesando archivos..."):
            if tipo_busqueda == "Por nombre de persona":
                paths = buscar_por_nombres(archivo_txt, archivos_pdf)
            else:
                paths = buscar_por_nit_y_nombre(archivo_txt, archivos_pdf)

            # Crear un ZIP
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
