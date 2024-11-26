import cv2
import numpy as np

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

    # Definir el kernel para la operación de apertura
    kernel = np.ones((5, 5), np.uint8)
    opened_image = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, kernel)

    # Aplicar el filtro de desenfoque promedio
    mean_blurred_image = cv2.blur(opened_image, (5, 5))

    # Aplicar CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(mean_blurred_image)

    # Aplicar los sustractores de fondo
    mog2_mask = mog2_subtractor.apply(clahe_image)
    knn_mask = knn_subtractor.apply(clahe_image)

    # Aplicar la máscara sobre el frame original
    colored_objects_mog2 = cv2.bitwise_and(frame, frame, mask=mog2_mask)
    colored_objects_knn = cv2.bitwise_and(frame, frame, mask=knn_mask)

    # Detectar el objeto en el centro de la pantalla
    height, width = mog2_mask.shape
    center_x, center_y = width // 2, height // 2
    object_detected = False

    # Revisar si hay un objeto en el centro de la imagen
    if knn_mask[center_y - 50:center_y + 50, center_x - 50:center_x + 50].any():
        object_detected = True
        cv2.putText(frame, "Objeto detectado", (width - 200, height - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Concatenar las imágenes en dos filas
    top_row = np.hstack((frame, cv2.cvtColor(mog2_mask, cv2.COLOR_GRAY2BGR), cv2.cvtColor(knn_mask, cv2.COLOR_GRAY2BGR)))
    bottom_row = np.hstack((frame, colored_objects_mog2, colored_objects_knn))
    combined = np.vstack((top_row, bottom_row))

    # Mostrar los resultados en la ventana ya creada
    cv2.imshow('Comparación de Sustractores', combined)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar el video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
