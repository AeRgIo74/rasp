import asyncio
import websockets
import json

async def send_data():
    async with websockets.connect('ws://192.168.0.67:8080') as websocket:
        # Ingresar datos por terminal
        fibomassi = float(input("Ingrese el valor de Fibomassi: "))
        error_fibomassi = float(input("Ingrese el valor de ErrorFibomassi: "))
        error = float(input("Ingrese el valor de Error: "))
        rgb = input("Ingrese el valor de RGB (ejemplo: #FF0000): ")
        n_fibomassi = int(input("Ingrese el valor de NFibomassi: "))

        data = {
            'Fibomassi': fibomassi,
            'ErrorFibomassi': error_fibomassi,
            'Error': error,
            'RGB': rgb,
            'NFibomassi': n_fibomassi
        }
        
        await websocket.send(json.dumps(data))
        print('Datos enviados:', data)

# Ejecutar el cliente WebSocket
asyncio.run(send_data())
