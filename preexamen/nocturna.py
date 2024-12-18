import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from gpiozero import Servo
from time import sleep
import threading
import serial
from sort.sort import Sort  # Implementación de SORT

# Configuración del puerto serie
PORT = '/dev/rfcomm0'  # Puerto UART
BAUDRATE = 9600       # Velocidad de comunicación UART

# Inicializar conexión serie
def init_serial():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"Conectado al puerto {PORT} a {BAUDRATE} baudios.")
        return ser
    except Exception as e:
        print(f"Error al conectar con el puerto serie: {e}")
        return None

# Deshabilitar el uso de la GPU
tf.config.set_visible_devices([], 'GPU')

# Cargar el modelo entrenado
model = load_model('modelo_entrenado.h5')

# Inicializar la webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

# Inicializar la conexión UART
ser = init_serial()

# Nombres de las categorías
category_names = ['category_Aika', 'category_Simba', 'category_Suzuka', 'category_Tsuki']

# Configuración del servomotor
servo = Servo(17)

# Instanciar el rastreador SORT
tracker = Sort(max_age=30, min_hits=3, iou_threshold=0.3)

# Función para activar el servo
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

# Función en un hilo para el servo
def servo_thread(cat_name):
    thread = threading.Thread(target=activate_servo, args=(cat_name,))
    thread.start()

# Crear el conjunto para almacenar IDs rastreados
tracked_ids = set()

# Bandera para alternar entre los modos
night_vision_mode = False
prediction_mode = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    # Dimensiones del frame
    frame_height, frame_width = frame.shape[:2]

    if night_vision_mode:
        # Modo de visión nocturna
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Ajustar brillo y contraste
        alpha = 2.0  # Contraste
        beta = 30    # Brillo
        enhanced_frame = cv2.convertScaleAbs(gray_frame, alpha=alpha, beta=beta)

        # Desenfoque para suavizar detalles
        blurred_frame = cv2.GaussianBlur(enhanced_frame, (7, 7), 0)

        # Agregar un mapa de color verde (visión nocturna típica)
        night_vision_frame = cv2.applyColorMap(blurred_frame, cv2.COLORMAP_SUMMER)

        # Mostrar el modo de visión nocturna
        cv2.imshow("Night Vision Mode", night_vision_frame)

    elif prediction_mode:
        # Convertir la imagen a escala de grises y preprocesar
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
        img_gray = clahe.apply(img_gray)
        img_resized = cv2.resize(img_gray, (50, 50))
        img_array = np.array(img_resized) / 255.0
        img_array = img_array.reshape(1, 50, 50, 1)

        # Realizar la predicción
        predictions = model.predict(img_array)
        predicted_bbox = predictions[0][0]  # [x, y, w, h]
        predicted_category_idx = np.argmax(predictions[1][0])
        predicted_category_prob = predictions[1][0][predicted_category_idx]
        predicted_category_name = category_names[predicted_category_idx]

        # Enviar el mensaje al módulo HC-05 si está conectado
        if ser and ser.is_open:
            mensaje_uart = "150"  # Comando a enviar
            ser.write(mensaje_uart.encode('utf-8'))
            print(f"Enviado al módulo HC-05: {mensaje_uart}")

        # Solo proceder si la probabilidad es >= 60%
        if predicted_category_prob >= 0.6:
            # Escalar las coordenadas de la bounding box al tamaño del frame
            x = int(predicted_bbox[0] * frame_width / 50)
            y = int(predicted_bbox[1] * frame_height / 50)
            w = int(predicted_bbox[2] * frame_width / 50)
            h = int(predicted_bbox[3] * frame_height / 50)
            bbox = [x, y, x + w, y + h]  # Formato [xmin, ymin, xmax, ymax]

            # Alimentar la detección al rastreador SORT
            detections = np.array([[x, y, x + w, y + h, 1.0]])  # Añadir una puntuación de confianza
            tracks = tracker.update(detections)

            for track in tracks:
                track_id = int(track[4])  # ID único del objeto rastreado
                xmin, ymin, xmax, ymax = map(int, track[:4])

                # Dibujar la bounding box y el ID del objeto
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                cv2.putText(frame, f'ID {track_id}: {predicted_category_name} ({predicted_category_prob:.2f})',
                            (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # Solo activar el servo si el objeto es nuevo
                if track_id not in tracked_ids:
                    servo_thread(predicted_category_name)
                    tracked_ids.add(track_id)  # Añadir a los objetos rastreados
        else:
            print(f"Categoría {predicted_category_name} descartada por baja probabilidad ({predicted_category_prob:.2f})")

        # Mostrar el frame con predicciones
        cv2.imshow('Prediction Mode', frame)

    else:
        # Mostrar el video normal
        cv2.imshow('Normal Mode', frame)

    # Escuchar teclas
    key = cv2.waitKey(1) & 0xFF
    if key == ord('v'):  # Alternar modo de visión nocturna
        night_vision_mode = not night_vision_mode
        prediction_mode = False
        print("Modo de visión nocturna:", night_vision_mode)
    elif key == ord('p'):  # Alternar modo de predicción
        prediction_mode = not prediction_mode
        night_vision_mode = False
        print("Modo de predicción:", prediction_mode)
    elif key == ord('q'):  # Salir
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()