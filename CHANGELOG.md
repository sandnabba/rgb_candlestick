# 2025.12

Reversed controller architecture. The candlestick now connects to the controller, instead of the controller connecting to the candlestick.  
The main frontend was moved to a standalone web app, which can run on another computer.

* Added candlestick state tracking to the controller  
* Frontend displays the current state of the candlestick (with live updates)  
* Docker files added  
* Minor frontend updates (icons)

# Version 2 (2024.12)

2024–2025 season. First official “release” and major update.

* Renamed branches from `master` to `main`  
* Updated frontend from Mithril to React  
* Proper Python package for the serial and RGB controller  
* Logging implemented using the `logging` module  
* Lots of improvements and cleanup  
* systemd unit added  
* Ansible playbook added  

All software is still running on the Raspberry Pi.

# Version 1 (≈ 2017–2023)

First version, with a very hacky setup.

Arduino Nano–based candlestick hardware.  
Raspberry Pi as the controller, with a web app built using the Mithril framework.

