import serial

# Configuración del puerto serial
# Asegúrate de que /dev/rfcomm0 esté creado correctamente
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

except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
except KeyboardInterrupt:
    print("Programa interrumpido")

finally:
    # Cerrar el puerto serial al finalizar
    if ser.is_open:
        ser.close()
        print("Puerto serial cerrado")
