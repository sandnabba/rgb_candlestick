#!/usr/bin/env python3

'''
Quick and dirty debug script. Useful when troubleshooting or developing new patterns.
Use as `python -m candlestick.debug` from a parent directory
'''

import logging
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
    while True:
        functions['wave'](controller=controller, direction="left")