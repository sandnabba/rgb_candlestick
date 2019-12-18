# The RGB Candlestick for Christmas
This is the code and a short howto about how I made my RGB LED candlestick for last christmas.

[![YouTube Video](http://i.imgur.com/g4cEDqO.png)](http://www.youtube.com/watch?feature=player_embedded&v=RDOWLQ8P0aQ)

### Features:
* Can be controlled by any computer with Python support and an USB port.
* Single cable for both power and programming
* Simple interface between candlestick and controller.
* Easy to add new features and light-patterns.

### Design
Today the project is built up by 2 main components, the candlestick and the control software.
Since it's a lot easier to rewrite the python code then compiling and flashing the Arduio code, most of the intelligence resides in the controller.

#### Candlestick
The candlestick is designed to be easy and inexpensive to build, simple to use and very reliable. It is:
* Both powered and controlled through a USB interface.
* Using a serial over USB interface to the controller.
* Accepting a byte-array with values for each LED from the controller.

The version 2 of the candlestick is using a single Arduino Nano, but any arduino would work as long as it has a USB port and fits within the candlestick.
The leds are 5mm WS2812 (NeoPixel compatible) RGB Leds.

[Build instructions](/candlestick)

#### Controller
The controller software is written in Python, and is verified to work on both generic X86 and ARM (Raspberry Pi)

For more information, see the [controllers README](/controller/)

## Todo
* Add a virtual env for the controller, so that we don't need to install system packages.
* Make the number of LEDs dynamic
  * Support for multiple candlesticks in the controller software.
  * Add a "super controller" that can command multiple candlesticks over network.
* Implement basic light patterns in the Arduino code so that it can run without a dedicated controller.
* Implement a GET function in the API so that the webapp can get the current state of the candlestick.
