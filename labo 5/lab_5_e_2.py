import serial
from signal import pause

def leer_configuracion():
    # Inicializa los valores de tiempo
    tiempo = 1  # Valor por defecto
    try:
        with open('/home/AeRgIo/Downloads/rasp/labo 5/timer.txt', 'r') as f:
            for line in f:
                if line.startswith('tiempo='):
                    tiempo = int(line.split('=')[1])
                    break  # Solo necesitas el primer valor de 'tiempo'
    except FileNotFoundError:
        print("El archivo timer.txt no se encontró. Usando valores por defecto.")
    except ValueError:
        print("Error al convertir el valor de tiempo. Usando el valor por defecto.")

    return tiempo

# Inicializa el puerto serie
ser = serial.Serial(
    port='/dev/ttyACM0',  # Ajusta esto según tu configuración
    baudrate=115200,
    timeout=1
)

try:
    while True:
        # Lee la configuración desde el archivo
        tiempo = leer_configuracion()
        print(f"Tiempo leído: {tiempo} segundos")

        # Envía el valor de 'tiempo' al puerto serie
        ser.write(f'{tiempo}\n'.encode())  # Envía el valor convertido a bytes

        # Lee los datos del puerto serie, si es necesario
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Datos recibidos: {line}")

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    ser.close()
    print("Conexión serial cerrada.")
