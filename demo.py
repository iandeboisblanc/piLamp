import time
import os
import requests
from neopixel import *
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

# Strip Config:
LED_COUNT       = 16
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 5
LED_BRIGHTNESS  = 255
LED_INVERT      = False


# Network Config:
WIFI_NAME = parser.get('wifi', 'wifi_name')
WIFI_PASSWORD = parser.get('wifi', 'wifi_password')

LASTFM_API_KEY = parser.get('apis', 'lastfm_api_key')
LASTFM_HOST = parser.get('apis', 'lastfm_host')

# Account Config:
LASTFM_USER = parser.get('accounts', 'lastfm_user')

print ('Got network: {}'.format(WIFI_NAME))
print ('Got api-key: {}'.format(LASTFM_API_KEY))

# Request Methods:
def queryLastFM():
    payload = {
        'method':     'user.getrecenttracks',
        'user':       LASTFM_USER,
        'api_key':    LASTFM_API_KEY,
        'format':     'json',
        'limit':      1
    }
    r = requests.get('http://{}/2.0/'.format(LASTFM_HOST), params=payload)
    print (r.text)
    print (r.json())

# LED-Control Methods:
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

if __name__ == '__main__':
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    print ('Press Ctrl-C to quit.')
    queryLastFM()
    while True:
        colorWipe(strip, Color(255, 0, 0))
        colorWipe(strip, Color(0, 255, 0))
