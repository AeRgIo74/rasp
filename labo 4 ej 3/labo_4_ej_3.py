from gpiozero import LED
import time

# Configuración de los pines para los 4 LEDs
leds = [LED(21), LED(20), LED(16), LED(12)]  # Cambia los pines según tu configuración

def leer_configuracion():
    # Lee el archivo config.txt para obtener el valor del delay
    with open('/home/AeRgIo/Downloads/rasp/labo 4 ej 3/delay_ej_3.txt', 'r') as f:
        for line in f:
            if line.startswith('delay='):
                return float(line.split('=')[1])
    return 0.5  # Valor por defecto si no se encuentra el archivo

def mostrar_binario_simple(valor):
    # Usa operaciones bit a bit para encender y apagar los LEDs
    for i in range(4):  # Tenemos 4 LEDs
        if valor & (1 << i):  # Comprueba el bit i-ésimo de 'valor'
            leds[i].on()  # Enciende el LED si el bit es 1
        else:
            leds[i].off()  # Apaga el LED si el bit es 0

try:
    contador = 0  # Inicializa el contador
    while True:
        delay = leer_configuracion()  # Lee el intervalo de tiempo desde el archivo
        mostrar_binario_simple(contador)  # Muestra el contador binario en los LEDs
        time.sleep(delay)  # Espera antes de avanzar al siguiente número
        contador = (contador + 1) % 16  # Incrementa el contador y reinicia en 0 después de 15

except KeyboardInterrupt:
    print("Programa detenido.")

