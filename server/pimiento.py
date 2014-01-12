#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
#http://RasPi.tv/2013/how-to-use-soft-pwm-in-rpi-gpio-pt-2-led-dimming-and-motor-speed-control
# Using PWM with RPi.GPIO pt 2 - requires RPi.GPIO 0.5.2a or higher

import RPi.GPIO as GPIO # always needed with RPi.GPIO
from time import sleep  # pull in the sleep function from time module
import colorsys # for color math

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM

R_PIN = 17
G_PIN = 22
B_PIN = 23


GPIO.setup(R_PIN, GPIO.OUT)# set GPIO R_PIN as output for white led
GPIO.setup(G_PIN, GPIO.OUT)# set GPIO G_PIN as output for red led
GPIO.setup(B_PIN, GPIO.OUT)# set GPIO G_PIN as output for red led

red = GPIO.PWM(R_PIN, 100)    # create object white for PWM on port 25 at 100 Hertz
green = GPIO.PWM(G_PIN, 100)      # create object red for PWM on port G_PIN at 100 Hertz
blue = GPIO.PWM(B_PIN, 100)      # create object red for PWM on port B_PIN at 100 Hertz

r, g, b = colorsys.hsv_to_rgb(0, 1, 0.5)
red.start(r*100)              # start white led on 0 percent duty cycle (off)
green.start(g*100)              # red fully on (100%)
blue.start(b*100)              # red fully on (100%)

# now the fun starts, we'll vary the duty cycle to 
# dim/brighten the leds, so one is bright while the other is dim

pause_time = 0.02           # you can change this to slow down/speed up

try:
    print "Starting..."
    i = 0.0
    while True:
        r, g, b = colorsys.hsv_to_rgb(i, 1, 0.5)

        red.ChangeDutyCycle(r*100)
        green.ChangeDutyCycle(g*100)
        blue.ChangeDutyCycle(b*100)

        i += 0.005

        sleep(pause_time)

except KeyboardInterrupt:
    red.stop()            # stop the white PWM output
    green.stop()              # stop the red PWM output
    blue.stop()
    GPIO.cleanup()          # clean up GPIO on CTRL+C exit
