# SailingBot

Project repository for the development of the main firmware of my open-source sailing robot. More documentation about this project is to be made on a dedicated website in the future. For now, the project is just an embryo and not functionning as expected.

# Purpose

The aim of this project is to developped an automatic sailing boat model, which is capable of going from waypoints to waypoints on a flat water, by automatically adapting its trajectory, sails and direction in function of the wind direction and wind force. All data will be saved to a file, and remotely transfered to a graphic interface on a computer for real-time monitoring of all parameters and manual control of the boat model through Wifi.

# Parts

The hardware of the boast is composed of:
 - A raspberry Pi 3 Rev 1.3 B freshly flashed with a Raspbian Stretch image
 - An [Adafruit Raspberry Pi PWM Hat](https://www.adafruit.com/product/2327) for servo control 
 - An [BlueDot 9 axis "gyroscope" BNO055](https://www.bluedot.space/shop/) purchased from Amazon (or an [Adafruit BNO055](https://www.adafruit.com/product/2472)) 
 - An USB GPS GlobalSat [G-Star IV BU-353S4](http://usglobalsat.com/p-688-bu-353-s4.aspx#images/product/large/688.jpg)
 - A 3 color intense led for monitoring boat status (Similar to [this one](https://www.amazon.fr/SODIAL-Couleurs-Couleur-tricolore-Arduino/dp/B00JGFF8PC/))
 - An [absolute position rotary encoder](https://www.tindie.com/products/arielnh56/high-resolution-absolute-encoder-128-positions/) for the windcock purchased from tindies
 - A simple [180 degree servo](https://www.servocity.com/hs-311-servo) for the tiller 
 - A [continuous rotation servo](https://www.pololu.com/product/1248) for the sail main sheet
 - A small press button connected by a wire
 - A red led on the top of the mast indicating wifi quality and signaling before the connection is lost
 - A mobile phone external power supply for powering the Pi
 - A 4 battery pack for powering the servo
 - An old laptop for controlling the boat over wifi

# Wiring

 - The raspberry Pi PWM HAT is soldered and mounted [as indicated by adafruit](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/)
 - The tiller servo is plugged on the first PWM connector (Number 0)
 - The main sheet servo is connected on the 2nd PWM connector (Number 1)
 - The GPS is connected on the USB plug of the Raspberry Pi
 - The 3 color led is connected on pin 19-20-21 of the HAT breakout. Ground is connected to ground of this breakout.
 - The BNO055 is soldered using adapters on the top breadboard of the Adafruit Servo Hat. 
    - RST pin of BNO055 is connected on GPIO 1.  
    - SDA pin of BNO055 is connected to GPIO 16 which act as an emulated serial UART RX.
    - SCL pin of BNO055 is connected to GPIO 15 which act as an emulated serial UART TX.
    - GND pin of BNO055 is connected to GRND.
    - 3.3V from the Rpi (Pin 1) is connected to both VCC and PS1 (which enable serial interface on the BNO055).
 - The I2C rotary encoder is connected to the SDA, SCL, 5V and GND of the Adafruit Servo Hat of the breakout.
 - The press button is connected to a 10k resistor, between the ground and GPIO 16of the Adafruit Servo Hat of the breakout.
 - The mast led is connected in serie with a 220 ohm resistor between the GPIO 18 and the ground.

# Configure the Pi

## Configure raspbian

Install a fresh Raspbian Stretch Lite on a 16 or 32 GB SD card. Look at this [tutorial](https://www.howtoforge.com/tutorial/howto-install-raspbian-on-raspberry-pi/) if your don't know how to proceed. Don't forget to change the default password and upgrade all packages qith `sudo apt-get update` and `sudo apt-get uprade`.

Use `raspi-config` to enable SSH tunnel (Interfacing options > SSH), and connect your pi to your wifi (Network options > Wifi)

Still in `raspi-config` disable serial console ("5 Interfacing Options" > "P6 Serial" | <No> and then <Yes>) and enable IC2 ("5 Interfacing Options" > "P5 I2C") , and reboot.

Finally connect to you pi through ssh

```bash
$ ssh pi@my-IP-adress
```

## Install the main program and dependencies

### Install the Pi Adafruit Servo Hat driver

Following the [Adafruit tutorial](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library) you can install the Adafruit Servo Hat driver by typing the following commands

```bash
$ cd ~
$ sudo apt-get install -y git build-essential python-dev python-smbus python-pip
$ git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
$ cd Adafruit_Python_PCA9685
$ sudo python setup.py install
```

### Install the Adafruit BNO055 driver

Following the [Adafruit BNO055 tutorial](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black?view=all), type the following commands.

```bash
$ cd ~
$ git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
$ cd Adafruit_Python_BNO055
$ sudo python setup.py install
```

### Cloning SailingBot repository

Install this repository by typing

```bash
$ cd ~
$ git clone https://github.com/cyrpaut/sailingbot.git
```

# Test your parts & connection

## Test parts individually
The `sailingbot/test_parts` folder contains standalone python script to test component one by one. Before you continue executing the script, I strongly encourage you to tests your parts one by one by running the appropriate script.

```bash
$ python test_XXXXX.py 
```

If your part is not working properly, please check you wiring and debug further with the toys examples until all your parts works! Your I2C adresses may not be the same as mine, for instance. Work part by parts until they all worked. In case you changed GPIO or change I2C adresses, modify them in the main code before running it.

## Test your wiki connection to the controlling laptop

MORE TO COME

# Run the code

When the main code will be available, you can run it by typing

```bash
$ python main.py
```

and add this program launched on startup using crontab -e

# Acknowledgements

Many thanks to the people I got inspiration from, including:

 - Adafruit PWM libraries and BNO055 raspberry library, under BSD licence
 - To [Red Hunter](https://www.tindie.com/products/arielnh56/high-resolution-absolute-encoder-128-positions/), who made the absolute orientation encoder and sell it on tindies
 - TheMagPi for [its tutorial on GPS tracer(FR)](https://raspberry-pi.developpez.com/cours-tutoriels/projets-rpi-zero/traceur-gps/) I inspired from
 - To [BlueDot](https://www.bluedot.space/shop/) peoples for making this cool sensor available !!
 - To the many people in the forums, and the large python and raspberry pi community


