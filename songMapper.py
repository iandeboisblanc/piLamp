import math
# https://developer.spotify.com/web-api/get-audio-features/

def generatePattern(songQualities, t):
    bpm = songQualities['tempo'] # float bpm
    timeSignature = songQualities['time_signature'] # int beats / bar
    cheeriness = songQualities['valence'] # 0-1f
    key = songQualities['key'] # int representing half-steps
    energy = songQualities['energy'] # 0-1f
    danciness = songQualities['danceability'] # 0-1f
    # something => number of colors at one time
    # something => color change rate (aka color distance traveled per tick) (or tied to bpm?)



    # Pulse lights to bpm, with larger pulses every timeSignature
    # energy to determine intesity of pulsing (amplitude), or sharpness (sawtooth wave)
    # danciness to determine breadth of color range
    # cheeriness to determine base color scheme


    # Could represent as a series of sine functions added together (Fourier series)
    # Wave-length is fixed > 16 LEDs should be considered continuous, and thus must
    # represent a full wave-length (2n*pi) distance.
    # A separate or layered wave-function can be used for brightness.
    # Amplitude of wave can be mapped to color (should use HSV 0 - 360 deg)

    # For period of 1:
    # f(w,t) = A + B*sin(2pi*wt) + C*sin(2pi*2wt) + D*sin(2pi*3wt)
    #   + E*cos(2pi*wt) + F*cos(2pi*2wt) + G*cos(2pi*3wt)

    #  w => phase (radians), t => time (s)

    # For brightness, all LEDs should probably have same w (flash concurrently):
    # f(t) = A + B*sin(2pi*t*(bpm/60)) + C*sin(2pi*t*(bpm/60)/timeSignature)

    pi = math.pi
    sin = math.sin
    avgBrightness = 3.0
    # brightness = midValue + Wave(period = beat) + Wave(period = measure)
    brightness = avgBrightness + (energy) * sin(2.0*pi*t*bpm/60.0) + (energy) * sin(2.0*pi*t*bpm/timeSignature/60.0)
    state = {
        'brightness': int(math.floor(brightness * 255.0/5.0))
    }
    return state

def piecewiseBrightness(songQualities, t):
    bpm = songQualities['tempo'] # float bpm
    timeSignature = songQualities['time_signature'] # int beats / bar
    energy = songQualities['energy'] # 0-1f

    periodOfMeasure = 60.0 * timeSignature / bpm
    periodOfBeat = 60.0 / bpm

    timeIntoMeasure = t % periodOfMeasure
    timeIntoBeat = t % periodOfBeat

    normalBeatBrightness = 175.0 # Used for reference
    firstBeatMaxBrightness = 255.0
    normalBeatMinDelta = 20.0
    firstBeatMinDelta = 50.0

    # 125.0 is arbitrary sizeable chunk for chilling on the downbeat
    minBrightness = min(normalBeatBrightness - 125.0 * energy, normalBeatBrightness - normalBeatMinDelta)
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
    w = 2 * math.pi / periodOfMeasure

    points = map(lambda x : {'x':x, 't':t, 'w':w}, xValues)
    hues = map(standingWave, points)

    return hues

def standingWave(point):
    x = point['x']
    t = point['t']
    angularFreq = point['w']
    multiplier = 360
    y = (2 * multiplier * math.cos(x) * math.cos(t * angularFreq)) % 360
    return y

# input -> state
# state + ts -> new state
# new state -> draws it
