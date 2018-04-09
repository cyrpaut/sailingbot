#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

print "SailingBot: Test 3 color led on pin 19,20,21"

while 1:
	GPIO.output(21,GPIO.LOW)
	GPIO.output(19,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(19,GPIO.LOW)
	GPIO.output(20,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(20,GPIO.LOW)
	GPIO.output(21,GPIO.HIGH)
	time.sleep(1)
