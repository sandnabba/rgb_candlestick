# Controller software
The controller is a simple python application sending an array of bytes (a frame) over a serial connection to the candlestick.

## The candlestick frame format
Each light is an RGB diode, requiering 3 bytes, Red, Green and Blue.
Each frame starts with one preamble, a byte of 255 and ends with one byte of 254.  
<img src="https://docs.google.com/drawings/d/1aIw0J8FX-caLTSyFx5ciofKwaJQVx-R4x_U5gbiJGIU/pub?w=1088&amp;h=238">

The frame above would set the first LED to orange, and the second to green.
