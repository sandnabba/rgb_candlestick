# Controller software
The controller is a simple Python application that sends an array of bytes (a frame) over a serial connection to the candlestick.
It also provides an HTTP API for use by the web app and external applications.

## Requirements

* Python3
  * pyserial > 3.0
  * flask
* A web server (for the web app)

## Installation

**Note:** There is an Ansible playbook available in the root directory that installs both the web app and the controller application.  
This could be used as a quick and dirty way to get the application running on a Raspberry Pi.

### Python virtual environment

The recommended approach is to use a Python virtual environment:
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Ubuntu/Debian
In an Ubuntu environment, the packages can also be installed system-wide via APT:
```sh
apt-get install python3-flask python3-serial
```

### Serial port permissions
To allow the program to run as a normal user, add yourself to the dialout group:
```sh
sudo usermod -a -G dialout $USER
```

#### Issues
If rgb_candlestick fails with the error `AttributeError: 'Serial' object has no attribute 'in_waiting'`, it indicates that you are using an older version of pyserial. Upgrade to a version greater than 3.0.

## Startup

Launch the application by running `main.py`. A simple debug tool is also available, which can be started with:
```sh
python3 -m controller.debug
```

### Auto Start / Systemd Service
There is a `rgb-candlestick.service` Systemd unit available to run the application as a system service.  
Install it in `/etc/systemd/system/rgb-candlestick.service` and reload Systemd: `systemctl daemon-reload`.

Now the service can be controlled by systemd:
```sh
# Start/stop
systemctl [start|stop|status] rgb-candlestick

# View logs
journalctl -u rgb-candlestick [-f]
```

## API

**WARNING:** The API totally lacks error handling and any kind of data validation.

The API is available on HTTP port `5000` at the `/api` endpoint.  
It currently supports `POST` requests with a JSON body containing the following parameters:

|Parameter|Type|Description|
|-|-|-|
|`program`|string|Program/Pattern. `rb` (rainbow) etc.
|`speed`|integer|How fast the programs are running.
|`direction`|string|Set the direction of some patterns. Supported values: `left`, `right`, `up`, `down`
|`color`|string|Set the whole candlestick to the same color. Accepts a HTML color code (`#aabbcc`)

**Example request**
```
curl -X POST -H "Content-Type: application/json" -d '{"program": "rb"}' http://localhost:5000/api
```

## Candlestick Frame Format

Each light is an RGB diode, requiring 3 bytes: Red, Green, and Blue.  
Frames start with a preamble byte (`255`) and end with a terminator byte (`254`).

<img src="https://docs.google.com/drawings/d/1aIw0J8FX-caLTSyFx5ciofKwaJQVx-R4x_U5gbiJGIU/pub?w=1088&amp;h=238">

The frame shown above sets the first LED to orange and the second to green.  

## Todo / Improvement ideas

- Proper REST API
  - Add a `GET` endpoint in the API to retrieve current settings.
  - Move some logic into the HTTP server.
- Implement brightness level control.
- Add some more pattern. "Fire" would be cool and simple.