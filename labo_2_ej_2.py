from gpiozero import LED, Button
from time import sleep

# Inicializar los LEDs en los pines correspondientes
leds = [
    LED(17),  # LED 1 en el pin GPIO 17rt
    LED(27),  # LED 2 en el pin GPIO 27
    LED(22),  # LED 3 en el pin GPIO 22
    LED(23),  # LED 4 en el pin GPIO 23
]

# Inicializar los botones en los pines correspondientes
button_increment = Button(18, pull_up=True)  # Botón en GPIO 18 con pull-up
button_decrement = Button(15, pull_up=True)  # Botón en GPIO 15 con pull-up

contador = 0

def decimal_to_binary_array(num):
    binary_array = [0, 0, 0, 0]  # Inicializa el array de 4 bits
    for i in range(4):
        binary_array[3 - i] = num % 2  # Almacena el bit en orden correcto
        num //= 2
    return binary_array

def increment_counter():
    global contador
    contador += 1
    if contador > 15:  # Limitar a 15
        contador = 15
    update_leds()
    
def decrement_counter():
    global contador
    contador -= 1
    if contador < 0:  # Limitar a 0
        contador = 0
    update_leds()

def update_leds():
    # Obtener la representación binaria del contador
    binary_array = decimal_to_binary_array(contador)

    # Encender o apagar los LEDs según el array binario
    for i in range(4):
        if binary_array[i] == 1:
            leds[i].on()
        else:
            leds[i].off()
    print(contador)

# Asignar funciones de callback a los botones
button_increment.when_pressed = increment_counter
button_decrement.when_pressed = decrement_counter

# Bucle principal
while True:
    sleep(0.1)  # Pequeña pausa para evitar alta carga de CPU

