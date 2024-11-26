import asyncio
import websockets
import serial
import time
import json

# Configuraci�n del puerto serie
PORT = '/dev/rfcomm0'  # Puerto UART
BAUDRATE = 9600       # Velocidad de comunicaci�n UART

# Inicializar conexi�n serie
def init_serial():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"Conectado al puerto {PORT} a {BAUDRATE} baudios.")
        return ser
    except Exception as e:
        print(f"Error al conectar con el puerto serie: {e}")
        return None

async def handle_websocket(ser):
    """
    Maneja la conexi�n WebSocket y env�a los mensajes recibidos al m�dulo HC-05.
    """
    uri = "ws://192.168.96.75:8080"  # Direcci�n del servidor WebSocket
    try:
        async with websockets.connect(uri) as websocket:
            print("Conectado al servidor WebSocket.")

            # Enviar mensaje inicial para identificarse
            await websocket.send(json.dumps({"role": "uart_client"}))
            print("Mensaje inicial enviado al servidor WebSocket.")

            # Escuchar mensajes del WebSocket
            async for message in websocket:
                try:
                    # Decodificar el mensaje recibido
                    data = json.loads(message)
                    print(f"Mensaje recibido del WebSocket: {data}")

                    # Enviar el mensaje al m�dulo HC-05
                    if ser and ser.is_open:
                        mensaje_uart = data.get("command")  # Obtener comando
                        ser.write(mensaje_uart.encode('utf-8'))
                        print(f"Enviado al m�dulo HC-05: {mensaje_uart}")
                        
                        # Leer respuesta del HC-05
                        if ser.in_waiting > 0:
                            respuesta = ser.readline().decode('utf-8').strip()
                            print(f"Respuesta del m�dulo HC-05: {respuesta}")

                except json.JSONDecodeError:
                    print("Error: mensaje recibido no es un JSON v�lido.")
    except Exception as e:
        print(f"Error en la conexi�n WebSocket: {e}")

async def main():
    """
    Inicializa el puerto serie y gestiona la conexi�n WebSocket.
    """
    ser = init_serial()  # Inicializar UART
    if not ser:
        print("No se pudo inicializar el puerto UART.")
        return

    # Iniciar el manejo de WebSocket
    await handle_websocket(ser)

    # Cerrar la conexi�n UART al finalizar
    if ser and ser.is_open:
        ser.close()
        print("Conexi�n UART cerrada.")

if __name__ == "__main__":
    asyncio.run(main())
