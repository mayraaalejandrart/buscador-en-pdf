with tab2:
    archivos_para_organizar = st.file_uploader(
        "Sube los PDFs a organizar",
        type=["pdf"],
        accept_multiple_files=True
    )

    opcion_nombres = st.selectbox(
        "¿Cómo deseas nombrar los archivos PDF?",
        ["Conservar el nombre original", "Usar el mismo nuevo nombre para todos", "Especificar un nombre diferente para cada archivo"]
    )

    nombre_comun = None
    nombres_individuales = None

    if opcion_nombres == "Usar el mismo nuevo nombre para todos":
        nombre_comun = st.text_input("Ingrese el nuevo nombre común (sin .pdf)", value="resultado")
    elif opcion_nombres == "Especificar un nombre diferente para cada archivo" and archivos_para_organizar:
        nombres_individuales = []
        for archivo in archivos_para_organizar:
            nuevo_nombre = st.text_input(f"Nuevo nombre para '{archivo.name}' (sin .pdf)", value=Path(archivo.name).stem)
            nombres_individuales.append(nuevo_nombre)

    if st.button("📁 Organizar PDFs"):
        if not archivos_para_organizar:
            st.warning("Por favor, sube al menos un archivo PDF.")
        else:
            try:
                import tempfile
                from pathlib import Path

                with tempfile.TemporaryDirectory() as temp_dir:
                    pdf_paths = []
                    for archivo in archivos_para_organizar:
                        temp_path = Path(temp_dir) / archivo.name
                        with open(temp_path, "wb") as f:
                            f.write(archivo.read())
                        pdf_paths.append(str(temp_path))

                    zip_path = organizar_pdfs(pdf_paths, opcion_nombres, nombre_comun, nombres_individuales)

                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="📦 Descargar ZIP con PDFs organizados",
                            data=f,
                            file_name="organizados.zip",
                            mime="application/zip"
                        )
            except Exception as e:
                st.error(f"Ocurrió un error al organizar los PDFs: {e}")
