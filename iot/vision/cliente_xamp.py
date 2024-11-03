import asyncio
import websockets
import json

async def send_data():
    async with websockets.connect('ws://localhost:6789') as websocket:
        data = {
            'Fibomassi': 1.23,
            'ErrorFibomassi': 0.1,
            'Error': 0.05,
            'RGB': '#FF0000',
            'NFibomassi': 42
        }
        await websocket.send(json.dumps(data))
        print('Datos enviados:', data)

# Ejecutar el cliente WebSocket
asyncio.run(send_data())
