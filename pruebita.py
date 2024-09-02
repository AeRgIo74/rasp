import RPi.GPIO as GPIO
import time

# Configurar la numeración de pines
GPIO.setmode(GPIO.BCM)

# Definir el pin al que está conectado el LED
LED_PIN = 17

# Configurar el pin del LED como salida
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        # Encender el LED
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("Hola Mundo: LED encendido")
        time.sleep(1)  # Esperar 1 segundo

        # Apagar el LED
        GPIO.output(LED_PIN, GPIO.LOW)
        print("Hola Mundo: LED apagado")
        time.sleep(1)  # Esperar 1 segundo

except KeyboardInterrupt:
    # Limpiar la configuración de los pines al salir
    GPIO.cleanup()
