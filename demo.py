import time
import os
import requests
import sys
import math
from neopixel import *
from configparser import ConfigParser
from songMapper import generateColors, piecewiseBrightness
from apiTest import generateSpotifyToken, getMostRecentSong, getSongQualities

parser = ConfigParser()
parser.read('config.ini')

# Strip Config:
LED_COUNT       = 16
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 5
LED_BRIGHTNESS  = 255
LED_INVERT      = False

# Network Config:
SPOTIFY_CLIENT_ID = parser.get('apis', 'spotify_client_id')
SPOTIFY_CLIENT_SECRET = parser.get('apis', 'spotify_client_secret')
SPOTIFY_REDIRECT_URL = parser.get('apis', 'spotify_redirect_url')

# LED-Control Methods:
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def setColors(strip, colors):
    for i in range(strip.numPixels()):
        color = Color(*colors[i])
        strip.setPixelColor(i, color)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print('Press Ctrl-C to quit.')
    else:
        print("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
    print('Checking for currently playing song...')
    song = getMostRecentSong(token)
    print('Playing:', song['item']['name'])
    # if song['is_playing']:
    qualities = getSongQualities(token, song['item']['id'])
    print('BPM:', qualities['tempo'])
    print('Time Signature:', qualities['time_signature'])
    print('Energy:', qualities['energy'])
    print('Cheeriness', qualities['valence'])
    print('Danciness', qualities['danceability'])

    print('color about to be wiped.')
    colorWipe(strip, Color(255, 0, 0))
    print('color wiped.')
    xValues = map(lambda x: 2.0 * math.pi * x / LED_COUNT, range(0, LED_COUNT))
    while True:
        # state = generatePattern(qualities, time.time())
        # print ('brightness:', state['brightness'])
        brightness = piecewiseBrightness(qualities, time.time())
        # print ('brightness:', brightness)
        strip.setBrightness(brightness)
        colors = generateColors(qualities, time.time(), xValues)
        setColors(strip, colors)
        strip.show()
