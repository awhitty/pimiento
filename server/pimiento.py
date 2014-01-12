#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
#http://RasPi.tv/2013/how-to-use-soft-pwm-in-rpi-gpio-pt-2-led-dimming-and-motor-speed-control
# Using PWM with RPi.GPIO pt 2 - requires RPi.GPIO 0.5.2a or higher

import RPi.GPIO as GPIO # always needed with RPi.GPIO
from time import sleep  # pull in the sleep function from time module
import colorsys # for color math

import firebasin

FIREBASE_ROOT = "https://pimiento.firebaseio.com"
DEVICE_ID = 0

RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 23

r_value = 0.0
g_value = 0.0
b_value = 0.0

# Helpers
def do_rgb(r,g,b):
    r /= 255.0
    g /= 255.0
    b /= 255.0

    r *= 100
    g *= 100
    b *= 100

    r_step = (r-r_value)/100
    g_step = (g-g_value)/100
    b_step = (g-g_value)/100

    for i in range(0,101):
	red.ChangeDutyCycle(r_value)
        green.ChangeDutyCycle(g_value)
        blue.ChangeDutyCycle(b_value)

        r_value += r_step
        b_value += b_step
        g_value += g_step

        sleep(0.02)


def handle_update(snapshot):
    data = snapshot.val()

    print data

    r = float(data['red'].get('value', 0))
    g = float(data['green'].get('value', 0))
    b = float(data['blue'].get('value', 0))

    do_rgb(r,g,b)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Create PWM objects
red   = GPIO.PWM(RED_PIN, 100)  
green = GPIO.PWM(GREEN_PIN, 100)
blue  = GPIO.PWM(BLUE_PIN, 100) 

red.start(r_value)
green.start(g_value)
blue.start(b_value)

# pause_time = 0.02           # you can change this to slow down/speed up

try:
    # Setup Firebase
    root = firebasin.Firebase(FIREBASE_ROOT)

    root.child('devices/%s' % DEVICE_ID).on('value', handle_update)

    while True:
        1 + 1    	

except KeyboardInterrupt:
    red.stop()            # stop the white PWM output
    green.stop()              # stop the red PWM output
    blue.stop()
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit
