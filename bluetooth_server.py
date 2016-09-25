#!/usr/bin/python3

#
# SailingBot, cyrpaut, 2016
# Threaded bluetooth server based on python3 standard socket and RFCOMM protocol
#

import bluetooth
import threading
from global_variables import *

class BluetoothServer(threading.Thread):
	def __init__(self):
		# Initialize Threading
		threading.Thread.__init__(self)

		# Setting up server socket
		self.server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		self.port = 1
		self.server_sock.bind(("",self.port))
		self.server_sock.listen(1)

	def run(self):
		# Getting global control variables
		global global_tiller_position
		global global_sail_position
		global global_control_mode

		while True:

			flag = True

			print("BLUETOOTH > Waiting for bluetooth connection")
			self.client_sock, address = self.server_sock.accept()
			print("BLUETOOTH > Connexion accepted from", address)

			while True:
				try:
					data = self.client_sock.recv(1024)
					print("BLUETOOTH > RECEIVED [%s]" % data)

				except:
					print("BLUETOOTH > Connection lost!")
					self.client_sock.close()
					flag = False
					break


				data_string = data.decode("utf-8")
				data_list = data_string.split('\r')[0].split(':')

				if (data_list[0] == "Sail"):
					global_sail_position = int(data_list[1])
					global_control_mode = "Manual"

				if (data_list[0] == "Tiller"):
					global_tiller_position = int(data_list[1])
					global_control_mode = "Manual"

				if (data_list[0] == "HoldTiller"):
					global_control_mode = "HoldTiller"

				if (data_list[0] == "HoldSail"):
					global_control_mode = "SailSail"

				if (data_list[0] == "HoldBoth"):
					global_control_mode = "HoldBoth"

				message = ":".join([global_control_mode, str(global_tiller_position), str(global_sail_position)])
				message += '\r\n'
				if flag:
					self.client_sock.send(message.encode(encoding='UTF-8'))

	
	def stop(self):
		self.client_sock.close()
		self.server_sock.close()

# Unitary test for this method: Send something using Bluetooth Terminal app from Android

if (__name__ == '__main__'):
	#global_tiller_position = 50
	#global_sail_position = 50	
	#global_control_mode = "Manual" 	

	btsrv = BluetoothServer()
	try:
		btsrv.run()
	except KeyboardInterrupt:
		btsrv.stop()
