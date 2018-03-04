#!/usr/bin/python3

#
#   MAIN FUNCTION OF THE SAILING BOT. LICENCE GPL. CYRPAUT, 2018
#

from threading import Thread
import bluetooth_server
from global_variables import *

if (__name__ == '__main__'):
	print("Welcome to the sailingbot")
	print("cyrpaut, 2016")

	print("Starting servers:")
	
	btsrv = bluetooth_server.BluetoothServer()
	btsrv.start()
	
	print("  > Bluetooth server started")

	

