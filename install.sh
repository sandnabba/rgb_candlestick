#!/bin/bash

mkdir /opt/candlestick_controller
cp -rv http_server/ \
       	master.py \
       	rgb_serial.py \
	serial_controller/ \
       	/opt/candlestick_controller/

cp -rv webapp/build/ /opt/candlestick_controller/webapp
chmod -R 755 /opt/candlestick_controller/webapp
chmod -R 755 /opt/candlestick_controller
