from gpiozero import Buzzer, Button
from time import sleep

buzzer = Buzzer(18)  # Define el pin para el buzzer
touch_on = Button(23, pull_up=True, bounce_time=0.5)   # Sensor táctil para encender el buzzer
touch_off = Button(24, pull_up=True, bounce_time=0.5)  # Sensor táctil para apagar el buzzer
state = 0
last_state_on = False
last_state_off = False

while True:
    current_state_on = touch_on.is_pressed
    current_state_off = touch_off.is_pressed

    if current_state_on and not last_state_on:  # Detectar transición
        state = 1
        print("Touch ON presionado, estado: 1")

    if current_state_off and not last_state_off:  # Detectar transición
        state = 0
        print("Touch OFF presionado, estado: 0")

    last_state_on = current_state_on
    last_state_off = current_state_off

    print(f"Estado actual: {state}")  # Imprime el valor de 'state'

    # Controla el estado del buzzer
    if state == 1:
        buzzer.off()  # Enciende el buzzer
    else:
        buzzer.on()  # Apaga el buzzer

    sleep(0.1)  # Añade un pequeño retardo para evitar sobrecargar la CPU
