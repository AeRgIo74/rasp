#!/usr/bin/env python3
import cv2
import os
from picamera2 import Picamera2

# Definir la ubicación donde se guardarán las capturas
capture_dir = '/home/leyla/Desktop/LAB7/CAPTURA'

# Crear el directorio "CAPTURA" si no existe
os.makedirs(capture_dir, exist_ok=True)

# Inicializar la cámara
camera = Picamera2()
camera.start()

def take_photo(frame_number):

    filename = f'{capture_dir}/imagen{frame_number}.jpg'
    camera.capture_file(filename)
    print(f'Capturada: {filename}')

def process_image(image_path):

    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Obtener dimensiones
    height, width = gray_image.shape[:2]

    # Dividir la imagen en cuadrantes
    quadrants = {
        "Cuadrante 1": gray_image[:height // 2, :width // 2],  # Superior Izquierda
        "Cuadrante 2": gray_image[:height // 2, width // 2:],  # Superior Derecha
        "Cuadrante 3": gray_image[height // 2:, :width // 2],  # Inferior Izquierda
        "Cuadrante 4": gray_image[height // 2:, width // 2:],  # Inferior Derecha
    }

    # Mostrar los cuadrantes
    for name, quadrant in quadrants.items():
        cv2.imshow(name, quadrant)

    # Esperar a que el usuario presione una tecla
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    frame_number = 1  # Contador de fotogramas

    try:
        while True:
            # Capturar el fotograma de la cámara
            frame = camera.capture_array()

            # Mostrar la imagen en una ventana
            cv2.imshow("Camara", frame)

            # Verificar si se presiona la tecla 'c'
            key = cv2.waitKey(1)

            if key == ord('c'):
                take_photo(frame_number)  # Capturar la imagen
                process_image(f'{capture_dir}/imagen{frame_number}.jpg')  # Procesar la imagen
                frame_number += 1  # Incrementar el contador de fotogramas

            # Verificar si se presiona la tecla 'q' para salir
            if key == ord('s'):
                break

    except KeyboardInterrupt:
        print("Proceso terminado por el usuario.")

    finally:
        camera.stop_preview()
        cv2.destroyAllWindows()
