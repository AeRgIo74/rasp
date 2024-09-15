import serial
from gpiozero import PWMOutputDevice, DigitalOutputDevice, Button
from signal import pause

def leer_configuracion():
    # Inicializa los valores de duty
    duty1 = 50  # Valor por defecto
    duty2 = 50  # Valor por defecto

    # Lee el archivo duty.txt para obtener los valores de duty1 y duty2
    try:
        with open('/home/AeRgIo/Downloads/rasp/labo 5/duty.txt', 'r') as f:
            for line in f:
                if line.startswith('duty1='):
                    duty1 = float(line.split('=')[1].strip())
                elif line.startswith('duty2='):
                    duty2 = float(line.split('=')[1].strip())
    except FileNotFoundError:
        print("El archivo duty.txt no se encontró. Usando valores por defecto.")

    return duty1, duty2

# Inicializa el puerto serie
ser = serial.Serial(
    port='/dev/ttyACM0',  # Ajusta esto según tu configuración
    baudrate=115200,
    timeout=1
)

# Inicializa los pines GPIO para los motores
motor1_on = DigitalOutputDevice(pin=17)  # GPIO para encender/apagar motor1
motor2_on = DigitalOutputDevice(pin=18)  # GPIO para encender/apagar motor2

# Inicializa los pines PWM para los motores
motor1_pwm = PWMOutputDevice(pin=22)  # GPIO para PWM de motor1
motor2_pwm = PWMOutputDevice(pin=23)  # GPIO para PWM de motor2

# Inicializa el pin GPIO para el botón (sensor táctil)
buzzer_button = Button(27, pull_up=True)  # Cambia el número de pin según tu conexión

# Asigna la función a ejecutar cuando el botón es presionado
def button_pressed():
    print("Botón presionado, enviando mensaje 'buzzer' a Tiva.")
    ser.write(b'buzzer\r\n')  # Envía el mensaje 'buzzer' al Tiva

buzzer_button.when_pressed = button_pressed  # Asignación fuera del bucle

# Variables de estado de los motores
motor1_state = False  # Estado del motor1 (apagado)
motor2_state = False  # Estado del motor2 (apagado)

# Función para establecer el ciclo de trabajo (duty cycle)
def set_duty_cycle(motor_pwm, duty_cycle):
    motor_pwm.value = duty_cycle / 100  # Escala de 0-100 a 0-1

try:
    while True:
        duty1, duty2 = leer_configuracion()  # Leer configuración
        set_duty_cycle(motor1_pwm, duty1)     # Actualizar duty cycle motor1
        set_duty_cycle(motor2_pwm, duty2)     # Actualizar duty cycle motor2

        if ser.in_waiting > 0:
            message = ser.readline().decode().strip()
            print(f"Mensaje recibido: {message}")

            if message == "motor1":
                motor1_state = not motor1_state  # Cambia el estado del motor1
                if motor1_state:
                    print("Activando motor1")
                    motor1_on.on()  # Enciende motor1
                else:
                    print("Apagando motor1")
                    motor1_on.off()  # Apaga motor1

            elif message == "motor2":
                motor2_state = not motor2_state  # Cambia el estado del motor2
                if motor2_state:
                    print("Activando motor2")
                    motor2_on.on()  # Enciende motor2   
                else:
                    print("Apagando motor2")
                    motor2_on.off()  # Apaga motor2


except KeyboardInterrupt:
    pass
finally:
    motor1_pwm.close()
    motor2_pwm.close()
    motor1_on.close()
    motor2_on.close()
    ser.close()
