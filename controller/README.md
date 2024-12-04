# Controller software
The controller is a simple Python application that sends an array of bytes (a frame) over a serial connection to the candlestick.
It also has a HTTP API that is used by the web app (and external applications)

## Requirements

* Python3
  * pyserial > 3.0
  * flask
* A web server (for the web app)

## Installation

The recommended approach is to use a Python virtual env:
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Ubuntu
In an Ubuntu environment, the packages can be installed system wide from APT:  
`apt-get install python3-flask python3-serial`

### Serial port permissions
To be able to run the program as a normal user, add yourself to the dialout group:  
`sudo usermod -a -G dialout $USER`

#### Issues
If the rgb_candlestick fails with `AttributeError: 'Serial' object has no attribute 'in_waiting'`, you are running an older version of pyserial. Upgrade to a version > 3.0

## API

**WARNING:** The API totally lacks error handling or any kind of sanity check of the data.

The API is available at HTTP port `5000` on the `/api` URL.
It currently only supports `POST` requests with a JSON body, supporting the following parameters:

|Parameter|Type|Description|
|-|-|-|
|`program`|string|Program/Pattern. `rb` (rainbow) etc.
|`speed`|integer|How fast the programs are running.
|`direction`|sting|Set the direction of some patterns. Supported values: `left`, `right`

**Example**
```
curl -X POST -H "Content-Type: application/json" -d '{"program": "rb"}' http://localhost:5000/api
```

## The candlestick frame format
Each light is an RGB diode, requiring 3 bytes: Red, Green and Blue.
Each frame starts with a preamble byte of 255 and ends with a byte of 254.  
<img src="https://docs.google.com/drawings/d/1aIw0J8FX-caLTSyFx5ciofKwaJQVx-R4x_U5gbiJGIU/pub?w=1088&amp;h=238">

The frame above would set the first LED to orange, and the second to green.

## Todo
* Add upstart/systemd job
* Add brightness level setting
* GET endpoint in API for getting current settings
