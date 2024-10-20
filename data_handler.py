import math
import serial
import smtplib
from datetime import datetime
from time import sleep  # Asegúrate de importar la función sleep

class FileHandler:
    def __init__(self, filename):
        """Inicializa el manejador de archivos con el nombre de archivo dado."""
        self.filename = filename
        self.file = None

    def open_file(self, mode='a'):
        """Abre el archivo en el modo especificado (por defecto, anexar)."""
        try:
            self.file = open(self.filename, mode)  # Modo 'a' para agregar contenido
        except IOError as e:
            print(f"Error al abrir el archivo: {e}")

    def write_to_file(self, content):
        """Escribe contenido en el archivo junto con la fecha y hora actual."""
        if self.file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                self.file.write(f"{timestamp} - {content}\n")
            except IOError as e:
                print(f"Error al escribir en el archivo: {e}")
        else:
            print("Error: El archivo no está abierto.")

    def read_file(self):
        """Lee el contenido del archivo y lo devuelve como una cadena de texto."""
        try:
            with open(self.filename, 'r') as f:
                return f.read()
        except IOError as e:
            print(f"Error al leer el archivo: {e}")
            return ""

    def clear_file(self):
        """Limpia el contenido del archivo."""
        try:
            with open(self.filename, 'w') as f:
                f.write("")  # Escribe una cadena vacía para borrar el contenido
        except IOError as e:
            print(f"Error al limpiar el archivo: {e}")

    def close_file(self):
        """Cierra el archivo."""
        if self.file:
            try:
                self.file.close()
                self.file = None
            except IOError as e:
                print(f"Error al cerrar el archivo: {e}")

# Configuración del puerto serial
puerto = '/dev/rfcomm0'
baudrate = 9600  # Baud rate del HC-06 (por defecto es 9600)

# Inicializa la variable para almacenar la última dirección
ultima_direccion = None
file_handler = FileHandler('mi_archivo.txt')

# Inicializa la sesión SMTP
try:
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("lipaleyla9@gmail.com", "smkz cmbr tjuq taiu")  
except smtplib.SMTPException as e:
    print(f"Error al configurar SMTP: {e}")

def data_run():
    global ultima_direccion  # Declarar ultima_direccion como global
    # Abrir el puerto serial
    try:
        ser = serial.Serial(puerto, baudrate, timeout=1)
        print(f"Conectado al puerto {puerto} con baudrate {baudrate}")
        ser.write(f"auto\n".encode('utf-8'))
        while True:
            # Abre el archivo para escritura en cada ciclo
            file_handler.open_file()

            # Leer datos recibidos
            if ser.in_waiting > 0:
                datos = ser.readline().decode('utf-8').strip()
                print(f"Datos recibidos: {datos}")

                # Verifica si la dirección ha cambiado
                if datos != ultima_direccion:
                    file_handler.write_to_file(datos)  # Escribe los datos recibidos en el archivo
                    print(f"Dirección cambiada a: {datos}, escribiendo en archivo")
                    ultima_direccion = datos  # Actualiza la última dirección

                # Si el mensaje recibido es "alerta", envía el correo
                if datos == "alerta":
                    print("Alerta recibida, enviando correo...")
                    try:
                        # Leer el contenido del archivo
                        contenido_archivo = file_handler.read_file()

                        # Crear el mensaje de alerta con el contenido del archivo
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        message = f"""\
Subject: Alerta del Sistema

El sistema se detuvo en la fecha y hora: {current_time}
Historial de movimientos:
{contenido_archivo}
"""

                        # Enviar el correo
                        s.sendmail("lipaleyla9@gmail.com", "lipaleyla9@gmail.com", message)
                        print("Correo de alerta enviado")

                        # Limpiar el archivo después de enviar el correo
                        file_handler.clear_file()
                        print("Contenido del archivo limpiado")
                    except smtplib.SMTPException as e:
                        print(f"Error al enviar el correo: {e}")

            # Determinar la dirección (puedes ajustar la lógica aquí si es necesario)
            direccion = "quieto"  # Ejemplo estático, puedes modificar esto según tus necesidades

            # Enviar la dirección y el duty cycle por separado
            ser.write(f"{direccion}\n".encode('utf-8'))
            print(f"Enviado: {direccion}")

            sleep(0.1)  # Pausa antes del siguiente ciclo
            file_handler.close_file()

    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario")
    finally:
        file_handler.close_file()
        if 'ser' in locals() and ser.is_open:
            ser.close()
        print("Puerto serial cerrado")

data_run()
