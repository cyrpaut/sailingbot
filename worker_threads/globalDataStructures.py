#!/bin/python

class SensorData:
    '''This class contains all sensor data written by the different threads'''
    def __init__(self):

        # GPS Data
        self.gps_long = 0.0
        self.gps_lat = 0.0
        self.gps_speed = 0.0
        self.gps_time = ""
        self.gps_date = ""
        self.gps_validity = ""

        # BNO055 data
        self.BNO055_heading = 0.0
        self.BNO055_roll = 0.0
        self.BNO055_pitch = 0.0
        self.BNO055_sys_cal = 0
        self.BNO055_gyro_cal = 0
        self.BNO055_accel_cal = 0
        self.BNO055_mag_cal = 0

        # Bournes Encoder
        self.bournes_angle = 0.0
        self.bournes_turns = 0

        # Windcock angle
        self.mocoder_angle = 0
        self.average_mocoder_angle = 0

        # Wifi Status
        self.wifi_link = 0
        self.wifi_level = 0
        self.wifi_noise = 0

        # Button status
        self.button_activate = False


class ActuatorParameters:
    '''This class contains variable which are target for PID'''
    def __init__(self):

        # Tiller Servo
        self.tiller_servo_min = 0
        self.tiller_servo_max = 0
        self.tiller_servo_PID = 0
        self.tiller_servo_actual = 0

        # Main line Servo
        self.line_servo_min = 0
        self.line_servo_max = 0
        self.line_servo_PID = 0
        self.line_servo_actual = 0