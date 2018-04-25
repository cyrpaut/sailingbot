#!/usr/bin/python

import smbus
import time
address = 0x36

# Create SMBus on raspi I2C bus
bus = smbus.SMBus(1)

# Register adresses for memory from AMS_5600.cpp arduino demo file by AMS chip builder
_zmco = 0x00
_zpos_hi = 0x01
_zpos_lo = 0x02
_mpos_hi = 0x03
_mpos_lo = 0x04
_mang_hi = 0x05
_mang_lo = 0x06
_conf_hi = 0x07
_conf_lo = 0x08
_raw_ang_hi = 0x0c
_raw_ang_lo = 0x0d
_ang_hi = 0x0e
_ang_lo = 0x0f
_stat = 0x0b
_agc = 0x1a
_mag_hi = 0x1b
_mag_lo = 0x1c
_burn = 0xff


print("Sailingbot AMS5600 test function")
print("Device connected by I2C on 0x36 adress\n")

# Read all registers

while True:
	raw_ang_hi = bus.read_byte_data(address,_raw_ang_hi)
	raw_ang_lo = bus.read_byte_data(address,_raw_ang_lo)
	ang_hi = bus.read_byte_data(address,_ang_hi)
	ang_lo = bus.read_byte_data(address,_ang_lo)
	stat = bus.read_byte_data(address,_stat)
	agc = bus.read_byte_data(address, _agc)
	mag_hi = bus.read_byte_data(address,_mag_hi)
	mag_lo = bus.read_byte_data(address,_mag_lo)

	print("\n---")
	print("raw_ang_hi: {n10} \t raw_ang_lo: {n11} \t ang_hi: {n12} \t ang_lo: {n13} \t stat: {n14} \t agc: {n15} \t mag_hi: {n16} \t mag_lo: {n17}".format(n10=raw_ang_hi, n11=raw_ang_lo, n12=ang_hi, n13=ang_lo, n14=stat, n15=agc, n16=mag_hi, n17=mag_lo))

	# The angle is cutted into 8 sectors of 22,5 degree which are themselve devided in 256 bits
	calc_angle = raw_ang_hi * 22.5 + raw_ang_lo * 0.087890625

	print("Calculated angle: {}".format(calc_angle))

	time.sleep(0.5)

