from gpiozero import Buzzer, Button
from signal import pause
from time import sleep

# Definición de las notas
notes = {
    'C4': 261,
    'D4': 294,
    'E4': 329,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 493,
    'C5': 523,
    'C6': 1047,
    'D5': 587,
    'E5': 659,
    'F5': 698,
    'G5': 784,
    'A5': 880,
    'B5': 988,
    'AS4': 466,
    'AS5': 932,
    'DS6': 1175,
    'CS6': 1109,
    'G#5': 830,
    'F6': 1397,  # Agregado
    'REST': 0  # Opcional: para manejar los silencios
}

# Definición de la canción
melody = [
    'AS4', 'AS4', 'AS4',
    'F5', 'C6',
    'AS5', 'A5', 'G5', 'F6', 'C6',
    'AS5', 'A5', 'G5', 'F6', 'C6',
    'AS5', 'A5', 'AS5', 'G5', 'C5', 'C5', 'C5',
    'F5', 'C6',
    'AS5', 'A5', 'G5', 'F6', 'C6',

    'AS5', 'A5', 'G5', 'F6', 'C6',
    'AS5', 'A5', 'AS5', 'G5', 'C5', 'C5',
    'D5', 'D5', 'AS5', 'A5', 'G5', 'F5',
    'F5', 'G5', 'A5', 'G5', 'D5', 'E5', 'C5', 'C5',
    'D5', 'D5', 'AS5', 'A5', 'G5', 'F5',

    'C6', 'G5', 'G5', 'REST', 'C5',
    'D5', 'D5', 'AS5', 'A5', 'G5', 'F5',
    'F5', 'G5', 'A5', 'G5', 'D5', 'E5', 'C6', 'C6',
    'F6', 'DS6', 'CS6', 'C6', 'AS5', 'G#5', 'G5', 'F5',
    'C6'
]

durations = [
    8, 8, 8,
    2, 2,
    8, 8, 8, 2, 4,
    8, 8, 8, 2, 4,
    8, 8, 8, 2, 8, 8, 8,
    2, 2,
    8, 8, 8, 2, 4,

    8, 8, 8, 2, 4,
    8, 8, 8, 2, 8, 16,
    4, 8, 8, 8, 8, 8,
    8, 8, 8, 4, 8, 4, 8, 16,
    4, 8, 8, 8, 8, 8,

    8, 16, 2, 8, 8,
    4, 8, 8, 8, 8, 8,
    8, 8, 8, 4, 8, 4, 8, 16,
    4, 8, 4, 8, 4, 8, 4, 8,
    1
]

buzzer = Buzzer(18)
touch_next = Button(23, pull_up=True)   # Botón para la siguiente canción
touch_prev = Button(24, pull_up=True)   # Botón para la canción anterior

current_song_index = 0

def play_song(song):
    """Reproduce una canción."""
    for note, duration in zip(song, durations):
        frequency = notes[note]
        buzzer.on()
        sleep(duration / 1000)  # Duración en segundos
        buzzer.off()
        sleep(duration * 1.3 / 1000)  # Pausa entre notas

def next_song():
    """Cambia a la siguiente canción."""
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    print(f"Cambiando a la canción {current_song_index + 1}")

def prev_song():
    """Cambia a la canción anterior."""
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    print(f"Cambiando a la canción {current_song_index + 1}")

# Asignar funciones de interrupción
touch_next.when_pressed = next_song
touch_prev.when_pressed = prev_song

try:
    while True:
        play_song(melody)  # Reproduce la canción actual
        sleep(0.1)
except KeyboardInterrupt:
    buzzer.off()
    print("Programa detenido.")
