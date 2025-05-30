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

# 1. Selección del tipo de búsqueda
tipo_busqueda = st.radio("¿Qué tipo de búsqueda deseas hacer?", ("Por nombre de persona", "Por NIT y nombre de empresa"))

# 2. Subida de archivos
archivo_txt = st.file_uploader("Sube el archivo de nombres o NITs (formato .TXT)", type=["txt"])
archivos_pdf = st.file_uploader("Sube los archivos PDF", type=["pdf"], accept_multiple_files=True)

# 3. Ejecutar búsqueda
iniciar = st.button("Iniciar búsqueda")

# Carpeta temporal para los resultados
output_folder = tempfile.mkdtemp()

if iniciar:
    if not archivo_txt or not archivos_pdf:
        st.warning("Debes subir el archivo TXT y al menos un archivo PDF.")
    else:
        with st.spinner("Procesando archivos..."):
            if tipo_busqueda == "Por nombre de persona":
                paths = buscar_por_nombres(archivo_txt, archivos_pdf, output_folder)
            else:
                paths = buscar_por_nit_y_nombre(archivo_txt, archivos_pdf, output_folder)

            if paths:
                # Crear ZIP
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                    with zipfile.ZipFile(tmp_zip.name, "w") as zf:
                        for path in paths:
                            zf.write(path, arcname=os.path.basename(path))
                    st.success("¡Búsqueda completada!")
                    with open(tmp_zip.name, "rb") as f:
                        st.download_button(
                            label="🛋 Descargar resultados (.zip)",
                            data=f,
                            file_name="resultados.zip",
                            mime="application/zip"
                        )
            else:
                st.info("No se encontraron coincidencias para los criterios de búsqueda.")

st.markdown("---")
st.header("📄 Organizador y renombrador de PDFs (opcional)")

usar_generados = st.checkbox("Usar los resultados generados en la búsqueda anterior", value=True)

archivos_para_organizar = []
if usar_generados:
    if os.path.exists(output_folder):
        archivos_para_organizar = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith(".pdf")]
else:
    subidos = st.file_uploader("Sube manualmente los archivos PDF a organizar", type=["pdf"], accept_multiple_files=True)
    if subidos:
        carpeta_temp_manual = tempfile.mkdtemp()
        for archivo in subidos:
            temp_path = os.path.join(carpeta_temp_manual, archivo.name)
            with open(temp_path, "wb") as f:
                f.write(archivo.read())
            archivos_para_organizar.append(temp_path)

if st.button("Ejecutar organizador"):
    if not archivos_para_organizar:
        st.info("No se encontraron archivos PDF para organizar.")
    else:
        with st.spinner("Organizando archivos PDF..."):
            organizados = organizar_pdfs(archivos_para_organizar)
            if organizados:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                    with zipfile.ZipFile(tmp_zip.name, "w") as zf:
                        for path in organizados:
                            zf.write(path, arcname=os.path.basename(path))
                    st.success("Organización completada.")
                    with open(tmp_zip.name, "rb") as f:
                        st.download_button(
                            label="📁 Descargar PDFs organizados",
                            data=f,
                            file_name="organizados.zip",
                            mime="application/zip"
                        )
            else:
                st.info("No se realizaron cambios en los archivos.")
