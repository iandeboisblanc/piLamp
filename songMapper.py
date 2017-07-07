import math
import colorsys
# https://developer.spotify.com/web-api/get-audio-features/

### GAME PLAN: ###
# Pulse lights to bpm, with larger pulses every timeSignature
# energy to determine intesity of pulsing (amplitude), or sharpness (sawtooth wave)
# danciness to determine breadth of color range
# cheeriness to determine base color scheme

def piecewiseBrightness(songQualities, t):
    bpm = songQualities['tempo'] # float bpm
    timeSignature = songQualities['time_signature'] # int beats / bar
    energy = songQualities['energy'] # 0-1f

    periodOfMeasure = 60.0 * timeSignature / bpm
    periodOfBeat = 60.0 / bpm

    timeIntoMeasure = t % periodOfMeasure
    timeIntoBeat = t % periodOfBeat

    # TODO: increase intensity of brightness modulation
    normalBeatBrightness = 100.0 # Used for reference
    firstBeatMaxBrightness = 175.0
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
    return int(math.floor(brightness))

# xValues is an array of positions for which a hue-value will be generated
def generateColors(songQualities, t, xValues):
    bpm = songQualities['tempo'] # float bpm
    timeSignature = songQualities['time_signature'] # int beats / bar
    cheeriness = songQualities['valence'] # 0-1f
    key = songQualities['key'] # int representing half-steps
    energy = songQualities['energy'] # 0-1f
    danciness = songQualities['danceability'] # 0-1f

    bpm = songQualities['tempo'] # float bpm
    timeSignature = songQualities['time_signature'] # int beats / bar
    periodOfMeasure = 60.0 * timeSignature / bpm

    # wave frequency should be lower for lower energy
    # TODO: map waveFreq to bpm-matching chunks
    waveFreq = 2 * math.pi / periodOfMeasure * math.floor(10 * energy)

    # scalar => intensity of wave, based on danciness
    # TODO consider reducing in order to tell difference better
    # OR, consider having whole wave shift up and down over time to cover spectrum
    # while the per-LED color difference is smaller at a given t
    scalar = danciness * danciness * 0.2

    points = map(lambda x : {'x':x, 't':t, 'w':waveFreq, 's':scalar}, xValues)
    hues = map(standingWave, points)

    # phase shift => more towards blues, based on cheeriness
    shiftedHues = map(lambda h : (h + (1/6.0) - (1.0 - cheeriness) / 2.0) % 1.0 , hues)

    # add wave movement over time
    moreShiftedHues = map(lambda h : h + danciness * danciness * math.sin(t * waveFreq / 10), shiftedHues)

    unitRgbs = map(lambda hue: colorsys.hsv_to_rgb(hue, 1.0, 1.0) , moreShiftedHues)
    scaledRgbs = map(lambda rgb: map(lambda c: int(math.floor(c * 255)), rgb), unitRgbs)
    return scaledRgbs

def standingWave(point):
    x = point['x']
    t = point['t']
    angularFreq = point['w']
    scalar = point['s']
    y = (2 * scalar * math.sin(x) * math.cos(t * angularFreq)) % 1
    return y
