import cv2
import numpy as np
import serial
import time

# Configuración UART para comunicación con TIVA
ser = serial.Serial('/dev/rfcomm0', 9600)  # Asegúrate de que /dev/ttyACM0 es el puerto correcto

# Inicializar la webcam
cap = cv2.VideoCapture(0)

# Inicializar los sustractores de fondo
mog2_subtractor = cv2.createBackgroundSubtractorMOG2()
knn_subtractor = cv2.createBackgroundSubtractorKNN()

# Crear la ventana una sola vez
cv2.namedWindow('Comparación de Sustractores', cv2.WINDOW_NORMAL)

# Bucle para procesar el video cuadro a cuadro
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el cuadro a escala de grises
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Operación de apertura para eliminar ruido
    kernel = np.ones((5, 5), np.uint8)
    opened_image = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, kernel)

    # Aplicar filtro de desenfoque promedio y CLAHE
    mean_blurred_image = cv2.blur(opened_image, (5, 5))
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(mean_blurred_image)

    # Aplicar los sustractores de fondo
    knn_mask = knn_subtractor.apply(clahe_image)

    # Encontrar contornos en la máscara para detectar el objeto
    contours, _ = cv2.findContours(knn_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    object_detected = False
    command = 'S'  # Por defecto, comando de "Stop"

    # Comprobar si hay algún contorno
    if contours:
        # Tomar el contorno más grande como el objeto detectado
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(largest_contour)

        # Dibujar el contorno y el cuadro delimitador
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calcular el centro del objeto
        object_center_x = x + w // 2
        object_detected = True

        # Determinar dirección basada en la posición del objeto en la imagen
        frame_center_x = frame.shape[1] // 2

        if object_center_x < frame_center_x - 100:
            command = 'L'  # Mover a la izquierda
        elif object_center_x > frame_center_x + 100:
            command = 'R'  # Mover a la derecha
        else:
            command = 'F'  # Mover hacia adelante

        # Mostrar estado de detección en pantalla
        cv2.putText(frame, f"Objeto detectado - Mov: {command}", (10, frame.shape[0] - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Enviar el comando a TIVA solo si hay un objeto detectado
    if object_detected:
        ser.write(command.encode())
        #time.sleep(0.1)  # Pausa para UART

    # Mostrar resultados en ventana
    combined = np.hstack((frame, cv2.cvtColor(knn_mask, cv2.COLOR_GRAY2BGR)))
    cv2.imshow('Comparación de Sustractores', combined)

    # Salir si se presiona 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
ser.close()
cv2.destroyAllWindows()
