import cv2
import numpy as np

# Cargar video
cap = cv2.VideoCapture('video1.mp4')

# Estado para las secuencias
sequence_stage = 0
frames_per_stage = 100  # Cantidad de cuadros que muestra cada etapa

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Cambiar el procesamiento de acuerdo con la etapa de secuencia
    if sequence_stage == 0:
        # Etapa 1: Mostrar video original
        cv2.imshow('Video', frame)

    elif sequence_stage == 1:
        # Etapa 2: Redimensionar el video
        resized_frame = cv2.resize(frame, (400, 600))
        cv2.imshow('Resized', resized_frame)

    elif sequence_stage == 2:
        # Etapa 3: Detectar bordes
        edges = cv2.Canny(frame, 100, 200)
        cv2.imshow('Edge', edges)

    elif sequence_stage == 3:
        # Etapa 4: Mostrar ambas mitades (izquierda y derecha) con margen
        height, width = frame.shape[:2]
        left_half = frame[:, :width // 2]  # Mitad izquierda
        right_half = frame[:, width // 2:]  # Mitad derecha

        # Crear un margen vertical entre las mitades
        margin_color = (0, 0, 0)  # Negro para el margen
        margin_width = 10
        vertical_margin = np.full((height, margin_width, 3), margin_color, dtype=np.uint8)

        # Combinar ambas mitades con el margen en el centro
        combined_frame_halves = np.concatenate((left_half, vertical_margin, right_half), axis=1)
        cv2.imshow('Left and Right Halves', combined_frame_halves)

    elif sequence_stage == 4:
        # Etapa 5: Mostrar todos los cuadrantes con etiquetas y márgenes
        height, width = frame.shape[:2]
        top_left = frame[:height // 2, :width // 2]
        top_right = frame[:height // 2, width // 2:]
        bottom_left = frame[height // 2:, :width // 2]
        bottom_right = frame[height // 2:, width // 2:]

        # Agregar etiquetas a cada cuadrante
        cv2.putText(top_left, 'Top Left', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(top_right, 'Top Right', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(bottom_left, 'Bottom Left', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(bottom_right, 'Bottom Right', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Crear márgenes entre cuadrantes
        vertical_margin = np.full((height // 2, margin_width, 3), margin_color, dtype=np.uint8)
        horizontal_margin = np.full((margin_width, width // 2 * 2 + margin_width, 3), margin_color, dtype=np.uint8)

        # Concatenar cuadrantes con márgenes
        top = np.concatenate((top_left, vertical_margin, top_right), axis=1)
        bottom = np.concatenate((bottom_left, vertical_margin, bottom_right), axis=1)
        combined_frame = np.concatenate((top, horizontal_margin, bottom), axis=0)

        # Mostrar imagen combinada con márgenes y etiquetas
        cv2.imshow('Quadrants', combined_frame)

    # Cambiar de etapa después de ciertos cuadros
    if cap.get(cv2.CAP_PROP_POS_FRAMES) % frames_per_stage == 0:
        sequence_stage = (sequence_stage + 1) % 5  # Regresa a la etapa 0 tras la última etapa
        cv2.destroyAllWindows()  # Cerrar todas las ventanas para evitar superposiciones

    # Terminar al presionar 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()