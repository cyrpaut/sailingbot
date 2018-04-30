#!/usr/bin/python

#
#   MAIN FUNCTION OF THE SAILING BOT. LICENCE GPL. CYRPAUT, 2018
#

import sys
import time
from worker_threads.globalDataStructures import SensorData
from worker_threads.Thread_BNO055 import BNO055Thread
from worker_threads.Thread_Bournes import BournesEncoderThread
from worker_threads.Thread_GPS import GpsThread

class parameters:
    def __init__(self):
        self.bournes_i2c_address = int()
        self.BNO055_serial_adress = ""
        self.gps_serial_adress = ""


class SailingBot:
    '''Main Class executing threads for the control of the sailingbot'''
    def __init__(self, _parameters):
        # Load sensor self.data structure
        self.data = SensorData()
        self.parameters = _parameters

    def start(self):
        '''Start sensor & actuator threads'''
        print("Starting Threads:")
        print("Starting Bournes encoder thread...")
        encoder_thread = BournesEncoderThread(1, "Bournes Encoder Thread", self.data, self.parameters.bournes_i2c_address)
        encoder_thread.daemon = True
        encoder_thread.start()

        print("Starting BNO055 thread...")
        bno055_thread = BNO055Thread(1, "BNO055 Thread", self.parameters.BNO055_serial_adress, self.data)
        bno055_thread.daemon = True
        bno055_thread.start()

        print("Starting GPS thread...")
        gps_thread = GpsThread(1, "GPS Thread", self.parameters.gps_serial_adress, self.data)
        gps_thread.daemon = True
        gps_thread.start()

    def run(self):
        '''Console logging'''
        while True:
            try:
                print("Longitude=", self.data.gps_long, \
                      "Latitude=", self.data.gps_lat, \
                      "Speed=", self.data.gps_speed, \
                      "Time=", self.data.gps_time, \
                      "Date=", self.data.gps_date,
                      "Angle=", self.data.bournes_angle, \
                      "Turns=", self.data.bournes_turns, \
                      "Accel cal=", self.data.BNO055_accel_cal, \
                      "Gyro Cal=", self.data.BNO055_gyro_cal, \
                      "Mag cal=", self.data.BNO055_mag_cal, \
                      "Sys cal=", self.data.BNO055_sys_cal, \
                      "Pitch=", self.data.BNO055_pitch, \
                      "Roll=", self.data.BNO055_roll, \
                      "Heading=", self.data.BNO055_heading)

            except KeyboardInterrupt:
                print("You pressed ctrl+C")
                sys.exit()
                
            time.sleep(1)


if __name__ == "__main__":
    print("Welcome to the sailingbot")
    print("cyrpaut, 2016")

    # Load parameters data structures
    param = parameters()

    # Data to migrate in the conf file
    param.bournes_i2c_address = 0x3f
    param.BNO055_serial_adress = '/dev/serial0'
    param.gps_serial_adress = '/dev/ttyUSB0'

    # Running main program
    SB = SailingBot(param)
    SB.start()
    SB.run()
