#!/usr/bin/env python3

import random
import logging
import sys
from .serial_controller import SerialController
from .patterns import *
from .patterns import directions  # Import directions list for random selection
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

def run_random(controller, speed=10, current_program_shared=None, current_direction_shared=None):
    # Normalize rb2 to rb for reporting
    program_choices = list(functions.keys())
    program = random.choice(program_choices)
    
    # Pick a random direction
    direction = random.choice(directions)
    
    # Normalize rb2 to rb for status reporting
    program_to_report = 'rb' if program == 'rb2' else program
    
    logger.info("Random program, Starting: %s with direction: %s", program_to_report, direction)
    
    # Update shared values so parent process knows what's running
    if current_program_shared is not None:
        current_program_shared.value = program_to_report.encode('utf-8')
    if current_direction_shared is not None:
        current_direction_shared.value = direction.encode('utf-8')
    
    functions[program](controller, speed=speed, direction=direction)

def run_program(program, speed, direction=None, rgb_color=None, current_program_shared=None, current_direction_shared=None):
    '''This function is called when the script is run externally'''
    controller = SerialController()
    
    # If no direction specified, pick a random one
    if direction is None:
        direction = random.choice(directions)

    while True:
        if program == "random":
            run_random(controller, speed, current_program_shared, current_direction_shared)
        else:
            # Update shared values with the specific program and direction
            if current_program_shared is not None:
                current_program_shared.value = program.encode('utf-8')
            if current_direction_shared is not None:
                current_direction_shared.value = direction.encode('utf-8')
            functions[program](controller=controller, speed=speed, direction=direction)

def blank_wrapper():
    """Wrapper for the blank function to be called from main_websocket"""
    logger.info("Starting blank function")
    blank()

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