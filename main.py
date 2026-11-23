import time
from machine import Pin
import dht
import ujson

pin_led1 = 16
pin_led2 = 17
sensor = dht.DHT11(Pin(15))
led1 = Pin(pin_led1, Pin.OUT)
led2 = Pin(pin_led2, Pin.OUT)
# Los números 15, 16 y 17 pueden cambiar de acuerdo
# al pin al que se conecte el sensor DHT11 y los LEDs.

prev_weather = ""
# Variable donde se guardarán los datos de temperatura y humedad.

while True:
    try:
        print("Obteniendo valores...")
        sensor.measure()

        # Se declara la variable datos con temperatura y humedad
        datos = {
            "temperatura": sensor.temperature(),
            "humedad": sensor.humidity(),
        }

        message = ujson.dumps(datos)

        # Validamos que el valor cambie; si no, se imprime "Sin cambios"
        if message != prev_weather:
            print("Valores actualizados!")
            print(message)

            if datos["temperatura"] < 23:
                print("led encendido")
                led1(1)
                led2(1)
            else:
                print("led apagado")
                led1(0)
                led2(0)

            prev_weather = message
        else:
            print("Sin cambios")

        time.sleep(2)
    except OSError:
        print("Intento de leer desde el sensor falló.")
