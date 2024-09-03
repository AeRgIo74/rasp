import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
LED_PINS = [17, 27, 22, 5]
BUTTON_1 = 6
BUTTON_2 = 13

# Setup for LEDs
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setup for buttons
GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# State management
def initial_state():
    return {'selected_led': 0, 'duration': 1}

# Button 1 press
def button_1_press(state):
    new_led = (state['selected_led'] + 1) % len(LED_PINS)
    return {'selected_led': new_led, 'duration': 1}

# Button 2 press
def button_2_press(state):
    new_duration = state['duration'] + 1
    return {'selected_led': state['selected_led'], 'duration': new_duration}

# Activate LED
def activate_led(state):
    selected_led = state['selected_led']
    duration = state['duration']
    
    GPIO.output(LED_PINS[selected_led], GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(LED_PINS[selected_led], GPIO.LOW)

# Main program loop
def main():
    state = initial_state()

    while True:
        if GPIO.input(BUTTON_1) == GPIO.LOW:
            state = button_1_press(state)
            time.sleep(0.2)  # Debounce delay

        if GPIO.input(BUTTON_2) == GPIO.LOW:
            state = button_2_press(state)
            time.sleep(0.2)  # Debounce delay

        # Activate selected LED
        activate_led(state)
