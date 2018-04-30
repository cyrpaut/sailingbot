#!/usr/bin/python

import sys
import time
import threading
from globalDataStructures import SensorData

class WifiThread (threading.Thread):
    def __init__(self, threadID, name, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.wifi_quality_file_path = "/proc/net/wireless"

    def run(self):
        while True:
            self.SensorData.wifi_link, self.SensorData.wifi_level, self.SensorData.wifi_noise = self.read_values()
            time.sleep(5)

    def read_values(self):
        file = open(self.wifi_quality_file_path, 'r')

        #Get to last line
        for line in file:
            pass

        l = line.split(' ')
        clean_lst = filter(None,l)

        return float(clean_lst[2]), float(clean_lst[3]), float(clean_lst[4])



# Test Function if the script is executed standalone to test Wifi quality on the system
if __name__ == "__main__":

    print("Test method for Wifi quality checker thread. Type Ctrl+C to exit gracefully.")

    data = SensorData()

    thread = WifiThread(1, "Wifi Quality check Thread", data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Link=", data.wifi_link, \
                  "Level=", data.wifi_level, \
                  "Noise=", data.wifi_noise)
            time.sleep(5)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()