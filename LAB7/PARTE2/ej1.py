


# import cv2
# import os

# # Ruta de la carpeta "colors"
# folder_path = '/home/leyla/Desktop/LAB7/PARTE2/COLORS'

# # Lista de archivos de imágenes en la carpeta
# image_files = os.listdir(folder_path)

# # Abre cada imagen e imprime el valor del color
# for image_file in image_files:
#     image_path = os.path.join(folder_path, image_file)
#     image = cv2.imread(image_path)

#     # Obtiene el valor medio de los píxeles de la imagen (BGR)
#     avg_color_per_row = cv2.mean(image)[:3]
#     print(f'Imagen: {image_file}, Color promedio (BGR): {avg_color_per_row}')

import cv2
import os
import matplotlib.pyplot as plt


folder_path = '/home/leyla/Desktop/LAB7/PARTE2/COLORS'


# Lista de archivos de imágenes en la carpeta
image_files = os.listdir(folder_path)

# Inicializar la figura para mostrar las imágenes en una fila
f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5))


for idx, image_file in enumerate(image_files):
    image_path = os.path.join(folder_path, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: No se pudo cargar la imagen {image_file}")
        continue

    #  BGR a RGB matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # valor medio de los píxelesy redondea
    avg_color_per_row = cv2.mean(image)[:3]
    avg_color_per_row = tuple(round(c, 1) for c in avg_color_per_row)

    print(f'Imagen: {image_file}, Color promedio (BGR): {avg_color_per_row}')

    # Mostrar la imagen en su correspondiente posición
    ax = [ax1, ax2, ax3][idx]  # Elegir el eje correspondiente (1, 2 o 3)
    ax.imshow(image_rgb)
    ax.set_title(f'{image_file}\nBGR: {avg_color_per_row}', fontsize=10)
    ax.axis('on')  # Ocultar los ejes

# Ajustar el diseño
plt.tight_layout()
plt.show()
