import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_color(image, lower_hsv, upper_hsv):
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

    return mask

# Definir los rangos
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

lower_green = np.array([50, 50, 50])
upper_green = np.array([70, 255, 255])

lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])

# Ruta 
image_path = '/home/leyla/Desktop/FOTOS/RGB.jpg'
# Cargar 
image = cv2.imread(image_path)

if image is None:
    print("No se pudo cargar la imagen.")
else:
    # Detectar los colores en la imagen
    red_mask = detect_color(image, lower_red, upper_red)
    green_mask = detect_color(image, lower_green, upper_green)
    blue_mask = detect_color(image, lower_blue, upper_blue)

    # imágenes enmascaradas
    masked_image_red = np.copy(image)
    masked_image_red[red_mask == 0] = [0, 0, 0]  

    masked_image_green = np.copy(image)
    masked_image_green[green_mask == 0] = [0, 0, 0]

    masked_image_blue = np.copy(image)
    masked_image_blue[blue_mask == 0] = [0, 0, 0]  


    f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(10, 5))

    # imagen enmascarada
    ax1.set_title('RED')
    ax1.imshow(masked_image_red)  
    ax1.axis('off')

    ax2.set_title('GREEN')
    ax2.imshow(masked_image_green) 
    ax2.axis('off')

    ax3.set_title('BLUE')
    ax3.imshow(masked_image_blue)  
    ax3.axis('off')

    #  máscara
    ax4.set_title('RED Mask')
    ax4.imshow(red_mask, cmap='gray')
    ax4.axis('off')

    ax5.set_title('GREEN Mask')
    ax5.imshow(green_mask, cmap='gray')
    ax5.axis('off')

    ax6.set_title('BLUE Mask')
    ax6.imshow(blue_mask, cmap='gray')
    ax6.axis('off')

    plt.tight_layout()
    plt.show()
