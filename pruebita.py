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
        GPIO.output(LED_PIN, GPIO.HIGH)  # Encender el LED
        time.sleep(1)  # Esperar 1 segundo
        GPIO.output(LED_PIN, GPIO.LOW)   # Apagar el LED
        time.sleep(1)  # Esperar 1 segundo

except KeyboardInterrupt:
    GPIO.cleanup()  # Limpiar los pines al salir
