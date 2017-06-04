import time
import os
import requests
import sys
from neopixel import *
from ConfigParser import SafeConfigParser
from songMapper import generatePattern
from apiTest import generateSpotifyToken, getMostRecentSong, getSongQualities

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
SPOTIFY_CLIENT_ID = parser.get('apis', 'spotify_client_id')
SPOTIFY_CLIENT_SECRET = parser.get('apis', 'spotify_client_secret')
SPOTIFY_REDIRECT_URL = parser.get('apis', 'spotify_redirect_url')

# LED-Control Methods:
def colorWipe(strip, color, wait_ms=50):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        print ('Press Ctrl-C to quit.')
    else:
        print ("Usage: %s 'spotify username'" % (sys.argv[0],))
        sys.exit()
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()

    token = generateSpotifyToken(username, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URL)
    print ('Checking for currently playing song...')
    song = getMostRecentSong(token)
    print ('Playing:', song['item']['name'])
    # if song['is_playing']:
    qualities = getSongQualities(token, song['item']['id'])

    colorWipe(strip, Color(255, 0, 0))
    while True:
        state = generatePattern(qualities, time.time())
        print ('brightness:', state['brightness'])
        strip.setBrightness(state['brightness'])
        strip.show()
