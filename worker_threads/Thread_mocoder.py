#!/usr/bin/python

import sys
import smbus
import time
import threading
from collections import deque
from globalDataStructures import SensorData

class MocoderThread (threading.Thread):
    def __init__(self, threadID, name, i2c_address, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.i2c_address = i2c_address

        # Using deque system instead of list because it it programmed to be performant to remove intem in the left of the list
        self.ave_deque = deque([0]*30)
        self.ave_deque_len = len(self.ave_deque)

        self.ang_hi_address = 0x0e
        self.ang_lo_address = 0x0f

        # Set-up i2c smbus connexion
        self.bus = smbus.SMBus(1)

    def run(self):
        while True:
            ang_hi = self.bus.read_byte_data(self.i2c_address, self.ang_hi_address)
            ang_lo = self.bus.read_byte_data(self.i2c_address, self.ang_lo_address)

            self.SensorData.mocoder_angle = ang_hi * 22.5 + ang_lo * 0.087890625

            self.ave_deque.popleft()
            self.ave_deque.extend([self.SensorData.mocoder_angle])

            sum = 0
            for elem in self.ave_deque:
                sum += elem

            self.SensorData.average_mocoder_angle = sum / self.ave_deque_len

            time.sleep(0.1)



# Test Function if the script is executed standalone to test Mocoder thread
if __name__ == "__main__":

    print("Test method for Mocoder thread class. Type Ctrl+C to exit gracefully.")

    data = SensorData()
    thread = MocoderThread(1, "Mocoder Thread", 0x36, data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Current angle=", data.mocoder_angle, \
                  "Average angle=", data.average_mocoder_angle)
            time.sleep(1)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()
