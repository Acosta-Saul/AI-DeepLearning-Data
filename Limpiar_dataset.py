import os
import json
from PIL import Image
import numpy as np

def vectorize_image(image_path):
    """Vectoriza la imagen y la convierte a un array de numpy."""
    with Image.open(image_path) as img:
        img = img.resize((128, 128))  # Redimensionar la imagen
        img_array = np.array(img)
        return img_array.flatten().tolist()  # Aplanar el array y convertir a lista

def load_existing_data(json_file):
    """Carga los datos existentes del archivo JSON, si existe."""
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            return json.load(file)
    return []

def process_folders(folder_names, json_file='dataset_habits_socializar.json'):
    data = load_existing_data(json_file)  # Cargar datos existentes
    base_path = os.getcwd()  # Obtener la ruta del directorio actual

    for folder_name in folder_names:
        folder_path = os.path.join(base_path, folder_name)  # Combinar la ruta base con el nombre de la carpeta

        if os.path.isdir(folder_path):
            # Eliminar archivos .xml si la carpeta se llama "Rezar"
            if folder_name == "Socializar":
                for file in os.listdir(folder_path):
                    if file.endswith('.xml'):
                        os.remove(os.path.join(folder_path, file))

            # Seleccionar las primeras 110 imágenes
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            selected_images = images[:60]

            # Si la carpeta es "Rezar", seleccionar 125 imágenes (1 de cada 4)
            if folder_name == "Socializar":
                selected_images = images[::1][:60]

            # Vectorizar y añadir al JSON
            for image_name in selected_images:
                image_path = os.path.join(folder_path, image_name)
                vector = vectorize_image(image_path)
                data.append({
                    "image": vector,
                    "description": folder_name
                })

    # Guardar todos los datos en el archivo JSON
    with open(json_file, 'w') as json_file:
        json.dump(data, json_file)

    print("Lista la carpeta", base_path)

# Lista de nombres de carpetas
folder_names = [
    'Socializar'
]

process_folders(folder_names)
