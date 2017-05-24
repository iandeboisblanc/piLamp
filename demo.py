import time
import os
import requests
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
WIFI_NAME = parser.get('wifi', 'wifi_name')
WIFI_PASSWORD = parser.get('wifi', 'wifi_password')

print ('Got network: {}'.format(WIFI_NAME))
print ('Got api-key: {}'.format(LASTFM_API_KEY))

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
    song = getMostRecentSong(token)
    print ('Checking for currently playing song...')
    # if song['is_playing']:
    qualities = getSongQualities(song['item']['id'])

    while True:
        state = generatePattern(qualities, time.time())
        strip.setBrightness(state['brightness'])
