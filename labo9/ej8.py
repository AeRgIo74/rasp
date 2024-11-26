import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('figuras.png')
output = image.copy()

# Convertir a escala de grises y aplicar umbral
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def detect_color(contour, image):
    mask = np.zeros(image.shape[:2], dtype=np.uint8)  # Crear máscara
    cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)  # Llenar el contorno en la máscara
    mean_val = cv2.mean(image, mask=mask)[:3]  # Obtener los valores promedio BGR

    # Normalizar los valores BGR para obtener RGB
    b, g, r = mean_val

    # Clasificar el color basado en los valores RGB
    if r > 200 and g < 100 and b < 100:
        return "Rojo brillante"
    elif r < 100 and g > 200 and b < 100:
        return "Verde brillante"
    elif r < 100 and g < 100 and b > 200:
        return "Azul brillante"
    elif r > 150 and g > 100 and b < 100:
        return "Amarillo"
    elif r < 100 and g > 150 and b > 100:
        return "Cyan"
    elif r > 100 and g < 100 and b > 150:
        return "Magenta"
    elif r > 100 and g > 100 and b > 100:
        return "Blanco"
    elif r < 100 and g < 100 and b < 100:
        return "Negro"
    else:
        return "Color intermedio"



# Iterar a través de los contornos y detectar formas y colores
for contour in contours:
    # Aproximar el contorno para detectar la forma
    epsilon = 0.01 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    x, y, w, h = cv2.boundingRect(approx)

    # Detectar la forma según la cantidad de vértices
    vertices = len(approx)
    if vertices == 3:
        shape_type = "Triangulo"
    elif vertices == 4:
        aspect_ratio = w / float(h)
        shape_type = "Cuadrado" if 0.95 <= aspect_ratio <= 1.05 else "Rectangulo"
    elif vertices == 5:
        shape_type = "Pentagono"
    elif vertices == 6:
        shape_type = "Hexagono"
    elif vertices > 6:
        shape_type = "circulo"  # Para más de 6 lados
    else:
        shape_type = "Desconocido"

    # Detectar color
    color = detect_color(contour, image)
    
    # Dibujar el contorno y poner texto en la imagen de salida
    cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)  # Dibujar el contorno aproximado
    cv2.putText(output, f"{color} {shape_type}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

# Mostrar la imagen de salida
cv2.imshow("Formas y Colores Detectados", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
