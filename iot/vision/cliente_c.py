import asyncio
import websockets
import json
import random
import cv2
from gpiozero import Button, RGBLED
from signal import pause
import time
from datetime import datetime
import base64

# Configuración del LED RGB y el botón (ajusta los pines según tu conexión)
led = RGBLED(red=17, green=27, blue=22)  # Cambia estos pines según tu conexión
button = Button(2)  # Cambia el número de pin según tu configuración

# Variable para controlar el envío de datos
sending_data = True

# Inicializar la cámara
camera = cv2.VideoCapture(0)

async def send_data(data):
    async with websockets.connect('ws://192.168.0.67:8080') as websocket:
        await websocket.send(json.dumps(data))
        #print('Datos enviados:', data)

def generate_data():
    now = datetime.now()
    Tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
    aire = random.uniform(0, 10)
    Ultasonico = random.uniform(0, 1)
    Temperatura = random.uniform(0, 0.5)
    Humedad = random.randint(0, 2)

    # Generar un color RGB aleatorio
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    led.color = (r / 255, g / 255, b / 255)

    return {
        'Tiempo': Tiempo,
        'aire': aire,
        'Ultrasonico': Ultasonico,
        'Temperatura': Temperatura,
        'Humedad': Humedad,
        'Color': f'#{r:02X}{g:02X}{b:02X}'
    }

def capture_image():
    success, frame = camera.read()
    if success:
        _, buffer = cv2.imencode('.jpg', frame)
        frame_b64 = base64.b64encode(buffer).decode('utf-8')
        return frame_b64
    else:
        return None

def on_button_press():
    global sending_data
    sending_data = False  # Detener el envío de datos

async def main():
    global sending_data
    button.when_pressed = on_button_press

    while sending_data:
        data = generate_data()  # Genera datos aleatorios de sensores
        image = capture_image()  # Captura una imagen de la cámara

        if image is not None:
            data['image'] = image  # Añade la imagen capturada a los datos

        await send_data(data)  # Enviar datos y la imagen a través de WebSocket

    print("Envío de datos detenido.")
    camera.release()  # Liberar la cámara al terminar

# Ejecutar el cliente WebSocket
asyncio.run(main())