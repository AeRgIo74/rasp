import serial
from gpiozero import LED
from time import sleep

# Configurar el puerto UART en la Raspberry Pi
ser = serial.Serial(
    port='/dev/serial0',   # Puerto UART de la Raspberry Pi
    baudrate=115200,       # Velocidad de transmisión
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Configurar el LED en un pin GPIO (ajusta según tu conexión)
led = LED(17)  # Por ejemplo, usa el pin GPIO 17

print("Esperando datos de UART...")

try:
    while True:
        if ser.in_waiting > 0:
            # Leer el mensaje desde UART
            mensaje = ser.readline().decode('utf-8').rstrip()
            print(f"Mensaje recibido: {mensaje}")
            
            # Encender el LED con "hola" y apagar con "mundo"
            if mensaje == "hola":
                led.on()
                print("LED encendido")
            elif mensaje == "mundo":
                led.off()
                print("LED apagado")

        sleep(0.1)  # Pequeña espera para evitar uso intensivo de CPU

except KeyboardInterrupt:
    print("Terminando el programa...")
finally:
    ser.close()
