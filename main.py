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
from worker_threads.Thread_mocoder import MocoderThread
from worker_threads.Thread_Wifi_Quality import WifiThread
from worker_threads.Thread_Button import ButtonThread
from worker_threads.Thread_Status_LED import StatusLedThread

class parameters:
    def __init__(self):
        self.bournes_i2c_address = int()
        self.mocoder_i2c_address = int()
        self.BNO055_serial_adress = ""
        self.gps_serial_adress = ""
        self.button_pin = 0
        self.led_pin_1 = 0
        self.led_pin_2 = 0
        self.led_pin_3 = 0


class SailingBot:
    '''Main Class executing threads for the control of the sailingbot'''
    def __init__(self, _parameters):
        # Load sensor self.data structure
        self.data = SensorData()
        self.parameters = _parameters

        # Thread initialization flag
        self.data.thread_ready = False

    def start(self):
        '''Start sensor & actuator threads'''
        print("Starting Threads:")

        print("Starting 3 color monitor led thread")
        led_monitor_thread = StatusLedThread(0, "Status led monitor", self.parameters.led_pin_1, \
                                             self.parameters.led_pin_2, self.parameters.led_pin_3, self.data)
        led_monitor_thread.daemon = True
        led_monitor_thread.start()

        print("Starting Bournes encoder thread...")
        encoder_thread = BournesEncoderThread(1, "Bournes Encoder Thread", self.parameters.bournes_i2c_address, self.data)
        encoder_thread.daemon = True
        encoder_thread.start()

        print("Sarting mocoder thread...")
        mocoder_thread = MocoderThread(2, "Mocoder Thread", self.parameters.mocoder_i2c_address, self.data)
        mocoder_thread.daemon = True
        mocoder_thread.start()

        print("Starting Wifi Quality Control thread...")
        wifi_thread = WifiThread(3, "Wifi Thread", self.data)
        wifi_thread.daemon = True
        wifi_thread.start()

        print("Starting BNO055 thread...")
        bno055_thread = BNO055Thread(4, "BNO055 Thread", self.parameters.BNO055_serial_adress, self.data)
        bno055_thread.daemon = True
        bno055_thread.start()

        print("Starting GPS thread...")
        gps_thread = GpsThread(5, "GPS Thread", self.parameters.gps_serial_adress, self.data)
        gps_thread.daemon = True
        gps_thread.start()

        print("Starting Logger Button thread...")
        button_thread = ButtonThread(5, "GPS Thread", self.parameters.button_pin, self.data)
        button_thread.daemon = True
        button_thread.start()

        # Set the flag to OK
        self.data.thread_ready = True

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
                      "Heading=", self.data.BNO055_heading, \
                      "Mocoder angle=", self.data.mocoder_angle, \
                      "Mocoder ave angl=", self.data.average_mocoder_angle, \
                      "Logger button=", self.data.button_activate)

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
    param.mocoder_i2c_address = 0x36
    param.button_pin = 16
    param.led_pin_1 = 19
    param.led_pin_2 = 20
    param.led_pin_3 = 21

    # Running main program
    SB = SailingBot(param)
    SB.start()
    SB.run()
