from gpiozero import MCP3008, Button
from time import sleep
import math

# Configura el botón del joystick (SW) en el GPIO 25
button = Button(25)

# Inicializa el contador
contador = 0

# Función de interrupción que incrementa el contador y lo reinicia a 0 si pasa de 1
def incrementar_contador():
    global contador
    contador += 1
    if contador > 1:
        contador = 0
    print(f"Contador: {contador}")

# Asocia la función de interrupción al evento de presionar el botón
button.when_pressed = incrementar_contador

# Inicializa el MCP3008 en los canales CH0 y CH1 para los ejes X y Y del joystick
x_axis = MCP3008(channel=0)  # VRx conectado a CH0
y_axis = MCP3008(channel=1)  # VRy conectado a CH1

# Función map personalizada
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# Inicializa la variable dirección
direccion = ""

while True:
    # Lee los valores de los ejes X y Y
    x_value = x_axis.value  # El valor está entre 0.0 y 1.0
    y_value = y_axis.value  # El valor está entre 0.0 y 1.0

    # Mapea los valores de 0.0 - 1.0 a -99 - 99
    x_mapped = map_value(x_value, 0.0, 1.0, -99, 99)
    y_mapped = map_value(y_value, 0.0, 1.0, -99, 99)

    # Calcula el dutycycle utilizando Pitágoras
    dutycycle = math.sqrt(x_mapped**2 + y_mapped**2)

    # Asegura que el dutycycle no exceda 99 y conviértelo en entero
    if dutycycle > 99:
        dutycycle = 99
    dutycycle = int(dutycycle)

    # Solo evalúa las direcciones si el contador es igual a 0
    if contador == 0:
        # Condicionales para la dirección basada en el eje Y y X
        if y_mapped >= 10:
            direccion = "adelante"
        elif y_mapped <= -10:
            direccion = "atrás"
        elif x_mapped >= 10:
            direccion = "derecha"
        elif x_mapped <= -10:
            direccion = "izquierda"
        elif -10 < y_mapped < 10 and -10 < x_mapped < 10:
            direccion = "quieto"  # Cuando el joystick está en el centro o no se mueve mucho

        # Imprime los valores mapeados, la dirección y el dutycycle
        print(f"X: {x_mapped:.2f}, Y: {y_mapped:.2f}, Dirección: {direccion}, Dutycycle: {dutycycle}")

    # Solo evalúa las direcciones si el contador es igual a 1
    if contador == 1:
        # Condicionales para la dirección basada en el eje Y y X en modo omnidireccional
        if y_mapped >= 10 and -10 < x_mapped < 10:
            direccion = "adelante"
        elif y_mapped <= -10 and -10 < x_mapped < 10:
            direccion = "atras"
        elif x_mapped >= 10 and -10 < y_mapped < 10:
            direccion = "derecha"
        elif x_mapped <= -10 and -10 < y_mapped < 10:
            direccion = "izquierda"
        elif x_mapped >= -10 and y_mapped >= 10:
            direccion = "ader_0"  # Adelante derecho
        elif x_mapped <= -10 and y_mapped >= 10:
            direccion = "aizq_0"  # Adelante izquierdo
        elif x_mapped >= 10 and y_mapped <= -10:
            direccion = "bder_0"  # Atrás derecho
        elif x_mapped <= -10 and y_mapped <= -10:
            direccion = "bizq_0"  # Atrás izquierdo
        else:
            direccion = "quieto"  # Cuando el joystick está en el centro o no se mueve mucho

        # Imprime los valores mapeados, la dirección y el dutycycle
        print(f"X: {x_mapped:.2f}, Y: {y_mapped:.2f}, Dirección: {direccion}, Dutycycle: {dutycycle}")

    sleep(0.5)
