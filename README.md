# SailingBot

Project repository for the development of the main firmware for an open-source sailing robot.

# Purpose

The aim of this project piece of code is to develop the core real-time controler of our automatic sailing robot. Based on a Raspberry pi 3 and some easily purchasable parts, we want to develop an automatic saling robot for which you have a standard remote control mode using an android app to drive the boat based on bluetooth low energy, a semi-automated mode in which you can ask the boat to hold direction and hold its sail to face the wind fluctuation. Our ultimate goal is to develop a GPS driving mode in which some waypoint are programmed through the android app and the boat is capable of measuring the wind direction, its position using the embeded GPS and calculate the optimal way to follow the instructions.

# Parts

The hardware is composed of:
 - A raspberry Pi 3 Rev 1.3 B
 - An Adafruit Raspberry Pi PWM Hat for servo control
 - An BlueDot 9 axis "gyroscope" BNO055 purchased from Amazon (will work the same with adafruit BNO055 but it is more expensive)
 - An USB GPS G-Star IV
 - A 3 color intense led for monitoring boat status
 - A rotary encoder for wind direction
 - A simple 180 degree servo for the tiller
 - A continuous rotation servo for the sail line
 - A mobile phone external power supply for powering the Pi
 - A 4 battery pack for powering the servo
 - An android phone with our app for control

# Wiring

 - The raspberry Pi PWM HAT is soldered as indicated by adafruit
 - The tiller servo is plugged on the first PWM connector
 - The sail line servo is connected on the 2nd PWM connector
 - The GPS is connected on the USB plug of the Raspberry Pi
 - The 3 color led is connected on pin 19-20-21 of the HAT breakout. Ground is connected to ground of this breakout.
 - The BNO055 is soldered using adapters on the top of the breakout. 
  - RST pin of BNO055 is connected on GPIO 1 (pin 12 of Rpi).  
  - SDA pin of BNO055 is connected to GPIO 16 (pin 10) which act as an emulated serial UART RX.
  - SCL pin of BNO055 is connected to GPIO 15 (pin 8) which act as an emulated serial UART TX.
  - GND pin of BNO055 is connected to GRND (pin 6 or equivalent in the breakout).
  - 3.3V from the Rpi (pin 1) is connected to both VCC and PS1 (which enable serial interface on the BNO055).
 - Rotary encoder is connected to pin 5 and pin 6 of the breakout.

# Configuring the Pi

## Configuring the system

Install a fresh raspbian Jessy on a 8 GB SD card. Start your pi and connect a screen and a keyboard. Go to raspi-config and enable SSH. Reboot.

Connect to the py through the network

```bash
$ ssh pi@my-IP-adress
```
Using raspbian-config, expand the storage on the whole drive ("7 Advanced Options" > "A1 Expand Filesystem") and reboot.

Reconnect your ssh shell. 

Using raspbian-config disable serial console ("5 Interfacing Options" > "P6 Serial" | <No> and then <Yes>) and enable IC2 ("5 Interfacing Options" > "P5 I2C") , and reboot.

## Installing Bluetooth

Install the pip3 package manager to install the PyBuleZ library by typing

```bash
$ sudo apt-get install python3-pip
$ sudo pip3 install PyBluez
```

You need to make your bluetooth device discoverable for pairing it with your phone by typing

```bash
$ sudo hciconfig hci0 piscan
$ sudo hciconfig hci0 name 'Device Name'
```

Then pair it with your phone. You won't need these to type these command again unless you want to pair it with a new phone or device

## Installing Wi-Fi

OPTINAL: Configure the wifi, so that you can upgrade the code on the boat without having to put a RJ45 on your boat which is not very convenient...

Edit the 'wpa_supplicant.conf' file by typing

```bash
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

And add to the file:

```
	network={
		ssid="MY_SSID"
		scan_ssid=1
		key_mgmt=WPA-PSK
		psk="MY_WIFI_PASSWORD"
	}
```
Then upgrade the wifi configuration by typing

```bash
$ sudo wpa_cli reconfigure
```

And then your are connected to your wifi, you can unplug the RJ45 and reconnect your ssh tunnel

## Cloning SailingBot repository

Go to your home folder and clone this repository by typing

```bash
$ sudo apt-get install git
$ git clone https://github.com/cyrpaut/sailingbot.git
```

Go in the folder and run the server manually to check its functionnality by typing

```bash
$ chmod +x main.py
$ ./main.py
```

You should see all servers started with no error, and the control led starting flashing. If not, check your configuration.

Make the software start automatically at startup using cron -e (to finish...)

# Acknowledgements

Many thanks to the people I got inspiration from, including:

 - Adafruit PWM libraries and BNO055 raspberry library, under BSD licence
 - Sash0k for its androind bluetooth terminal I outrageously got inspired from
 - David Vassalo for demonstrating Python/raspberry pi communication through RFCOMM (http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/)
 - To the many people in the forums, and the large python and raspberry pi community


