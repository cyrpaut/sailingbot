#!/usr/bin/python

import sys
import time
import threading
import serial
from globalDataStructures import SensorData

exitFlag = 0

class GpsThread (threading.Thread):
    def __init__(self, threadID, name, serial_address, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.serial_address = serial_address

        self.firstFixFlag = False  # this will go true after the first GPS fix.
        self.firstFixDate = ""

        # Set up serial connexion
        self.ser = serial.Serial(
            port=serial_address, \
            baudrate=4800, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=1)


    def run(self):
        while True:
            line = self.ser.readline()
            if "$GPRMC" in line:                         # This will exclude other NMEA sentences the GPS unit provides.
                gpsData = self.parse_GPRMC(line)         # Turn a GPRMC sentence into a Python dictionary called gpsData

                self.SensorData.gps_validity = gpsData['validity']

                if gpsData['validity'] == "A":           # If the sentence shows that there's a fix, then we can log the line
                    if self.firstFixFlag is False:       # If we haven't found a fix before, then set the filename prefix with GPS date & time.
                        self.firstFixDate = gpsData['fix_date'] + "-" + gpsData['fix_time']
                        self.firstFixFlag = True
                    else:                                 # write data in the datastructure
                        self.SensorData.gps_date = gpsData['fix_date']
                        self.SensorData.gps_time = gpsData['fix_time']
                        self.SensorData.gps_lat = gpsData['decimal_latitude']
                        self.SensorData.gps_long = gpsData['decimal_longitude']
                        self.SensorData.gps_speed = gpsData['speed']

    def parse_GPRMC(self, data):
        data = data.split(',')
        dict = {
                'fix_time': data[1],
                'validity': data[2],
                'latitude': data[3],
                'latitude_hemisphere' : data[4],
                'longitude' : data[5],
                'longitude_hemisphere' : data[6],
                'speed': data[7],
                'true_course': data[8],
                'fix_date': data[9],
                'variation': data[10],
                'variation_e_w' : data[11],
                'checksum' : data[12]
        }
        dict['decimal_latitude'] = self.degrees_to_decimal(dict['latitude'], dict['latitude_hemisphere'])
        dict['decimal_longitude'] = self.degrees_to_decimal(dict['longitude'], dict['longitude_hemisphere'])
        return dict

    # Helper function to take HHMM.SS, Hemisphere and make it decimal:
    def degrees_to_decimal(self, data, hemisphere):
        try:
            decimalPointPosition = data.index('.')
            degrees = float(data[:decimalPointPosition - 2])
            minutes = float(data[decimalPointPosition - 2:]) / 60
            output = degrees + minutes
            if hemisphere is 'N' or hemisphere is 'E':
                return output
            if hemisphere is 'S' or hemisphere is 'W':
                return -output
        except:
            return ""


# Test Function if the script is executed standalone to test GPS
if __name__ == "__main__":

    print("Test method for GPS thread class. Type Ctrl+C to exit gracefully.")

    data = SensorData()
    thread = GpsThread(1, "GPS Thread",'/dev/ttyUSB0', data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Longitude=", data.gps_long, \
                  "Latitude=", data.gps_lat, \
                  "Speed=", data.gps_speed, \
                  "Time=", data.gps_time, \
                  "Date=", data.gps_date)
            time.sleep(1)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()
