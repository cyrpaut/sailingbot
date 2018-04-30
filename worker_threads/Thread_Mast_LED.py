#!/usr/bin/python

import sys
import time
import threading
import RPi.GPIO as GPIO
from globalDataStructures import SensorData

class MastLedThread(threading.Thread):
    def __init__(self, threadID, name, mast_led_pin, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.mast_led_pin = mast_led_pin

        # Initiation GPIO module
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(mast_led_pin, GPIO.OUT)
        GPIO.output(mast_led_pin, GPIO.LOW)


    def run(self):
        while True:
            # Check quality of Wifi connection and the socket connection
            if (self.SensorData.wifi_link >= 20):
                if(self.SensorData.is_connected):
                    self.noblink(self.mast_led_pin)
                else:
                    self.slow_blink(self.mast_led_pin)
            else:
                self.fast_blink(self.mast_led_pin)


    def noblink(self, pin1, pin2=False, pin3=False):
        GPIO.output(pin1, GPIO.HIGH)
        if (pin2): GPIO.output(pin2, GPIO.HIGH)
        if (pin3): GPIO.output(pin3, GPIO.HIGH)
        time.sleep(self.status_time)
        GPIO.output(pin1, GPIO.LOW)
        if (pin2): GPIO.output(pin2, GPIO.LOW)
        if (pin3): GPIO.output(pin3, GPIO.LOW)


    def slow_blink(self, pin1, pin2=False, pin3=False):
        for i in range(3):
            GPIO.output(pin1, GPIO.HIGH)
            if (pin2) : GPIO.output(pin2, GPIO.HIGH)
            if (pin3) : GPIO.output(pin3, GPIO.HIGH)

            time.sleep(0.5)
            GPIO.output(pin1, GPIO.LOW)
            if (pin2) : GPIO.output(pin2, GPIO.LOW)
            if (pin3) : GPIO.output(pin3, GPIO.LOW)
            time.sleep(0.5)

    def fast_blink(self, pin1, pin2=False, pin3=False):
        for i in range(15):
            GPIO.output(pin1, GPIO.HIGH)
            if (pin2) : GPIO.output(pin2, GPIO.HIGH)
            if (pin3) : GPIO.output(pin3, GPIO.HIGH)

            time.sleep(0.1)
            GPIO.output(pin1, GPIO.LOW)
            if (pin2) : GPIO.output(pin2, GPIO.LOW)
            if (pin3) : GPIO.output(pin3, GPIO.LOW)
            time.sleep(0.1)


# Test Function if the script is executed standalone to test monitoring led thread on the system
if __name__ == "__main__":

    print("Test method for monitor led thread. Type Ctrl+C to exit gracefully.")

    data = SensorData()

    mast_led_pin = 18

    thread = MastLedThread(1, "Monitor 3 color led thread", mast_led_pin, data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Monitoring...")
            time.sleep(3)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()