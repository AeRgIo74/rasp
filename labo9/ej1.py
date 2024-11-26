import cv2
import numpy as np

# Ruta del video
video_path = 'bouncing.mp4'

# Cargar el video
cap = cv2.VideoCapture(video_path)

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
    kernel = np.ones((5, 5), np.uint8)  # Kernel de 5x5
    # Aplicar la operación de apertura
    opened_image = cv2.morphologyEx(frame_gray, cv2.MORPH_OPEN, kernel)
    
    # Definir el tamaño del kernel
    kernel_size = (5, 5)  # Tamaño del kernel (5x5)

    # Aplicar el filtro de desenfoque promedio
    mean_blurred_image = cv2.blur(opened_image, kernel_size)

    # Aplicar CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # Crear objeto CLAHE
    clahe_image = clahe.apply(mean_blurred_image)  # Aplicar CLAHE a la imagen abierta
    
    # Aplicar los sustractores de fondo
    mog2_mask = mog2_subtractor.apply(clahe_image)
    knn_mask = knn_subtractor.apply(clahe_image)
    
    # Redimensionar las máscaras para que coincidan con el tamaño de 'frame'
    mog2_mask_resized = cv2.resize(mog2_mask, (frame.shape[1], frame.shape[0]))
    knn_mask_resized = cv2.resize(knn_mask, (frame.shape[1], frame.shape[0]))

    # Crear una imagen de fondo negro
    black_background = np.zeros_like(frame)

    # Aplicar la máscara sobre el frame original
    colored_objects_mog2 = cv2.bitwise_and(frame, frame, mask=mog2_mask_resized)
    colored_objects_knn = cv2.bitwise_and(frame, frame, mask=knn_mask_resized)

    # Superponer los objetos detectados en color sobre el fondo negro
    result_mog2 = cv2.add(black_background, colored_objects_mog2)
    result_knn = cv2.add(black_background, colored_objects_knn)
    
    # Concatenar las imágenes horizontalmente
    combined = np.hstack((frame, cv2.cvtColor(mog2_mask_resized, cv2.COLOR_GRAY2BGR), cv2.cvtColor(knn_mask_resized, cv2.COLOR_GRAY2BGR),result_mog2,result_knn))
    
    # Mostrar los resultados en la ventana ya creada
    cv2.imshow('Comparación de Sustractores', combined)
    
    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar el video y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
