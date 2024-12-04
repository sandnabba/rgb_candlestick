# An RGB Candlestick for Christmas
This is the code and a short how-to on how I made my RGB LED candlestick for christmas.

[![YouTube Video](http://i.imgur.com/g4cEDqO.png)](http://www.youtube.com/watch?feature=player_embedded&v=RDOWLQ8P0aQ)

### Features:
* Can be controlled by any computer with Python support and a USB port.
* Single cable for both power and programming.
* Simple interface between the candlestick and controller.
* Easy to add new features and light-patterns.

### Design
Today the project is built with two main components, the candlestick and the control software.
Since it's much easier to rewrite the Python code than to compile and flash the Arduino code, most of the intelligence resides in the controller.

#### Candlestick
The candlestick is designed to be easy and inexpensive to build, simple to use, and very reliable. It is:
* Powered and controlled through a USB interface.
* Uses a serial over USB interface to the controller.
* Accepts a byte-array with values for each LED from the controller.

The version 2 of the candlestick uses a single Arduino Nano, but any Arduino, ESP32 or similar would work as long as it has a USB port and fits within the candlestick.
The leds are 5mm WS2812 (NeoPixel compatible) RGB Leds.

[Build instructions](/candlestick)

#### Controller
The controller software is written in Python, and is verified to work on both generic x86 and ARM (Raspberry Pi)

For more information, see the [controllers README](/controller/)

## Todo / Improvement ideas

Everything is terribly hacky. Remember that this is a weekend project setup a some week before Christmas, eventually with small improvements "next year".

* Make the number of LEDs dynamic
  * Support for multiple candlesticks in the controller software.
  * Add a "super controller" that can command multiple candlesticks over network.
* Implement basic light patterns in the Arduino code so that it can run without a dedicated controller.
* Implement a GET function in the API so that the web app can retrieve the current state of the candlestick.
