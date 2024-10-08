from gpiozero import MCP3008, Button
from time import sleep
import math
import serial
import time
import smtplib
from datetime import datetime

# Crea una sesión SMTP
s = smtplib.SMTP('smtp.gmail.com', 587)

# Inicia TLS para seguridad
s.starttls()


s.login("lipaleyla9@gmail.com", "smkz cmbr tjuq taiu")  

# Obtener fecha y hora actual
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Mensaje, fecha y hora
message = f"""\
Subject: Alerta del Sistema

El sistema se detuvo en la fecha y hora: {current_time}
Mensaje personalizado: El sistema ha dejado de funcionar inesperadamente. Por favor, revisa el estado."""  

# Configura el botón del joystick (SW) en el GPIO 25
button = Button(25)

# Inicializa el contador
contador = 0

# Función de interrupción que incrementa el contador y lo reinicia a 0 si pasa de 2
def incrementar_contador():
    global contador
    contador += 1
    if contador > 2:
        contador = 0
    print(f"Contador: {contador}")

# Asocia la función de interrupción al evento de presionar el botón
button.when_pressed = incrementar_contador

# Inicializa el MCP3008 en los canales CH0 y CH1 para los ejes X y Y del joystick
x_axis = MCP3008(channel=0)  # VRx conectado a CH0
y_axis = MCP3008(channel=1)  # VRy conectado a CH1

# Función map personalizada
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# Inicializa la variable dirección
direccion = ""

# Configuración del puerto serial
puerto = '/dev/rfcomm0'
baudrate = 9600  # Baud rate del HC-06 (por defecto es 9600)

try:
    # Abrir el puerto serial
    ser = serial.Serial(puerto, baudrate, timeout=1)
    print(f"Conectado al puerto {puerto} con baudrate {baudrate}")

    while True:
        # Leer datos recibidos
        if ser.in_waiting > 0:
            datos = ser.readline().decode('utf-8').strip()
            print(f"Datos recibidos: {datos}")
            # Si el mensaje recibido es "alerta", envía el correo
            if datos == "alerta":
                print("Alerta recibida, enviando correo...")
                s.sendmail("lipaleyla9@gmail.com", "lipaleyla9@gmail.com", message)
                print("Correo de alerta enviado")

        # Lee los valores de los ejes X y Y
        x_value = x_axis.value  # El valor está entre 0.0 y 1.0
        y_value = y_axis.value  # El valor está entre 0.0 y 1.0

        # Mapea los valores de 0.0 - 1.0 a -99 - 99
        x_mapped = map_value(x_value, 0.0, 1.0, -99, 99)
        y_mapped = map_value(y_value, 0.0, 1.0, -99, 99)

        # Calcula el dutycycle utilizando Pitágoras
        dutycycle = math.sqrt(x_mapped**2 + y_mapped**2)

        # Asegura que el dutycycle no exceda 99 y conviértelo en entero
        if dutycycle > 99:
            dutycycle = 99
        dutycycle = int(dutycycle)

        # Evalúa las direcciones y envía si contador es 0, 1 o 2
        if contador == 0 or contador == 1 or contador == 2:
            # Condicionales para la dirección basada en el eje Y y X
            if contador == 0:
                # Modo de dirección normal
                if y_mapped >= 10:
                    direccion = "adelante"
                elif y_mapped <= -10:
                    direccion = "atras"
                elif x_mapped >= 10:
                    direccion = "derecha"
                elif x_mapped <= -10:
                    direccion = "izquierda"
                elif -10 < y_mapped < 10 and -10 < x_mapped < 10:
                    direccion = "quieto"  # Cuando el joystick está en el centro o no se mueve mucho

            elif contador == 1:
                # Modo omnidireccional
                if y_mapped >= 10 and -10 < x_mapped < 10:
                    direccion = "adelante"
                elif y_mapped <= -10 and -10 < x_mapped < 10:
                    direccion = "atras"
                elif x_mapped >= 10 and -10 < y_mapped < 10:
                    direccion = "dder"
                elif x_mapped <= -10 and -10 < y_mapped < 10:
                    direccion = "iizq"
                elif x_mapped >= -10 and y_mapped >= 10:
                    direccion = "ader"  # Adelante derecho
                elif x_mapped <= -10 and y_mapped >= 10:
                    direccion = "aizq"  # Adelante izquierdo
                elif x_mapped >= 10 and y_mapped <= -10:
                    direccion = "bder"  # Atrás derecho
                elif x_mapped <= -10 and y_mapped <= -10:
                    direccion = "bizq"  # Atrás izquierdo
                else:
                    direccion = "quieto"  # Cuando el joystick está en el centro o no se mueve mucho

            elif contador == 2:
                # Modo adicional para girar
                if x_mapped >= 10 and -10 < y_mapped < 10:
                    direccion = "gder"
                elif x_mapped <= -10 and -10 < y_mapped < 10:
                    direccion = "gizq"
                else:
                    direccion = "quieto"  # Cuando el joystick está en el centro o no se mueve mucho

            # Imprime los valores mapeados, la dirección y el dutycycle
            print(f"X: {x_mapped:.2f}, Y: {y_mapped:.2f}, Dirección: {direccion}, Dutycycle: {dutycycle}")

            # Enviar la dirección y el duty cycle por separado
            ser.write(f"{direccion}\n".encode('utf-8'))  # Enviar dirección
            print(f"Enviado: {direccion.strip()}")
            ser.write(f"{abs(dutycycle)}\n".encode('utf-8'))  # Enviar duty cycle
            print(f"Enviado: {dutycycle}")

            sleep(0.1)  # Esperar un segundo antes de enviar nuevamente

except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
except KeyboardInterrupt:
    print("Programa interrumpido")

finally:
    # Cerrar el puerto serial al finalizar si está abierto
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Puerto serial cerrado")
