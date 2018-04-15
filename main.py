#!/usr/bin/python

#
#   MAIN FUNCTION OF THE SAILING BOT. LICENCE GPL. CYRPAUT, 2018
#

import sys
import time
from globalDataStructures import SensorData
from Thread_BNO055 import BNO055Thread
from Thread_Bournes import BournesEncoderThread
from Thread_GPS import GpsThread


print("Welcome to the sailingbot")
print("cyrpaut, 2016")

# Load sensor data structure
data = SensorData()

#Data to migrate in the conf file
bournes_i2c_address = 0x3f
BNO055_serial_adress = '/dev/serial0'
gps_serial_adress = '/dev/ttyUSB0'

print("Starting Threads:")

print("Starting Bournes encoder thread...")
encoder_thread = BournesEncoderThread(1, "Bournes Encoder Thread", data, bournes_i2c_address)
encoder_thread.daemon = True
encoder_thread.start()

print("Starting BNO055 thread...")
bno055_thread = BNO055Thread(1, "BNO055 Thread", BNO055_serial_adress, data)
bno055_thread.daemon = True
bno055_thread.start()

print("Starting GPS thread...")
gps_thread = GpsThread(1, "GPS Thread", '/dev/ttyUSB0', data)
gps_thread.daemon = True
gps_thread.start()

while True:
    try:
        print("Longitude=", data.gps_long, \
              "Latitude=", data.gps_lat, \
              "Speed=", data.gps_speed, \
              "Time=", data.gps_time, \
              "Date=", data.gps_date,
              "Angle=", data.bournes_angle, \
              "Turns=", data.bournes_turns, \
              "Accel cal=", data.BNO055_accel_cal, \
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