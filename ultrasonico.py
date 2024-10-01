import serial
from gpiozero import DistanceSensor
from time import sleep

# Inicializa el sensor de distancia
sensor = DistanceSensor(echo=24, trigger=23)  # Ajusta los pines según tu configuración

try:
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=1
    )
    while True:
        distancia = sensor.distance * 100  # La distancia se da en metros, multiplicamos por 100 para convertir a cm
        print(f"Distancia: {distancia:.2f} cm")
        sleep(1)  # Pausa de 1 segundo entre lecturas
        # Envía el valor del tiempo al puerto serial
        ser.write(f'{distancia}\n'.encode())


except serial.SerialException as e:
    print(f"Error en la comunicación serial: {e}")
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    ser.close()
    print("Conexión serial cerrada.")
