#!/usr/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("SailingBot: Test button on GPIO 16 of Adafruit Servo Hat")

prev_input = 0

while True:
  #take a reading
  input = GPIO.input(16)
  #if the last reading was low and this one high, print
  if ((not prev_input) and input):
    print("Button pressed")
  #update previous input
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
