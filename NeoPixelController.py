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

def standingWave(point):
    x = point['x']
    t = point['t']
    angularFreq = point['w']
    scalar = point['s']
    y = (2 * scalar * math.sin(x) * math.cos(t * angularFreq)) % 1
    return y

# def bitsToRGB(bits):
#     red = (bits & 0xff0000) >> 16
#     green = (bits & 0x00ff00) >> 8
#     blue = (bits & 0x0000ff)
#     return [red, green, blue]

class NeoPixelController:
    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()
        self.xValues = [2.0 * math.pi * x / LED_COUNT for x in range(0, LED_COUNT)]

    def setColors(self, colors):
        if len(colors) < self.strip.numPixels():
            print('Error: not enough color values for number of LEDs.')
            return
        for i in range(self.strip.numPixels()):
            # rgb = colors[i]
            # if brightnessFilter:
                # rgb = [max(val - brightnessFilter, 0) for val in rgb]
            color = Color(*colors[i])
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def setBrightness(self, value):
        self.strip.setBrightness(value)
        self.strip.show()

    def colorWipe(self, colors, wait_ms=50):
        color = Color(colors[0], colors[1], colors[2])
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def mapSongQualitiesToColors(self, songQualities):
        t = time.time()
        bpm = songQualities['tempo'] # float bpm
        timeSignature = songQualities['time_signature'] # int beats / bar
        cheeriness = songQualities['valence'] # 0-1f
        key = songQualities['key'] # int representing half-steps
        energy = songQualities['energy'] # 0-1f
        danciness = songQualities['danceability'] # 0-1f

        bpm = songQualities['tempo'] # float bpm
        timeSignature = songQualities['time_signature'] # int beats / bar
        periodOfMeasure = 60.0 * timeSignature / bpm

        # wave frequency should be lower for lower energy, in chunks relative to bpm
        waveFreq = 2 * math.pi / periodOfMeasure * math.floor(10 * energy)
        # exagerate effect:
        if energy < 0.5:
            waveFreq = waveFreq / 2
        if energy < 0.25:
            waveFreq = waveFreq / 2

        # scalar => factor for amplitude of wave, based on danciness
        scalar = danciness * danciness * 0.2

        points = [{'x':x, 't':t, 'w':waveFreq, 's':scalar} for x in self.xValues ]

        hues = [standingWave(p) for p in points]

        # Constant amplitude shift => more towards blues, based on cheeriness
        shiftedHues = [(h + (1/6.0) - (1.0 - cheeriness) / 2.0) % 1.0 for h in hues]

        # Time-dependent amplitude shift over a longer period of time to give added motion
        moreShiftedHues = [h + danciness * cheeriness * math.sin(t * waveFreq / 10) % 1.0 for h in shiftedHues]

        unitRgbs = [colorsys.hsv_to_rgb(hue, 1.0, 1.0) for hue in moreShiftedHues]
        scaledRgbs = [[int(math.floor(c * 255)) for c in rgb] for rgb in unitRgbs]

        self.setColors(scaledRgbs)
        # return scaledRgbs

    def mapSongQualitiesToBrightness(self, songQualities):
        t = time.time()
        bpm = songQualities['tempo'] # float bpm
        timeSignature = songQualities['time_signature'] # int beats / bar
        energy = songQualities['energy'] # 0-1f

        periodOfMeasure = 60.0 * timeSignature / bpm
        periodOfBeat = 60.0 / bpm

        timeIntoMeasure = t % periodOfMeasure
        timeIntoBeat = t % periodOfBeat

        # TODO: increase intensity of brightness modulation
        normalBeatBrightness = 75.0 # Used for reference
        firstBeatMaxBrightness = 200.0
        normalBeatMinDelta = 20.0
        firstBeatMinDelta = 50.0

        # 125.0 is arbitrary sizeable chunk for chilling on the downbeat
        minBrightness = min(normalBeatBrightness - 75.0 * energy, normalBeatBrightness - normalBeatMinDelta)
        # If in first beat of measure, generate larger output
        if (timeIntoMeasure < periodOfBeat):
            peakBrightness = max(normalBeatBrightness + (firstBeatMaxBrightness - normalBeatBrightness) * energy, minBrightness + firstBeatMinDelta)
        else:
            peakBrightness = normalBeatBrightness

        # If in first half of beat, slope is positive
        if (timeIntoBeat < periodOfBeat / 2):
            slope = (peakBrightness - minBrightness) / (periodOfBeat / 2)
            intercept = minBrightness
            brightness = slope * timeIntoBeat + intercept
        else:
            slope = (minBrightness - peakBrightness) / (periodOfBeat / 2)
            intercept = minBrightness + 2 * (peakBrightness - minBrightness)
            brightness = slope * timeIntoBeat + intercept
        self.setBrightness(int(math.floor(brightness)))
