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

    minBrightness = 175.0 - (175.0 - 125.0) * energy
    # If in first beat of measure, generate larger output
    if (timeIntoMeasure < periodOfBeat):
        peakBrightness = 175.0 + (255.0 - 175.0) * energy
        print ('==First beat. max brightness:', peakBrightness)
    else:
        peakBrightness = 175.0
        print ('==Later beat. max brightness:', peakBrightness)

    # If in first half of beat, slope is positive
    if (timeIntoBeat < periodOfBeat / 2):
        slope = (peakBrightness - minBrightness) / (periodOfBeat / 2)
        brightness = slope * timeIntoBeat
        print ('..going up. brightness:', brightness)
    else:
        slope = (minBrightness - peakBrightness) / (periodOfBeat / 2)
        brightness = slope * timeIntoBeat + 2 * peakBrightness
        print ('going down. brightness:', brightness)
    return int(math.floor(brightness))


# input -> state
# state + ts -> new state
# new state -> draws it
