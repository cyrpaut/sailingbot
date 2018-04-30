#!/usr/bin/python

import sys
import time
import threading
import RPi.GPIO as GPIO
from globalDataStructures import SensorData

class StatusLedThread (threading.Thread):
    def __init__(self, threadID, name, led_pin_1, led_pin_2, led_pin_3, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.led_pin_1 = led_pin_1
        self.led_pin_2 = led_pin_2
        self.led_pin_3 = led_pin_3

        self.status_time = 3

        # Initiation GPIO module
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(led_pin_1, GPIO.OUT)
        GPIO.setup(led_pin_2, GPIO.OUT)
        GPIO.setup(led_pin_3, GPIO.OUT)

        GPIO.output(led_pin_1, GPIO.LOW)
        GPIO.output(led_pin_2, GPIO.LOW)
        GPIO.output(led_pin_3, GPIO.LOW)

    def run(self):
        while True:
            # Check that all threads are started: Color=Red
            if (self.SensorData.thread_ready):
                self.noblink(self.led_pin_3)
            else:
                self.fast_blink(self.led_pin_3)

            # Check GPS status: Color=Blue
            if (self.SensorData.gps_validity == 'A'):
                self.noblink(self.led_pin_1)
            else:
                self.fast_blink(self.led_pin_1)

            # Check BNO055 calibration status: Color=Green
            if (self.SensorData.BNO055_sys_cal == 1 or self.SensorData.BNO055_sys_cal == 2):
                self.slow_blink(self.led_pin_2)
            elif (self.SensorData.BNO055_sys_cal == 3):
                self.noblink(self.led_pin_2)
            else:
                self.fast_blink(self.led_pin_2)

            # Check if rotary encoder are connected: Color=Yellow
            if (self.SensorData.mocoder_angle == 0.0 or self.SensorData.bournes_angle == 0.0): # Error on one of the encoders
                self.fast_blink(self.led_pin_2, self.led_pin_3)
            else:
                self.noblink(self.led_pin_2, self.led_pin_3)

            # Check button/logging status: Color = White
            if (self.SensorData.button_activate):
                self.noblink(self.led_pin_1, self.led_pin_2, self.led_pin_3)
            else:
                self.slow_blink(self.led_pin_1, self.led_pin_2, self.led_pin_3)


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

    led_pin_1 = 19
    led_pin_2 = 20
    led_pin_3 = 21

    thread = StatusLedThread(1, "Monitor 3 color led thread", led_pin_1, led_pin_2, led_pin_3, data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Monitoring...")
            time.sleep(3)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()