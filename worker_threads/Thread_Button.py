#!/usr/bin/python

import sys
import time
import threading
import RPi.GPIO as GPIO
from globalDataStructures import SensorData

class ButtonThread (threading.Thread):
    def __init__(self, threadID, name, button_pin, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.button_pin = button_pin

        # Initiation GPIO module with button in pull down mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def run(self):

        prev_input = 0

        while True:
            # take a reading
            input = GPIO.input(self.button_pin)

            # if the last reading was low and this one high, print
            if ((not prev_input) and input):
                if (self.SensorData.button_activate):
                    self.SensorData.button_activate = False
                else:
                    self.SensorData.button_activate = True

            # update previous input
            prev_input = input

            # slight pause to debounce
            time.sleep(0.05)


# Test Function if the script is executed standalone to test logging button on the system
if __name__ == "__main__":

    print("Test method for logging button thread. Type Ctrl+C to exit gracefully.")

    data = SensorData()

    button_pin = 16

    thread = ButtonThread(1, "Logging button thread", button_pin, data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Button statue=", data.button_activate)
            time.sleep(0.5)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()