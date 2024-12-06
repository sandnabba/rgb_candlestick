#!/usr/bin/env python3

'''
Quick and dirty debug script. Useful when troubleshooting or developing new patterns.
Use as `python -m candlestick.debug` from a parent directory
'''

import logging
from multiprocessing import Value
from .serial_controller import SerialController
from .patterns import *
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

functions = {
    'fall': fall,
    'wave': wave,
    'bounce': bounce,
    'cop': cop,
    'rb': rb,
}

if __name__ == "__main__":
    controller = SerialController()

    # The speed parameter must be a multiprocessing.Value() so that
    # it can be dynamically set in the web UI. It's accessed with `speed.value`
    speed = Value("i", 10)

    while True:
        #functions['bounce'](controller=controller, speed=speed, direction="left")
        functions['rb'](controller=controller, speed=speed, direction="left")