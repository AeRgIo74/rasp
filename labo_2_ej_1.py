from gpiozero import LED, Button
from time import sleep

# Configura los LEDs y el botón
led1 = LED(17)
led2 = LED(18)
button = Button(2, pull_up=True)


# Estado inicial
state = 0

def change_state():
    global state
    state += 1
    if state > 3:
        state = 0
    print(f"Estado cambiado a: {state}")

# Configura la detección de presión del botón
button.when_pressed = change_state

# Bucle infinito para controlar los LEDs
while True:
    if state == 0:
        led1.on()
        led2.off()
        sleep(1)
        led1.off()
        led2.on()
        sleep(1)
    elif state == 1:
        led1.on()
        led2.on()
        sleep(2)
        led1.off()
        led2.off()
        sleep(2)
    elif state == 2:
        led1.on()
        led2.on()
    elif state == 3:
        led1.off()
        led2.off()

