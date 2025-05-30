import streamlit as st
import zipfile
import tempfile
import os
import shutil
from busqueda_pdf import buscar_por_nombres
from busqueda_nit_pdf import buscar_por_nit_y_nombre
from scripts.organizar import organizar_pdfs

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
            with tempfile.TemporaryDirectory() as temp_dir:
                if tipo_busqueda == "Por nombre de persona":
                    paths = buscar_por_nombres(archivo_txt, archivos_pdf, output_dir=temp_dir)
                else:
                    paths = buscar_por_nit_y_nombre(archivo_txt, archivos_pdf, output_dir=temp_dir)

                st.session_state["resultado_dir"] = temp_dir
                st.session_state["pdf_generados"] = paths

                zip_path = os.path.join(temp_dir, "resultados.zip")
                with zipfile.ZipFile(zip_path, "w") as zf:
                    for path in paths:
                        zf.write(path, arcname=os.path.basename(path))

                st.success("¡Búsqueda completada!")
                with open(zip_path, "rb") as f:
                    st.download_button(
                        label="📦 Descargar resultados (.zip)",
                        data=f,
                        file_name="resultados.zip",
                        mime="application/zip"
                    )

st.markdown("---")
st.header("📄 Organizador y renombrador de PDFs (opcional)")

usar_resultados = st.checkbox("Usar los resultados generados en la búsqueda anterior", value=True)

pdfs_para_organizar = []

if usar_resultados and "pdf_generados" in st.session_state:
    pdfs_para_organizar = st.session_state["pdf_generados"]
else:
    pdfs_subidos = st.file_uploader("O subir manualmente los PDFs a organizar", type=["pdf"], accept_multiple_files=True)
    if pdfs_subidos:
        for archivo in pdfs_subidos:
            temp_path = os.path.join(tempfile.gettempdir(), archivo.name)
            with open(temp_path, "wb") as f:
                f.write(archivo.read())
            pdfs_para_organizar.append(temp_path)

if st.button("Ejecutar organizador"):
    if not pdfs_para_organizar:
        st.info("No se encontraron archivos PDF para organizar.")
    else:
        ruta_salida = os.path.join(tempfile.gettempdir(), "organizados")
        os.makedirs(ruta_salida, exist_ok=True)
        organizar_pdfs(pdfs_para_organizar, ruta_salida)
        st.success("Organización completada.")

        zip_organizados = os.path.join(ruta_salida, "organizados.zip")
        with zipfile.ZipFile(zip_organizados, "w") as z:
            for f in os.listdir(ruta_salida):
                ruta_f = os.path.join(ruta_salida, f)
                if os.path.isfile(ruta_f):
                    z.write(ruta_f, arcname=f)

        with open(zip_organizados, "rb") as f:
            st.download_button(
                label="📂 Descargar PDFs organizados",
                data=f,
                file_name="organizados.zip",
                mime="application/zip"
            )
