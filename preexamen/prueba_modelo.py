import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Deshabilitar el uso de la GPU
tf.config.set_visible_devices([], 'GPU')

# Cargar el modelo entrenado (asegúrate de tener el archivo .h5)
model = load_model('modelo_entrenado_100.h5')

# Inicializar la webcam (0 es generalmente la cámara predeterminada)
cap = cv2.VideoCapture(0)

# Asegúrate de que la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

# Nombres de las categorías (ajusta según tu caso)
category_names = ['category_Aika', 'category_Simba', 'category_Suzuka', 'category_Tsuki']

while True:
    # Capturar el frame de la webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo leer el frame.")
        break

    # Obtener las dimensiones del frame de la cámara
    frame_height, frame_width = frame.shape[:2]

    # Convertir la imagen a escala de grises
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(4, 4))
    img_gray = clahe.apply(img_gray)

    # Redimensionar la imagen a 50x50 (si tu modelo espera esta forma)
    img_resized = cv2.resize(img_gray, (100, 100))

    # Normalizar la imagen
    img_array = np.array(img_resized) / 255.0  # Normalización entre 0 y 1

    # Añadir una dimensión adicional para que tenga la forma (1, 50, 50, 1)
    img_array = img_array.reshape(1, 100, 100, 1)

    # Hacer la predicción con el modelo
    predictions = model.predict(img_array)
    print(predictions)

    # Bounding box y categoría predicha
    predicted_bbox = predictions[0][0]  # Caja delimitadora predicha [x, y, w, h]
    predicted_category_idx = np.argmax(predictions[1][0])  # Índice de la categoría predicha
    predicted_category_name = category_names[predicted_category_idx]

    # Extraer las coordenadas de la bounding box
    x, y, w, h = predicted_bbox.astype(int)  # Convertir a enteros para las coordenadas y dimensiones

    # Escalar las coordenadas de la bounding box al tamaño del frame
    x = int(x * frame_width / 100)  # Escalar x
    y = int(y * frame_height / 100)  # Escalar y
    w = int(w * frame_width / 100)   # Escalar w
    h = int(h * frame_height / 100)  # Escalar h

    # Mostrar la categoría en la imagen
    cv2.putText(frame, f'Predicción: {predicted_category_name}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Dibujar la bounding box sobre la imagen
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dibuja un rectángulo (color verde, grosor 2)

    # Mostrar el frame con la predicción y la bounding box
    cv2.imshow('Webcam', frame)

    # Si presionas la tecla 'q', el bucle se detendrá
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas cuando termine
cap.release()
cv2.destroyAllWindows()
