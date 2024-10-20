from gpiozero import Button
import threading
import time
from joystick_controller import joystick_run
from data_handler import data_run

# Configuración del botón
BUTTON_PIN = 17
button = Button(BUTTON_PIN)

# Variables de control
running = True
active_thread = None

def toggle():
    global running, active_thread
    # Detener el hilo actual si está activo
    if active_thread is not None:
        running = False
        active_thread.join()  # Esperar a que el hilo termine

    # Alternar entre joystick y recolección de datos
    if active_thread is None or active_thread.name == "DataThread":
        print("Cambiando a joystick...")
        active_thread = threading.Thread(target=joystick_run, name="JoystickThread")
    else:
        print("Cambiando a recolección de datos...")
        active_thread = threading.Thread(target=data_run, name="DataThread")

    running = True
    active_thread.start()

# Configurar el botón para alternar la función
button.when_pressed = toggle

if __name__ == "__main__":
    try:
        print("Sistema iniciado. Presiona el botón para alternar entre joystick y recolección de datos.")
        while True:
            time.sleep(1)  # Mantener el programa principal en ejecución
    except KeyboardInterrupt:
        print("Programa terminado.")
    finally:
        print("Limpieza finalizada.")
