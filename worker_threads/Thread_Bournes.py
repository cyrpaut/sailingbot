#!/usr/bin/python

import sys
import time
import threading
import RPi.GPIO as GPIO
import smbus
from globalDataStructures import SensorData

exitFlag = 0


class BournesEncoderThread (threading.Thread):

    """Class supporting BOURNES rotary encoder Ace128 I2C Backpack"""

    if GPIO.RPI_REVISION == 1:
        _bus = smbus.SMBus(0)
    else:
        _bus = smbus.SMBus(1)

    def __init__(self, threadID, name, i2caddr, SensorData, pinOrder=(8,7,6,5,4,3,2,1)):
        threading.Thread.__init__(self)
        self._i2caddr = i2caddr
        self.thread_ID = threadID
        self.thread_name = name
        self.SensorData = SensorData

        BournesEncoderThread._bus.write_byte(self._i2caddr, 255)  # set all pins up. pulldown for input

        # create encoder map on the fly - ported from make_encodermap.ino
        # track binary data taken from p1 column on datasheet

        track = [
            0b11000000, 0b00111111, 0b11110000, 0b00001111,
            0b11100000, 0b00011111, 0b11111111, 0b11111111,
            0b11111111, 0b00000000, 0b11111100, 0b00000011,
            0b10000000, 0b01111000, 0b00000110, 0b00000001,
            ]
        self._map = [255] * 256  # an array of all possible bit combinations
        for pos in range(0, 128):  # imagine rotating the encoder
            index = 0
            mask = 128 >> pos % 8  # which bit in current byte
            for pin in range(0, 8):  # think about each pin
                # which byte in track[] to look at.
                #  Each pin is 16 bits behind the previous
                offset = (pos - (1 - pinOrder[pin]) * 16) % 128 / 8
                if track[offset] & mask:  # is the bit set?
                    index |= 0b00000001 << pin  # set that pin's bit in the index byte

            self._map[index] = pos  # record the position in the map

    def acePins(self):
        return BournesEncoderThread._bus.read_byte(self._i2caddr)

    def rawPos(self):
        return self._map[self.acePins()]

    def run(self):
        while True:
            prev_angle = self.SensorData.bournes_angle
            self.SensorData.bournes_angle = self.rawPos() * 2.8125

            #print(self.SensorData.bournes_angle)

            if (prev_angle > 330 and self.SensorData.bournes_angle < 100):                   #Positive turn
                self.SensorData.bournes_turns += 1

            if (prev_angle < 30 and self.SensorData.bournes_angle > 280 ):                #Negative turn
                self.SensorData.bournes_turns -= 1

            time.sleep(0.01)

# Test Function if the script is executed standalone to test Bournes Ace128
if __name__ == "__main__":

    print("Test method for Bournes Encoder thread class. Type Ctrl+C to exit gracefully.")

    data = SensorData()

    encoder_i2c_address = 0x3f

    thread = BournesEncoderThread(1, "Bournes Encoder Thread", encoder_i2c_address, data)
    thread.daemon = True
    thread.start()

    print("Comming back to main Thread")

    while True:
        try:
            print("Angle=", data.bournes_angle, "Turns=", data.bournes_turns)
            time.sleep(0.2)
        except KeyboardInterrupt:
            print("You pressed ctrl+C")
            sys.exit()
