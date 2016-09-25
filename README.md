# SailingBot

Project repository for the development of the main firmware for an open-source sailing robot.

# Purpose

The aim of this project piece of code is to develop the core real-time controler of our automatic sailing robot. Based on a Raspberry pi 3 and some easily purchasable parts, we want to develop an 
automatic saling robot for which you have a standard remote control mode using an android app to drive the boat based on bluetooth low energy, a semi-automated mode in which you can ask the boat
to hold direction and hold its sail to face the wind fluctuation. Our ultimate goal is to develop a GPS driving mode in which some waypoint are programmed through the android app and the boat is
capable of measuring the wind direction, its position using the embeded GPS and calculate the optimal way to follow the instructions.

# Parts

The hardware is composed of:
 - A raspberry pi 3
 - An Adafruit Raspberry Pi PWM Hat for servo control
 - An Adafruit 9 axis "gyroscope" BNO055
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
 - The GPS is connected on the USB plug
 - The 3 color led is connected on pin 19-20-21 of the HAT breakout. Ground is connected to ground of this breakout.
 - The BNO055 is soldered using adapters on the top of the breakout. 
  - RST pin is connected on GPIO 19. 
  - Serial pin are connected to the TX and RX pin of the breakout.
  - GRND is connected to GRND
  - 3.3V from the raspberry is connected to Vin and PS1 to enable serial interface on the BNO055
 - Rotary encoder is connected to pin 5 and pin 6 of the breakout

# Configuring the Pi

A fresh raspbian installation is made on a 8 GB SD card.

Using raspbian-config disable serial console and enable IC2, and reboot
 
