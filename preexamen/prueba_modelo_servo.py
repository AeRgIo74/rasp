import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from gpiozero import Servo
from time import sleep
import threading

# Deshabilitar el uso de la GPU
tf.config.set_visible_devices([], 'GPU')

# Cargar el modelo entrenado (aseg�rate de tener el archivo .h5)
model = load_model('modelo_entrenado_100.h5')

# Inicializar la webcam (0 es generalmente la c�mara predeterminada)
cap = cv2.VideoCapture(0)

# Aseg�rate de que la c�mara se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se puede acceder a la c�mara.")
    exit()

# Nombres de las categor�as (ajusta seg�n tu caso)
category_names = ['category_Aika', 'category_Simba', 'category_Suzuka', 'category_Tsuki']

# Configuraci�n del servomotor usando gpiozero
servo = Servo(17)  # Usa el pin GPIO 17 para el servomotor

# Funci�n para activar el servomotor seg�n la raza del gato
def activate_servo(cat_name):
    if cat_name == 'category_Aika' or cat_name == 'category_Suzuka':
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

# Funci�n en un hilo para manejar el servo sin bloquear
def servo_thread(cat_name):
    thread = threading.Thread(target=activate_servo, args=(cat_name,))
    thread.start()

# Bucle principal
while True:
    # Capturar el frame de la webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    # Obtener las dimensiones del frame de la c�mara
    frame_height, frame_width = frame.shape[:2]

    # Convertir la imagen a escala de grises
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
    img_gray = clahe.apply(img_gray)

    # Redimensionar la imagen a 100x100 (si tu modelo espera esta forma)
    img_resized = cv2.resize(img_gray, (100, 100))

    # Normalizar la imagen
    img_array = np.array(img_resized) / 255.0  # Normalizaci�n entre 0 y 1

    # A�adir una dimensi�n adicional para que tenga la forma (1, 100, 100, 1)
    img_array = img_array.reshape(1, 100, 100, 1)

    # Hacer la predicci�n con el modelo
    predictions = model.predict(img_array)

    # Bounding box y categor�a predicha
    predicted_bbox = predictions[0][0]  # Caja delimitadora predicha [x, y, w, h]
    predicted_category_idx = np.argmax(predictions[1][0])  # �ndice de la categor�a predicha
    predicted_category_name = category_names[predicted_category_idx]

    # Escalar las coordenadas de la bounding box al tama�o del frame
    x = int(predicted_bbox[0] * frame_width / 100)  
    y = int(predicted_bbox[1] * frame_height / 100)
    w = int(predicted_bbox[2] * frame_width / 100)
    h = int(predicted_bbox[3] * frame_height / 100)

    # Mostrar la categor�a en la imagen
    cv2.putText(frame, f'Predicci�n: {predicted_category_name}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Dibujar la bounding box sobre la imagen
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Activar el servomotor en un hilo separado
    servo_thread(predicted_category_name)

    # Mostrar el frame con la predicci�n y la bounding box
    cv2.imshow('Webcam', frame)

    # Si presionas la tecla 'q', el bucle se detendr�
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la c�mara y cerrar todas las ventanas cuando termine
cap.release()
cv2.destroyAllWindows()
