import math
import colorsys
import time
from neopixel import *

LED_COUNT       = 16
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 5
LED_BRIGHTNESS  = 255
LED_INVERT      = False

class NeoPixelController:
    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.xValues = [2.0 * math.pi * x / LED_COUNT for x in range(0, LED_COUNT)]

    def setColors(self, colors):
        if len(colors) < self.strip.numPixels():
            print('Error: not enough color values for number of LEDs.')
            return
        for i in range(self.strip.numPixels()):
            color = Color(*colors[i])
            self.strip.setPixelColor(i, color)

    def colorWipe(self, color, wait_ms=50):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def mapSongQualities(self, qualities):
        
