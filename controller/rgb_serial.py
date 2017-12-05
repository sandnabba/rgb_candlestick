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
    'bounce': p.bounce,
    'rb': p.rb,
    'cop': p.cop,
}


def run_random(speed):
    print("Starting a random program")
    print(functions.keys())
    program = random.choice(list(functions.keys()))
    print("Starting: ", program)
    functions[program](speed=speed)


if __name__ == "__main__":
    print("Starting RBG serial")

    # We should pic a random function from the functions list
    # and add some random arguments as well

    functions['cop']()

def run(program, speed, direction=None):
    # print("Speed: ", speed.value)
    # print("Direction: ", direction)
    # print("Program type: ", type(program))
    # print("Speed type: ", type(speed))
    # print("direction type: ", type(direction))

    while True:
        if program == "random":
            run_random(speed)
        else:
            functions[program](speed=speed, direction=direction)
