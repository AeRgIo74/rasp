from gpiozero import Buzzer, Button
from time import sleep

buzzer = Buzzer(18)  # Define el pin para el buzzer
button = Button(23)  # Define el pin para el botón

while True:
    if button.is_pressed:  # Si el botón está presionado
        buzzer.on()  # Enciende el buzzer
    else:
        buzzer.off()  # Apaga el buzzer
    sleep(0.1)  # Añade un pequeño retardo para evitar sobrecargar la CPU

