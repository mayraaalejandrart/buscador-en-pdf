import streamlit as st
import zipfile
import tempfile
import os
from pathlib import Path
import shutil

# Importa tus funciones de búsqueda (ajusta según tu estructura)
from busqueda_pdf import buscar_por_nombres
from busqueda_nit_pdf import buscar_por_nit_y_nombre
from scripts.organizar import organizar_pdfs

st.set_page_config(page_title="🔎 Buscador PDF", layout="centered")

st.title("🔎 Buscador de nombres / NIT en PDFs")

tipo_busqueda = st.radio(
    "¿Qué tipo de búsqueda deseas hacer?",
    ("Por nombre de persona", "Por NIT y nombre de empresa")
)

archivo_txt = st.file_uploader(
    "Sube el archivo de nombres o NITs (formato .TXT)", type=["txt"]
)

archivos_pdf = st.file_uploader(
    "Sube los archivos PDF", type=["pdf"], accept_multiple_files=True
)

iniciar = st.button("Iniciar búsqueda")

if iniciar:
    if not archivo_txt or not archivos_pdf:
        st.warning("Debes subir el archivo TXT y al menos un archivo PDF.")
    else:
        with st.spinner("Procesando archivos..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                # Guardar PDFs subidos en carpeta temporal
                pdf_paths = []
                for pdf in archivos_pdf:
                    path_pdf = os.path.join(temp_dir, pdf.name)
                    with open(path_pdf, "wb") as f:
                        f.write(pdf.getbuffer())
                    pdf_paths.append(path_pdf)

                # Guardar archivo txt temporal
                path_txt = os.path.join(temp_dir, archivo_txt.name)
                with open(path_txt, "wb") as f:
                    f.write(archivo_txt.getbuffer())

                if tipo_busqueda == "Por nombre de persona":
                    paths = buscar_por_nombres(path_txt, pdf_paths, output_dir=temp_dir)
                else:
                    paths = buscar_por_nit_y_nombre(path_txt, pdf_paths, output_dir=temp_dir)

                st.session_state["resultado_dir"] = temp_dir
                st.session_state["pdf_generados"] = paths

                # Crear zip con resultados
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

usar_resultados = st.checkbox(
    "Usar los resultados generados en la búsqueda anterior", value=True
)

pdfs_para_organizar = []

if usar_resultados and "pdf_generados" in st.session_state:
    pdfs_para_organizar = st.session_state["pdf_generados"]
else:
    pdfs_subidos = st.file_uploader(
        "O subir manualmente los PDFs a organizar", type=["pdf"], accept_multiple_files=True
    )
    if pdfs_subidos:
        # Guardar los PDFs subidos en temp para pasar ruta
        for archivo in pdfs_subidos:
            temp_path = os.path.join(tempfile.gettempdir(), archivo.name)
            with open(temp_path, "wb") as f:
                f.write(archivo.getbuffer())
            pdfs_para_organizar.append(temp_path)

opcion_renombrado = st.selectbox(
    "¿Cómo deseas nombrar los archivos PDF?",
    options=[
        ("Conservar el nombre original", '1'),
        ("Usar el mismo nuevo nombre para todos", '2'),
        ("Especificar un nombre diferente para cada archivo (no implementado)", '3')
    ],
    index=0,
    format_func=lambda x: x[0]
)

if st.button("Ejecutar organizador"):
    if not pdfs_para_organizar:
        st.info("No se encontraron archivos PDF para organizar.")
    else:
        ruta_salida = os.path.join(tempfile.gettempdir(), "organizados")
        os.makedirs(ruta_salida, exist_ok=True)
        resultado = organizar_pdfs(pdfs_para_organizar, ruta_salida, opcion_renombrado=opcion_renombrado[1])
        st.success(resultado)

        # Crear zip con PDFs organizados
        zip_organizados = os.path.join(ruta_salida, "organizados.zip")
        with zipfile.ZipFile(zip_organizados, "w") as z:
            for carpeta in os.listdir(ruta_salida):
                carpeta_path = os.path.join(ruta_salida, carpeta)
                if os.path.isdir(carpeta_path):
                    for f in os.listdir(carpeta_path):
                        f_path = os.path.join(carpeta_path, f)
                        z.write(f_path, arcname=os.path.join(carpeta, f))

        with open(zip_organizados, "rb") as f:
            st.download_button(
                label="📂 Descargar PDFs organizados",
                data=f,
                file_name="organizados.zip",
                mime="application/zip"
            )
