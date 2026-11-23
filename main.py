import time
from machine import Pin
import dht
import ujson
import network
from umqtt.simple import MQTTClient

# --- Parámetros del servidor MQTT (Ubidots) ---
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_USER = "PEGAR-AQUÍ-EL-TOKEN-OBTENIDO"
MQTT_PASSWORD = ""
MQTT_TOPIC = "IEEE-PyTime-IOT"

# --- Configuración de pines (pueden variar según tu circuito) ---
pin_led1 = 16
pin_led2 = 17
sensor = dht.DHT11(Pin(15))
led1 = Pin(pin_led1, Pin.OUT)
led2 = Pin(pin_led2, Pin.OUT)

# --- Conexión a la red WiFi ---
print("Conectando a WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("SSID-RED", "PASSWORD-RED")  # Reemplazar con los datos de tu red

while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" ¡Conectado!")

# --- Conexión al servidor MQTT ---
print("Conectando al servidor MQTT... ", end="")
client = MQTTClient(
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    user=MQTT_USER,
    password=MQTT_USER
)
client.connect()
print("¡Conectado!")

# --- Lectura del sensor y envío de datos ---
prev_weather = ""

while True:
    try:
        print("Leyendo sensor... ", end="")
        sensor.measure()
        datos = {
            "temperatura": sensor.temperature(),
            "humedad": sensor.humidity(),
        }
        message = ujson.dumps(datos)

        # Publicamos solo si los valores cambiaron
        if message != prev_weather:
            print("¡Valores actualizados!")
            print(f"Enviando al tópico {MQTT_TOPIC}: {message}")
            client.publish(b"/v1.6/devices/ESP32", message)

            if datos["temperatura"] < 23:
                print("LEDs encendidos")
                led1(1)
                led2(1)
            else:
                print("LEDs apagados")
                led1(0)
                led2(0)

            prev_weather = message
        else:
            print("Sin cambios")

        time.sleep(2)  # El DHT11 necesita al menos 2 segundos entre lecturas
    except OSError:
        print("Error al leer el sensor DHT11.")