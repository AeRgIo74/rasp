import serial
import time

def leer_configuracion():
    tiempo = 1  # Valor por defecto
    try:
        with open('/home/AeRgIo/Downloads/rasp/labo 5/timer.txt', 'r') as f:
            for line in f:
                if line.startswith('tiempo='):
                    tiempo = int(line.split('=')[1])
                    break
    except FileNotFoundError:
        print("El archivo timer.txt no se encontró. Usando valores por defecto.")
    except ValueError:
        print("Error al convertir el valor de tiempo. Usando el valor por defecto.")
    
    return tiempo

try:
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=1
    )
    
    while True:
        tiempo = leer_configuracion()
        print(f"Tiempo leído: {tiempo} segundos")

        # Envía el valor del tiempo al puerto serial
        ser.write(f'{tiempo}\n'.encode())

        # Espera por una respuesta del puerto serial
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Datos recibidos: {line}")

        # Pausa por el valor de tiempo leído
        time.sleep(tiempo)

except serial.SerialException as e:
    print(f"Error en la comunicación serial: {e}")
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    ser.close()
    print("Conexión serial cerrada.")
