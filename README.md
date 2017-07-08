# piLamp
Code for using a Raspberry Pi to power LED lamp

## Installing dependencies
Although this code can be run in python3, the necessary neopixel library must be compiled using python2.
To build the library, follow the instructions [here](https://learn.adafruit.com/neopixels-on-raspberry-pi/software).
However, during the `python setup.py install` step, replace `python` with the path to your virtualenv python:

```
../../piLamp/[env]/bin/python3 setup.py install
```
