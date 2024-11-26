import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from gpiozero import Servo
from time import sleep
import threading
from sort.sort import Sort  # Implementaci�n de SORT

# Deshabilitar el uso de la GPU
tf.config.set_visible_devices([], 'GPU')

# Cargar el modelo entrenado
model = load_model('modelo_entrenado.h5')

# Inicializar la webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se puede acceder a la c�mara.")
    exit()

# Nombres de las categor�as
category_names = ['category_Aika', 'category_Simba', 'category_Suzuka', 'category_Tsuki']

# Configuraci�n del servomotor
servo = Servo(17)

# Instanciar el rastreador SORT
tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)

# Funci�n para activar el servo
def activate_servo(cat_name):
    if cat_name in ['category_Aika', 'category_Suzuka']:
        servo.value = 1
        sleep(1)
        servo.value = 0
    elif cat_name == 'category_Tsuki':
        servo.value = 1
        sleep(2)
        servo.value = 0
    elif cat_name == 'category_Simba':
        servo.value = 1
        sleep(0.5)
        servo.value = 0

# Funci�n en un hilo para el servo
def servo_thread(cat_name):
    thread = threading.Thread(target=activate_servo, args=(cat_name,))
    thread.start()

# Crear el conjunto para almacenar IDs rastreados
tracked_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    frame_height, frame_width = frame.shape[:2]

    # Convertir la imagen a escala de grises y preprocesar
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
    img_gray = clahe.apply(img_gray)
    img_resized = cv2.resize(img_gray, (50, 50))
    img_array = np.array(img_resized) / 255.0
    img_array = img_array.reshape(1, 50, 50, 1)

    # Realizar la predicci�n
    predictions = model.predict(img_array)
    predicted_bbox = predictions[0][0]  # [x, y, w, h]
    predicted_category_idx = np.argmax(predictions[1][0])
    predicted_category_prob = predictions[1][0][predicted_category_idx]
    predicted_category_name = category_names[predicted_category_idx]

    # Solo proceder si la probabilidad es >= 60%
    if predicted_category_prob >= 0.6:
        # Escalar las coordenadas de la bounding box al tama�o del frame
        x = int(predicted_bbox[0] * frame_width / 50)
        y = int(predicted_bbox[1] * frame_height / 50)
        w = int(predicted_bbox[2] * frame_width / 50)
        h = int(predicted_bbox[3] * frame_height / 50)
        bbox = [x, y, x + w, y + h]  # Formato [xmin, ymin, xmax, ymax]

        # Alimentar la detecci�n al rastreador SORT
        detections = np.array([[x, y, x + w, y + h, 1.0]])  # A�adir una puntuaci�n de confianza
        tracks = tracker.update(detections)

        for track in tracks:
            track_id = int(track[4])  # ID �nico del objeto rastreado
            xmin, ymin, xmax, ymax = map(int, track[:4])

            # Dibujar la bounding box y el ID del objeto
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.putText(frame, f'ID {track_id}: {predicted_category_name} ({predicted_category_prob:.2f})',
                        (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Solo activar el servo si el objeto es nuevo
            if track_id not in tracked_ids:
                servo_thread(predicted_category_name)
                tracked_ids.add(track_id)  # A�adir a los objetos rastreados
    else:
        print(f"Categor�a {predicted_category_name} descartada por baja probabilidad ({predicted_category_prob:.2f})")

    # Mostrar el frame
    cv2.imshow('Webcam', frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
