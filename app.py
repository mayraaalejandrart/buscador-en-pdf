import streamlit as st
import zipfile
import tempfile
import os
from pathlib import Path

from busqueda_pdf import buscar_por_nombres
from busqueda_nit_pdf import buscar_por_nit_y_nombre
from scripts.organizar import organizar_pdfs  # Verifica que la ruta sea correcta

st.set_page_config(page_title="🔎 Buscador PDF + Organizador", layout="centered")

st.title("🧰 Herramienta PDF: Búsqueda y Organización")

tab1, tab2 = st.tabs(["🔍 Buscar en PDFs", "🗂️ Organizar PDFs"])

# ----- TAB 1: BUSCAR EN PDF -----
with tab1:
    tipo_busqueda = st.radio(
        "¿Qué tipo de búsqueda deseas hacer?",
        ("Por nombre de persona", "Por NIT y nombre de empresa")
    )

    archivo_txt = st.file_uploader(
        "Sube el archivo de nombres o NITs (formato .TXT)",
        type=["txt"]
    )
    archivos_pdf = st.file_uploader(
        "Sube los archivos PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("🔎 Iniciar búsqueda"):
        if not archivo_txt or not archivos_pdf:
            st.warning("Debes subir el archivo TXT y al menos un archivo PDF.")
        else:
            try:
                with st.spinner("Procesando archivos..."):
                    # Guardar archivo TXT temporalmente
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_txt:
                        tmp_txt.write(archivo_txt.read())
                        tmp_txt_path = tmp_txt.name

                    # Guardar PDFs temporalmente Y guardar nombres originales
                    pdf_paths = []
                    pdf_nombres = []
                    for archivo in archivos_pdf:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                            tmp_pdf.write(archivo.read())
                            pdf_paths.append(tmp_pdf.name)
                            pdf_nombres.append(archivo.name)  # CORRECCIÓN: Guardar nombre original

                    # Lógica de búsqueda con nombres originales
                    if tipo_busqueda == "Por nombre de persona":
                        paths = buscar_por_nombres(tmp_txt_path, pdf_paths, pdf_nombres)
                    else:
                        paths = buscar_por_nit_y_nombre(tmp_txt_path, archivos_pdf)

                    if not paths:
                        st.warning("No se encontraron coincidencias en los PDFs.")
                    else:
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
            except Exception as e:
                st.error(f"Ocurrió un error durante la búsqueda: {e}")

# ----- TAB 2: ORGANIZAR PDFS -----
with tab2:
    archivos_para_organizar = st.file_uploader(
        "Sube los PDFs a organizar",
        type=["pdf"],
        accept_multiple_files=True
    )

    opcion_nombres = st.selectbox("¿Cómo deseas nombrar los archivos PDF?", [
        "Conservar el nombre original",
        "Usar el mismo nuevo nombre para todos",
        "Especificar un nombre diferente para cada archivo"
    ])

    nombre_comun = None
    nombres_individuales = []

    if opcion_nombres == "Usar el mismo nuevo nombre para todos":
        nombre_comun = st.text_input("Nuevo nombre común (sin .pdf)", value="resultado")
    elif opcion_nombres == "Especificar un nombre diferente para cada archivo":
        for archivo in archivos_para_organizar or []:
            nuevo_nombre = st.text_input(f"Nuevo nombre para '{archivo.name}'", value=Path(archivo.name).stem)
            nombres_individuales.append(nuevo_nombre)

    if st.button("📁 Organizar PDFs"):
        if not archivos_para_organizar:
            st.warning("Por favor, sube al menos un archivo PDF.")
        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_paths = []
                    for archivo in archivos_para_organizar:
                        temp_path = Path(temp_dir) / archivo.name
                        with open(temp_path, "wb") as f:
                            f.write(archivo.read())
                        pdf_paths.append(str(temp_path))

                    zip_path = organizar_pdfs_zip(
                        pdf_paths,
                        opcion_nombres,
                        nombre_comun,
                        nombres_individuales
                    )

                    st.success("Archivos organizados correctamente.")
                    with open(zip_path, "rb") as f:
                        st.download_button("📦 Descargar ZIP", f, file_name="organizados.zip")
            except Exception as e:
                st.error(f"Ocurrió un error al organizar los PDFs: {e}")
