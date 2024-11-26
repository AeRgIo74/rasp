import cv2
import os
import matplotlib.pyplot as plt

# Ruta de la carpeta "colors"
folder_path = '/home/leyla/Desktop/LAB7/PARTE2/COLORS'

# Lista de archivos de imágenes en la carpeta
image_files = os.listdir(folder_path)

# Función para convertir una imagen a escala de grises
def convert_to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

# Función para calcular el color promedio
def calculate_average_color(image):
    avg_color = cv2.mean(image)[:3]  # Devuelve (B, G, R)
    return tuple(round(c, 1) for c in avg_color)  # Redondear a 1 decimal

# Crear una cuadrícula de 2x3 para las imágenes
f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(5, 5))

# Lista de ejes para asignar las imágenes
axes = [ax1, ax2, ax3, ax4, ax5, ax6]

# Mostrar las imágenes en color y en escala de grises
for idx, image_file in enumerate(image_files):
    image_path = os.path.join(folder_path, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: No se pudo cargar la imagen {image_file}")
        continue

    # Convertir la imagen BGR a RGB para matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Calcular el color promedio en RGB
    avg_rgb = calculate_average_color(image)

    # Convertir la imagen a escala de grises
    gray_image = convert_to_grayscale(image)

    # Calcular el valor promedio en escala de grises
    avg_gray = cv2.mean(gray_image)[0]  # Valor medio (escala de grises)

    # Mostrar la imagen original en color
    axes[idx].imshow(image_rgb)
    axes[idx].set_title(f'RGB : {avg_rgb}', fontsize=8)
    axes[idx].axis('off')  # Ocultar los ejes

    # Mostrar la imagen en escala de grises en la posición siguiente
    axes[idx + 3].imshow(gray_image, cmap='gray')
    axes[idx + 3].set_title(f'Gray : {round(avg_gray, 1)}', fontsize=8)
    axes[idx + 3].axis('off')  # Ocultar los ejes

# Ajustar el diseño
plt.tight_layout()
plt.show()
