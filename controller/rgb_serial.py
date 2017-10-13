#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import time
from time import sleep
from serial_controller import rgb_patterns as p
import sys
import random

functions = {
    'fall': p.fall,
    'wave': p.wave,
    'studs': p.studs
}

if __name__ == "__main__":
    print("Starting RBG serial")

    # We should pic a random function from the functions list
    # and add some random arguments as well

    functions['wave']()
    functions['fall']()

def run(program):
    while True:
        functions[program]()
