import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen
image = cv2.imread('monedas.jpg')

# Convertir a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aplicar el filtro de desenfoque promedio
kernel_size = (5, 5)
mean_blurred_image = cv2.blur(gray, kernel_size)

# Aplicar CLAHE
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_image = clahe.apply(mean_blurred_image)

# Aplicar un umbral para obtener una imagen binaria
_, binary = cv2.threshold(clahe_image, 127, 255, cv2.THRESH_BINARY)

# Encontrar los contornos en la imagen binaria
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar y dibujar solo los contornos que cumplen con el área mínima
min_area = 2500
coin_count = 0
image_contours = image.copy()
for contour in contours:
    if cv2.contourArea(contour) > min_area:
        cv2.drawContours(image_contours, [contour], -1, (0, 255, 0), 2)
        coin_count += 1

# Convertir la imagen de BGR a RGB para matplotlib
image_rgb = cv2.cvtColor(image_contours, cv2.COLOR_BGR2RGB)

# Configurar subplots
plt.figure(figsize=(15, 10))

# Imagen original en escala de grises
plt.subplot(2, 3, 1)
plt.title("Escala de Grises")
plt.imshow(gray, cmap='gray')
plt.axis('off')

# Imagen desenfocada
plt.subplot(2, 3, 2)
plt.title("Desenfoque Promedio")
plt.imshow(mean_blurred_image, cmap='gray')
plt.axis('off')

# Imagen con CLAHE aplicado
plt.subplot(2, 3, 3)
plt.title("CLAHE Aplicado")
plt.imshow(clahe_image, cmap='gray')
plt.axis('off')

# Imagen binaria después del umbral
plt.subplot(2, 3, 4)
plt.title("Imagen Binaria")
plt.imshow(binary, cmap='gray')
plt.axis('off')

# Imagen final con los contornos dibujados
plt.subplot(2, 3, 5)
plt.title(f"Monedas detectadas: {coin_count}")
plt.imshow(image_rgb)
plt.axis('off')

# Mostrar todos los subplots
plt.tight_layout()
plt.show()
