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

if __name__ == "__main__":
    frame_number = 1  # Contador de fotogramas
    mode = 'grayscale'  # Modo inicial

    try:
        while True:
            # Capturar el fotograma de la cámara
            frame = camera.capture_array()

            # Cambiar entre RGB y escala de grises
            if mode == 'rgb':
                display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:  # Cambiar a escala de grises
                display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Mostrar la imagen en una ventana
            cv2.imshow("Camara", display_frame)

            # Verificar si se presiona la tecla
            key = cv2.waitKey(1)

            # Cambiar el modo al presionar 'g'
            if key == ord('g'):
                mode = 'rgb' if mode == 'grayscale' else 'grayscale'  # Cambiar de modo

            # Verificar si se presiona la tecla 'c' para capturar la imagen
            if key == ord('c'):
                take_photo(frame_number)  # Capturar la imagen
                frame_number += 1  # Incrementar el contador de fotogramas

                # Esperar a que el usuario presione una tecla
                cv2.waitKey(0)
                cv2.destroyAllWindows()  # Cerrar todas las ventanas

            # Verificar si se presiona la tecla 's' para salir
            if key == ord('s'):
                break

    except KeyboardInterrupt:
        print("Proceso terminado por el usuario.")

    finally:
        camera.stop_preview()
        cv2.destroyAllWindows()
