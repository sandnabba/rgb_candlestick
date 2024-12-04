#!/usr/bin/env python3

import random
import logging
import sys
from .serial_controller import SerialController
from .patterns import *
logger = logging.getLogger(__name__)

functions = {
    'fall': fall,
    'wave': wave,
    'bounce': bounce,
    'cop': cop,
    'rb': rb,
    # This is a terribly uggly hack to show the rainbow a bit more often.
    # This should be solved within `run_random` instead!
    'rb2': rb,
}

def run_random(controller, speed=10):
    program = random.choice(list(functions.keys()))
    logger.info("Random program, Starting: %s", program)
    functions[program](controller, speed=speed)

def run_program(program, speed, direction=None, rgb_color=None, update=None):
    '''This function is called when the script is run externally'''
    controller = SerialController()
    # print("Speed: ", speed.value)
    # print("Direction: ", direction)
    # print("Program type: ", type(program))
    # print("Speed type: ", type(speed))
    # print("direction type: ", type(direction))

    while True:
        if program == "random":
            run_random(controller, speed)
        else:
            functions[program](controller=controller, speed=speed, direction=direction)

def blank():
    logger.info("Starting blank function")
    p.blank()

def set_color(controller, rgb_color):
    #controller = SerialController()
    logger.info("Setting color to static value from API")
    set_color_from_api(controller, rgb_color)

if __name__ == "__main__":
    logger.info("Starting RBG serial")
    controller = SerialController()
    # Uncomment to start with a specific function:
    # functions['cop'](controller)
    while True:
        run_random(controller=controller)