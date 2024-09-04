from gpiozero import LED, Button
from time import sleep

# Define GPIO pins
leds = [
    LED(17),  # LED 1 en el pin GPIO 17
    LED(27),  # LED 2 en el pin GPIO 27
    LED(22),  # LED 3 en el pin GPIO 22
    LED(23),  # LED 4 en el pin GPIO 23
]

button_1 = Button(18, pull_up=True)  # Botón en GPIO 18 con pull-up
button_2 = Button(15, pull_up=True) 

# State management
def initial_state():
    return {'selected_led': 0, 'duration': 1}

# Button 1 press
def button_1_press(state):
    new_led = (state['selected_led'] + 1) % len(leds)
    return {'selected_led': new_led, 'duration': 1}

# Button 2 press
def button_2_press(state):
    new_duration = state['duration'] + 1
    if new_duration > 10:
        new_duration = 1
    return {'selected_led': state['selected_led'], 'duration': new_duration}

# Activate LED
def activate_led(state):
    selected_led = state['selected_led']
    duration = state['duration']
    
    leds[selected_led].on()
    sleep(duration)
    leds[selected_led].off()
    sleep(duration)

# Main program loop
def main():
    state = initial_state()

    while True:
        if button_1_press:
            state = button_1_press(state)
            sleep(0.2)  # Debounce delay

        if button_2_press:
            state = button_2_press(state)
            sleep(0.2)  # Debounce delay

        # Activate selected LED
        activate_led(state)
