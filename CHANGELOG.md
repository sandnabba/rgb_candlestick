# 2025.12

Reversed controller architecture. Now the candlestick connects to the controller, instead of the controller connecting to the candlestick.
Main frontend moved to stand alone webapp which could run on another computer.

* Added candlestick state tracking to the controller.
* Frontend displays current state of the candlestick (+ updates)
* Docker files added
* Minor frontend updates (icons)

# Version 2 (2024.12): 

2024-2025 season. First official "release" and major update.

* Renamed branches from master -> main
* Updated frontend from Mithril -> React
* Proper Python package for serial and RGB controller.
* Logging using logging module
* Lots of improvements and clean up
* Systemd unit added
* Ansible playbook added

All software still running on the Raspberry pi.

# Version 1 - Pre 2023

Arduino nano candlestick hardware. 
