import Adafruit_DHT

sensor = Adafruit_DHT.DHT11  # O DHT22 si est�s usando ese sensor
pin = 27  # Pin GPIO conectado al DHT11

try:
    while True:
        # Forzar el uso de la Raspberry Pi
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature}�C  Humidity: {humidity}%")
        else:
            print("Failed to read data from sensor.")
        time.sleep(2)

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    print("Cleaning up GPIO...")
