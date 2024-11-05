import asyncio
import websockets

async def send_messages():
    async with websockets.connect('ws://192.168.0.67:8080') as websocket:
        while True:
            message = input("Escribe un mensaje para enviar al servidor (o 'salir' para cerrar): ")
            if message.lower() == 'salir':
                break
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Respuesta del servidor: {response}")

asyncio.run(send_messages())
