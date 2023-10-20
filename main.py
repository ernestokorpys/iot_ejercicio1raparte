# Germán Andrés Xander 2023

from machine import Pin, Timer, unique_id
import dht
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')

mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=10, ssl=True)

led = Pin(2, Pin.OUT)
d = dht.DHT22(Pin(25))
contador = 0

def heartbeat(nada):
    global contador
    if contador > 5:
        pulsos.deinit()
        contador = 0
        return
    led.value(not led.value())
    contador += 1
  
def transmitir(pin):
    print("publicando")
    mqtt.connect()
    mqtt.publish(f"iot/{CLIENT_ID}",datos)
    mqtt.disconnect()
    pulsos.init(period=150, mode=Timer.PERIODIC, callback=heartbeat)

pulsos = Timer(1)
temperatura_superior=25;
temperatura_inferior=25;
publicado = False  # Variable de estado para rastrear si se ha realizado la publicación

while True:
    try:
        d.measure()
        temperatura = d.temperature()
        humedad = d.humidity()
        datos = json.dumps(OrderedDict([
            ('La tempera ha alcanzado el valor de ', temperatura)
        ]))
        print("Temperatura: "+ str(temperatura))
        if temperatura >= temperatura_superior and not publicado:
            transmitir(None)
            publicado = True  
        elif temperatura < temperatura_inferior:
            publicado = False  
    except OSError as e:
        print("sin sensor")
    time.sleep(5)
