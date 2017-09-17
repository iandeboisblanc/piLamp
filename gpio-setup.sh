# Initial Pi Setup
# Resources:
#   https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup?view=all
#   https://learn.adafruit.com/neopixels-on-raspberry-pi/software

sudo apt-get update

sudo apt-get install git

# GPIO Control:
sudo apt-get install python-dev # dependency of below
sudo apt-get install python-rpi.gpio

# I2C Control: (Not currently used)
# sudo apt-get install -y python-smbus
# sudo apt-get install -y i2c-tools
# Follow instructions here to continue setting up I2C:
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup?view=all

# Additional dependencies to run pixel library:
sudo apt-get install build-essential scons swig

# Download and compile pixel library:
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons

# Install compiled library:
cd python
sudo python setup.py install

# TODO: include how to make it work for python3?
