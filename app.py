import streamlit as st
import zipfile
import tempfile
import os
from pathlib import Path
from busqueda_pdf import buscar_por_nombres
from busqueda_nit_pdf import buscar_por_nit_y_nombre
from scripts.organizar import organizar_pdfs  # función que definimos antes

st.set_page_config(page_title="🔎 Buscador PDF + Organizador", layout="centered")

st.title("🔎 Buscador de nombres / NIT en PDFs")

# --- SECCIÓN BUSCADOR ---
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
                    paths = buscar_por_nombres(archivo_txt, archivos_pdf, carpeta_resultados=temp_dir)
                else:
                    paths = buscar_por_nit_y_nombre(archivo_txt, archivos_pdf, carpeta_resultados=temp_dir)

                # Crear un ZIP con resultados
                with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_zip:
                    with zipfile.ZipFile(tmp_zip.name, "w") as zf:
                        for path in paths:
                            if os.path.isfile(path):
                                zf.write(path, arcname=os.path.basename(path))

                    st.success("¡Búsqueda completada!")
                    with open(tmp_zip.name, "rb") as f:
                        st.download_button(
                            label="📦 Descargar resultados (.zip)",
                            data=f,
                            file_name="resultados.zip",
                            mime="application/zip"
                        )

st.markdown("---")

# --- SECCIÓN ORGANIZADOR ---
st.header("🗂 Organizador y renombrador de PDFs (opcional)")

# Obtener ruta actual del script
script_path = Path(__file__).parent.resolve()
pdfs_en_carpeta = [f.name for f in script_path.glob("*.pdf")]

if not pdfs_en_carpeta:
    st.info("No se encontraron archivos PDF en la carpeta del script para organizar.")
else:
    opcion = st.radio("¿Cómo deseas nombrar los archivos PDF?", 
                      options=[1, 2, 3], 
                      format_func=lambda x: {
                          1: "Conservar nombre original",
                          2: "Usar mismo nombre para todos",
                          3: "Especificar un nombre diferente para cada archivo"
                      }[x])

    nombre_global = None
    nombres_individuales = {}

    if opcion == 2:
        nombre_global = st.text_input("Ingresa el nombre que deseas usar para todos los archivos (sin .pdf):")

    if opcion == 3:
        st.write("Ingresa nuevo nombre para cada archivo (sin extensión .pdf):")
        for archivo in pdfs_en_carpeta:
            nuevo_nombre = st.text_input(f"{archivo}", key=archivo)
            if nuevo_nombre:
                nombres_individuales[archivo] = nuevo_nombre

    if st.button("Organizar PDFs"):
        resultado = organizar_pdfs(opcion, nombre_global, nombres_individuales)
        st.success(resultado)
