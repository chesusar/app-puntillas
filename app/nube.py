# pip install adafruit-io

import random
import time

from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY = ''
ADAFRUIT_IO_USERNAME = 'Rarribas'

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.connect()

client.loop_background()

print('Publica un nuevo mensaje cada 10 segundos (Ctrl-C para salir)...')
while True:
    value = random.randint(0, 100)
    print('Publicando {0} a feed.'.format(value))
    client.publish('maximo', value)
    client.publish('promedio', value)
    client.publish('minimo', value)
    client.publish('tiempo-subida', value)
    client.publish('tiempo-puntillas', value)
    time.sleep(10)
