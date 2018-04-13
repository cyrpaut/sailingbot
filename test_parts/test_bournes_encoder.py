#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import smbus
import time

class Ace128:

    """Class supporting the ACE-128 I2C Backpack"""

    if GPIO.RPI_REVISION == 1:
        _bus = smbus.SMBus(0)
    else:
        _bus = smbus.SMBus(1)

    def __init__(self, i2caddr, pinOrder=(8,7,6,5,4,3,2,1)):
        self._i2caddr = i2caddr

        Ace128._bus.write_byte(self._i2caddr, 255)  # set all pins up. pulldown for input

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
        return Ace128._bus.read_byte(self._i2caddr)

    def rawPos(self):
        return self._map[self.acePins()]

if __name__ == "__main__":
    DEVICE = 0x3f  # Device address (A0-A2)
    ace = Ace128(0x3f)

    print("Sailingbot test part - Bournes absolute position rotary encoder on adress 0x3f")
    print("Part can be ordered from tindies https://www.tindie.com/products/arielnh56/high-resolution-absolute-encoder-128-positions/")
    print("Many thanks to Red Hunter for the part and the associated code")
    while True:
        print("Weathercock is at " + str(ace.rawPos()*2.8125) + " degree")
        time.sleep(0.5)

