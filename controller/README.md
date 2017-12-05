# Controller software
The controller is a simple python application sending an array of bytes (a frame) over a serial connection to the candlestick.

## Requirements

* Python3
  * pyserial > 3.0
  * flask
* A webserver (for the webapp)

### Ubuntu / Debian
First install the necessary dependencies:  
`apt-get install python3-flask python3-serial`

To be able to run the program as user, add your self to the dialout group:  
`sudo usermod -a -G dialout $USER`

#### Issues
If the rgb_candlestick fails with `AttributeError: 'Serial' object has no attribute 'in_waiting'`, you are running an older version of pyserial. Upgrade to a version > 3.0

## The candlestick frame format
Each light is an RGB diode, requiering 3 bytes, Red, Green and Blue.
Each frame starts with one preamble, a byte of 255 and ends with one byte of 254.  
<img src="https://docs.google.com/drawings/d/1aIw0J8FX-caLTSyFx5ciofKwaJQVx-R4x_U5gbiJGIU/pub?w=1088&amp;h=238">

The frame above would set the first LED to orange, and the second to green.
