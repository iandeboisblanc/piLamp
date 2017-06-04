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

    # For brightness, all LEDs should probably have same w (flash concurrently):
    # f(t) = A + B*sin(2pi*t*(bpm/60)) + C*sin(2pi*timeSignature*t*(bpm/60))
    pi = math.pi
    sin = math.sin
    avgBrightness = 3.0
    brightness = avgBrightness + (0.5 + energy) * sin(2.0*pi*t*bpm/60.0) + energy * sin(2.0*pi*timeSignature*t*bpm/60.0)
    state = {
        'brightness': int(math.floor(brightness * 255.0/5.5))
    }
    return state

    # input -> state
    # state + ts -> new state
    # new state -> draws it
