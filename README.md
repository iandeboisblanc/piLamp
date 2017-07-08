# piLamp
Code for using a Raspberry Pi to power LED lamp

## Installing dependencies
Although this code can be run in python3, the necessary neopixel library must be compiled using python2.
To build the library, follow the instructions [here](https://learn.adafruit.com/neopixels-on-raspberry-pi/software).
However, during the `python setup.py install` step, replace `python` with the path to your virtualenv python:

```
../../piLamp/[env]/bin/python3 setup.py install
```

## Other stuff
If the lights are flashy, you may need to [disable the pi sound card.](http://www.instructables.com/id/Disable-the-Built-in-Sound-Card-of-Raspberry-Pi/)
