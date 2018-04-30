#!/usr/bin/python

import sys
import time
import threading
from Adafruit_BNO055 import BNO055
from globalDataStructures import SensorData

class BNO055Thread (threading.Thread):
    def __init__(self, threadID, name, sensor_address, SensorData):
        threading.Thread.__init__(self)
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData
        self.sensor_address = sensor_address
        self.bno = BNO055.BNO055(serial_port=sensor_address, rst=1)

        # Initializing BNO055 connection
        while True:
            try:
                # Initialize the BNO055 and stop if something went wrong.
                if not self.bno.begin():
                    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

                # Print system status and self test result.
                status, self_test, error = self.bno.get_system_status()
                break

            except Exception as e:
                print("Got error: {}".format(e))
                print("Sleeping 1s before retrying")
                time.sleep(1)

        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')

    def run(self):
        while True:
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            self.SensorData.BNO055_heading, self.SensorData.BNO055_roll, self.SensorData.BNO055_pitch = self.bno.read_euler()
            # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
            self.SensorData.BNO055_sys_cal, self.SensorData.BNO055_gyro_cal, self.SensorData.BNO055_accel_cal, self.SensorData.BNO055_mag_cal = self.bno.get_calibration_status()
            time.sleep(0.1)


# Test Function if the script is executed standalone to test BNO055 sensor
if __name__ == "__main__":

    print("Test method for BNO055 thread class. Type Ctrl+C to exit gracefully.")

    data = SensorData()
    thread = BNO055Thread(1, "BNO055 Thread",'/dev/serial0', data)
    thread.daemon = True
    thread.start()

    while True:
        try:
            print("Accel cal=", data.BNO055_accel_cal, \
                  "Gyro Cal=", data.BNO055_gyro_cal, \
                  "Mag cal=", data.BNO055_mag_cal, \
                  "Sys cal=", data.BNO055_sys_cal, \
                  "Pitch=", data.BNO055_pitch, \
                  "Roll=", data.BNO055_roll, \
                  "Heading=", data.BNO055_heading)
            time.sleep(1)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()
