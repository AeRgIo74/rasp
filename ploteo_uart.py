import serial
from time import sleep

try:
    # Inicializa la comunicación serial
    ser = serial.Serial(
        port='/dev/ttyACM0',  # Asegúrate de que este sea el puerto correcto
        baudrate=115200,
        timeout=1
    )
    
    print("Esperando datos en el puerto serial...")
    while True:
        # Lee una línea de datos del puerto serial
        data = ser.readline()  # Lee hasta un salto de línea
        if data:  # Si hay datos recibidos
            # Decodifica los datos y quita los caracteres de nueva línea
            print(f"Datos recibidos: {data.decode('utf-8').strip()}")

        sleep(0.5)  # Pausa de 1 segundo entre lecturas

except serial.SerialException as e:
    print(f"Error en la comunicación serial: {e}")
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    ser.close()  # Asegúrate de cerrar el puerto al final
    print("Conexión serial cerrada.")
