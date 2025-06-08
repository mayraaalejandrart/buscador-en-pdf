import os
import shutil
import streamlit as st

def organizar_pdfs():
    st.header("Organizar PDFs")
    
    folder = st.text_input("Ruta de la carpeta donde están los archivos PDF", value=os.getcwd())

    if not os.path.isdir(folder):
        st.warning("La ruta especificada no es válida.")
        return

    opciones = {
        "1": "Conservar el nombre original",
        "2": "Usar el mismo nuevo nombre para todos",
        "3": "Especificar un nombre diferente para cada archivo"
    }

    opcion = st.selectbox("¿Cómo deseas nombrar los archivos PDF?", list(opciones.values()))

    if st.button("Organizar PDFs"):
        archivos_pdf = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
        if not archivos_pdf:
            st.warning("No se encontraron archivos PDF en la ruta especificada.")
            return

        for archivo in archivos_pdf:
            ruta_original = os.path.join(folder, archivo)
            nombre_sin_extension = os.path.splitext(archivo)[0]
            carpeta_destino = os.path.join(folder, nombre_sin_extension)
            os.makedirs(carpeta_destino, exist_ok=True)

            # Determinar nuevo nombre según opción
            if opcion == opciones["1"]:
                nuevo_nombre = archivo
            elif opcion == opciones["2"]:
                nombre_comun = st.text_input("Ingresa el nuevo nombre común para todos (sin .pdf)", value="resultado")
                if not nombre_comun:
                    st.warning("Debes ingresar un nombre válido.")
                    return
                nuevo_nombre = f"{nombre_comun}.pdf"
            elif opcion == opciones["3"]:
                nuevo_nombre = st.text_input(f"Nuevo nombre para '{archivo}' (sin .pdf)", value=nombre_sin_extension)
                if not nuevo_nombre:
                    st.warning(f"Nombre inválido para el archivo '{archivo}'.")
                    return
                nuevo_nombre = f"{nuevo_nombre}.pdf"
            else:
                st.warning("Opción no válida.")
                return

            ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
            shutil.move(ruta_original, ruta_destino)
        
        st.success("Archivos organizados correctamente.")
