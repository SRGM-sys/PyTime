import time
from machine import Pin
import dht
import ujson
import network
from umqtt.simple import MQTTClient

MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER = "industrial.api.ubidots.com"
MQTT_USER = "PEGAR-AQUÍ-EL-TOKEN-OBTENIDO"
MQTT_PASSWORD = ""
MQTT_TOPIC = "NIOT-PyTime-IOT"

pin_led1 = 16
pin_led2 = 17
sensor = dht.DHT11(Pin(15))
led1 = Pin(pin_led1, Pin.OUT)
led2 = Pin(pin_led2, Pin.OUT)

SSID_RED = "PEGAR-AQUI-NOMBRE-DEL-HOST"
PASSWORD_RED = "PEGAR-AQUI-CONTRASEÑA-DEL-HOST"

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID_RED, PASSWORD_RED)
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    user=MQTT_USER,
    password=MQTT_USER
)
client.connect()
print("Connected!")

prev_weather = ""
while True:
    try:
        print("Obteniendo valores... ", end="")
        sensor.measure()
        datos = {
            "temperatura": sensor.temperature(),
            "humedad": sensor.humidity(),
        }
        message = ujson.dumps(datos)

        if message != prev_weather:
            print("Updated!")
            print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
            client.publish(b"/v1.6/devices/ESP32", message)

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
            print("No change")

        time.sleep(2)
    except OSError:
        print("Intento de leer desde el sensor falló.")
