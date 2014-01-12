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

# Helpers
def do_rgb(r,g,b):
    r /= 255
    g /= 255
    b /= 255

    red.ChangeDutyCycle(r*100)
    green.ChangeDutyCycle(g*100)
    blue.ChangeDutyCycle(b*100)

def handle_update(snapshot):
    data = snapshot.val()

    r = data['red']['value']
    g = data['green']['value']
    b = data['blue']['value']

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

red.start(0)
green.start(0)
blue.start(0)

# pause_time = 0.02           # you can change this to slow down/speed up

try:
    # Setup Firebase
    root = firebasin.Firebase(FIREBASE_ROOT)

    root.child('devices/%s' % DEVICE_ID).on('value', handle_update)

except KeyboardInterrupt:
    red.stop()            # stop the white PWM output
    green.stop()              # stop the red PWM output
    blue.stop()
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit
