import asyncio
import websockets
import json
import random
from gpiozero import Button, RGBLED
from signal import pause
import time

# Configuración del LED RGB (ajusta los pines según tu conexión)
led = RGBLED(red=17, green=27, blue=22)  # Cambia estos pines según tu conexión
button = Button(2)  # Cambia el número de pin según tu configuración

# Variable para controlar el envío de datos
sending_data = True

async def send_data(data):
    async with websockets.connect('ws://192.168.0.67:8080') as websocket:
        await websocket.send(json.dumps(data))
        print('Datos enviados:', data)

def generate_data():
    # Generar valores aleatorios
    fibomassi = random.uniform(0, 10)
    error_fibomassi = random.uniform(0, 1)
    error = random.uniform(0, 0.5)
    n_fibomassi = random.randint(1, 100)

    # Generar un color RGB aleatorio
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    # Cambiar el color del LED
    led.color = (r / 255, g / 255, b / 255)  # Normaliza el valor a 0-1 para gpiozero

    # Convertir a formato hexadecimal
    rgb_color = f'#{r:02X}{g:02X}{b:02X}'  # Formato hexadecimal

    return {
        'Fibomassi': fibomassi,
        'ErrorFibomassi': error_fibomassi,
        'Error': error,
        'RGB': rgb_color,
        'NFibomassi': n_fibomassi
    }

def on_button_press():
    global sending_data
    sending_data = False  # Detener el envío de datos

async def main():
    global sending_data
    button.when_pressed = on_button_press  # Configura la interrupción para el botón

    while sending_data:
        data = generate_data()  # Genera datos aleatorios
        await send_data(data)  # Enviar datos a través de WebSocket
        await asyncio.sleep(1)  # Esperar 1 segundo antes de enviar nuevamente

    print("Envío de datos detenido.")

# Ejecutar el cliente WebSocket
asyncio.run(main())
