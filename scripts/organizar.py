import os
import shutil

def main():
    # Carpeta donde está el script
    script_path = os.path.dirname(os.path.abspath(__file__))

    # Listar PDFs
    pdfs = [f for f in os.listdir(script_path) if f.lower().endswith('.pdf')]

    print("¿Cómo deseas nombrar los archivos PDF?")
    print("1. Conservar el nombre original")
    print("2. Usar el mismo nuevo nombre para todos")
    print("3. Especificar un nombre diferente para cada archivo")
    opcion = input("Ingresa 1, 2 o 3: ").strip()

    nombre_global = None

    for pdf in pdfs:
        folder_name = os.path.splitext(pdf)[0]

        # Crear carpeta si no existe
        folder_path = os.path.join(script_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        if opcion == '1':
            new_file_name = pdf

        elif opcion == '2':
            if not nombre_global:
                nombre_global = input("Ingresa el nombre que deseas usar para todos los archivos (con o sin .pdf): ").strip()
                if not nombre_global.lower().endswith('.pdf'):
                    nombre_global += '.pdf'
            new_file_name = nombre_global

        elif opcion == '3':
            nuevo_nombre = input(f"Ingresa el nuevo nombre para '{pdf}' (con o sin .pdf): ").strip()
            if not nuevo_nombre.lower().endswith('.pdf'):
                nuevo_nombre += '.pdf'
            new_file_name = nuevo_nombre

        else:
            print("Opción inválida. Se usará el nombre original.")
            new_file_name = pdf

        # Mover el archivo
        origen = os.path.join(script_path, pdf)
        destino = os.path.join(folder_path, new_file_name)

        # Si el destino ya existe, preguntar o sobrescribir (aquí sobrescribimos)
        if os.path.exists(destino):
            print(f"El archivo {destino} ya existe y será sobrescrito.")

        shutil.move(origen, destino)

    print("Archivos organizados correctamente.")

if __name__ == "__main__":
    main()
