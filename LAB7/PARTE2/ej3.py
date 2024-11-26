import cv2
import os
import matplotlib.pyplot as plt

# Ruta de la carpeta "colors"
folder_path = '/home/leyla/Desktop/LAB7/PARTE2/COLORS'

# Lista de archivos de imágenes en la carpeta
image_files = os.listdir(folder_path)

class ColorConverter:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("No se pudo cargar la imagen.")

    def to_rgb(self):

        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def to_hsv(self):

        return cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

    def to_grayscale(self):

        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

# Crear una figura para mostrar las imágenes
fig, axes = plt.subplots(3, 3, figsize=(10, 5))  # 3 filas y 3 columnas
axes = axes.flatten()  #  matriz de ejes

# Contador para las posiciones en la cuadrícula
index = 0


for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)

    try:
        converter = ColorConverter(image_path)

        
        rgb_image = converter.to_rgb()
        hsv_image = converter.to_hsv()
        grayscale_image = converter.to_grayscale()

        
        axes[index].imshow(rgb_image)
        axes[index].set_title('RGB')
        axes[index].axis('off') 
        index += 1

        axes[index].imshow(hsv_image)
        axes[index].set_title('HSV')
        axes[index].axis('off')  # Ocultar los ejes
        index += 1

        axes[index].imshow(grayscale_image, cmap='gray')
        axes[index].set_title('Grayscale')
        axes[index].axis('off')  # Ocultar los ejes
        index += 1

        # Limitar la cantidad de imágenes a 9
        if index >= 9:
            break

    except ValueError as e:
        print(e)


plt.tight_layout()
plt.show()
