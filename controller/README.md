# Controller software
The controller is a simple python application sending an array of bytes (a frame) over a serial connection to the candlestick.
It is composed of 3 components
* A master process
* The HTTP-server
* A process that generates light patterns

There is also a simple webapp written in Javascript that communicates with the API.

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

## HTTP API
The HTTP has currently only one endpoint:  
**/api:** Supports POST requests with JSON data with the following parameters:  
`program`: Set the light pattern.  
`speed`: Set the speed of the light pattern.  
`direction`: Set direction of light pattern.  
* Program can also be set to "stop".  

### Examples
Stopp the candlestick:  
`curl -H "Content-Type: application/json" -X POST -d '{"program": "stop"}' 127.0.0.1:5000/api`

Start with random pattern:  
`curl -H "Content-Type: application/json" -X POST -d '{"program": "random"}' 127.0.0.1:5000/api`

### Start the candlestick in the morning and stop during night with cron:
```
$ cat /etc/cron.d/candlestick
# Start candlestick at 05:00 in the morning:
0 5 * * * root curl -v -H "Content-Type: application/json" -X POST -d '{"program": "random"}' 127.0.0.1:5000/api

# Stop Candlestick at 22:30 each night:
30 22 * * * root curl -v -H "Content-Type: application/json" -X POST -d '{"program": "stop"}' 127.0.0.1:5000/api
```


#### Issues
If the rgb_candlestick fails with `AttributeError: 'Serial' object has no attribute 'in_waiting'`, you are running an older version of pyserial. Upgrade to a version > 3.0

## The candlestick frame format
Each light is an RGB diode, requiering 3 bytes, Red, Green and Blue.
Each frame starts with one preamble, a byte of 255 and ends with one byte of 254.  
<img src="https://docs.google.com/drawings/d/1aIw0J8FX-caLTSyFx5ciofKwaJQVx-R4x_U5gbiJGIU/pub?w=1088&amp;h=238">

The frame above would set the first LED to orange, and the second to green.

## Todo
* Add upstart/systemd job
* Add brightness level setting
* GET endpoint in API for getting current settings
