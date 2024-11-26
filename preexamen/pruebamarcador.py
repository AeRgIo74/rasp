import cv2
import tensorflow as tf
import numpy as np

# Diccionario para mapear el índice de la clase al nombre de la clase
class_names = {
    0: 'Almoadilla',
    1: 'Rojo',
    2: 'Negro',
    3: 'Azul'
}

# Cargar el modelo .h5
model = tf.keras.models.load_model('modelo_entrenado (1).h5')

# Predicción para una sola imagen
def predict(image):
    # Preprocesar la imagen
    image_resized = cv2.resize(image, (224, 224))  # Redimensionar a 224x224
    image_resized = np.array(image_resized, dtype=np.float32)  # Convertir a tipo float32
    image_resized = image_resized / 255.0  # Normalizar a [0, 1]
    image_resized = np.expand_dims(image_resized, axis=0)  # Añadir dimensión batch

    # Hacer predicción
    bbox_pred, class_pred = model.predict(image_resized)
    predicted_class = np.argmax(class_pred[0])  # Obtener el índice de la clase predicha

    # Extraer bounding box predicho
    predicted_bbox = bbox_pred[0]

    return predicted_bbox, predicted_class

# Función para dibujar la bounding box sobre el frame
def draw_bbox(frame, bbox, predicted_class):
    # Dibujar la bounding box en el frame
    x, y, w, h = bbox  # Coordenadas de la bounding box
    frame = cv2.resize(frame,(240,240))
    cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (0, 0, 255), 2)  # Caja roja

    # Mostrar el nombre de la clase predicha sobre la imagen
    predicted_class_name = class_names[predicted_class]
    cv2.putText(frame, f'Predicted: {predicted_class_name}', (int(x), int(y) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame

# Captura de video desde la webcam
cap = cv2.VideoCapture(2)

while True:
    # Capturar un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error al capturar el frame")
        break

    # Realizar predicción en el frame capturado
    bbox, predicted_class = predict(frame)

    # Dibujar la bounding box sobre el frame
    frame_with_bbox = draw_bbox(frame, bbox, predicted_class)

    # Mostrar el frame con la bounding box en tiempo real
    cv2.imshow("Video en Tiempo Real", frame_with_bbox)

    # Esperar por una tecla para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
