import cv2
import numpy as np

# Ruta del video
video_path = 'bouncing.mp4'

# Cargar el video
cap = cv2.VideoCapture(video_path)

# Inicializar los sustractores de fondo
mog2_subtractor = cv2.createBackgroundSubtractorMOG2()
knn_subtractor = cv2.createBackgroundSubtractorKNN()

# Crear una ventana para mostrar el resultado
cv2.namedWindow('Contornos de Objetos en Movimiento', cv2.WINDOW_NORMAL)

# Bucle para procesar el video cuadro a cuadro
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Aplicar el sustractor de fondo
    mask_mog2 = mog2_subtractor.apply(frame)
    mask_knn = knn_subtractor.apply(frame)

    # Aplicar un umbral a la máscara para obtener una imagen binaria
    _, thresh_mog2 = cv2.threshold(mask_mog2, 254, 255, cv2.THRESH_BINARY)
    _, thresh_knn = cv2.threshold(mask_knn, 254, 255, cv2.THRESH_BINARY)

    # Encontrar contornos en la imagen umbralizada
    contours_mog2, _ = cv2.findContours(thresh_mog2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_knn, _ = cv2.findContours(thresh_knn, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar los contornos en el cuadro original
    frame_mog2 = frame.copy()
    frame_knn = frame.copy()

    for contour in contours_mog2:
        if cv2.contourArea(contour) > 500:  # Filtrar por área mínima para evitar ruido
            cv2.drawContours(frame_mog2, [contour], -1, (0, 255, 0), 2)  # Dibuja contornos en verde

    for contour in contours_knn:
        if cv2.contourArea(contour) > 500:  # Filtrar por área mínima para evitar ruido
            cv2.drawContours(frame_knn, [contour], -1, (0, 255, 0), 2)  # Dibuja contornos en verde

    # Concatenar los resultados de MOG2 y KNN
    combined_frame = np.hstack((frame_mog2, frame_knn))

    # Mostrar el resultado
    cv2.imshow('Contornos de Objetos en Movimiento', combined_frame)
    
    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar el video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
