from gpiozero import LED, Button
from time import sleep

# Inicializar los LEDs en los pines correspondientes
leds = [
    LED(17),  # LED 1 en el pin GPIO 17
    LED(27),  # LED 2 en el pin GPIO 27
    LED(22),  # LED 3 en el pin GPIO 22
    LED(23),  # LED 4 en el pin GPIO 23
]

# Inicializar los botones en los pines correspondientes
button_increment = Button(14, pull_up=True)  # Botón en GPIO 14 con pull-up
button_decrement = Button(15, pull_up=True)  # Botón en GPIO 15 con pull-up

contador = 0

def decimal_to_binary_array(num):
    binary_array = [0, 0, 0, 0]  # Inicializa el array de 4 bits
    for i in range(4):
        binary_array[3 - i] = num % 2  # Almacena el bit en orden correcto
        num //= 2
    return binary_array

while True:
    if button_increment.is_pressed:  # Si el botón de incremento está presionado
        sleep(0.5)  # Esperar para evitar el rebote
        contador += 1
        if contador > 15:  # Limitar a 15
            contador = 15

    if button_decrement.is_pressed:  # Si el botón de decremento está presionado
        sleep(0.5)  # Esperar para evitar el rebote
        contador -= 1
        if contador < 0:  # Limitar a 0
            contador = 0

    # Obtener la representación binaria del contador
    binary_array = decimal_to_binary_array(contador)

    # Encender o apagar los LEDs según el array binario
    for i in range(4):
        if binary_array[i] == 1:
            leds[i].on()
        else:
            leds[i].off()

    sleep(0.1)  # Pequeña pausa para evitar el uso excesivo de la CPU
