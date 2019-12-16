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
    'rb2': p.rb, # Extra rainbow, just because it's beautiful :)
}


def run_random(speed=10):
    program = random.choice(list(functions.keys()))
    print("Random program, Starting: ", program)
    functions[program](speed=speed)


if __name__ == "__main__":
    print("Starting RBG serial")
    functions['cop']()
    # functions['wave']()
    while True:
        run_random()


def run(program, speed, direction=None, rgb_color=None, update=None):
    # print("Speed: ", speed.value)
    # print("Direction: ", direction)
    # print("Program type: ", type(program))
    # print("Speed type: ", type(speed))
    # print("direction type: ", type(direction))

    while True:
        if program == "random":
            run_random(speed)
        if program == "rgb_color":
            p.rgb_color(rgb_color=rgb_color, update=update)
        else:
            functions[program](speed=speed, direction=direction)

def blank():
    print("Starting blank function")
    p.blank()
