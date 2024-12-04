#!/usr/bin/env python3

from multiprocessing import Process, Queue, Value, Array, Event
from queue import Empty
import signal
import sys
import argparse
import logging
import traceback

from http_server import server as http_server
import candlestick as rgb_serial

'''
This file should be refactored into a proper class `class Candlestick()`
Some of the HTTP logic should also me moved to the HTTP server.

`rgb_serial` was the old "package" name, before it was an actual package.
It's kept for legacy reasons

The SerialController class should probably be instantiated here as well.
'''

# Functions:
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    # We should probably terminate the serial connection here
    sys.exit(0)

def httpProcess(messagebus):
    logging.info("Starting HTTP process")
    http_server.run(messagebus)

def restart_candle(candle, program, speed, direction):
    logging.info("Restarting candle")
    if candle.is_alive():
        candle.terminate()
        candle.join()
    candle = Process(target=rgb_serial.run_program, args=(program, speed, direction))
    candle.start()
    return(candle)

def html_color_to_rgb(color_code):
    # Ensure the color code starts with '#'
    if color_code.startswith('#'):
        color_code = color_code[1:]

    # Split the color code into its RGB components and convert them to decimal
    red = int(color_code[0:2], 16)
    green = int(color_code[2:4], 16)
    blue = int(color_code[4:6], 16)

    # Return the RGB components as an array
    return [red, green, blue]

def main():
    signal.signal(signal.SIGINT, signal_handler)
    logging.info("Starting Main Thread")
    controller = rgb_serial.SerialController()

    # Defaults:
    speed = Value('i', 10)
    rgb_color = Array('i', [250, 250, 250]) # This is a multiprocessing Array
    direction = None
    program = "random"

    # Start HTTP server:
    messagebus = Queue()
    server = Process(target=httpProcess, args=(messagebus,))
    server.start()
    logging.info("HTTP Server started")

    # Start a default program:
    candle = Process(target=rgb_serial.run_program, args=(program, speed, direction))
    candle.start()

    # State:
    program_override = False

    while True:
        logging.info("Waiting for message from HTTP server...")
        try:
            data = messagebus.get(timeout=60)
            logging.debug("Main recieved: %s", data)
            program_override = True

            if 'direction' in data:
                if data['direction'] == "left":
                    direction = "left"
                if data['direction'] == "right":
                    direction = "right"
                if data['direction'] == "up":
                    direction = "up"
                if data['direction'] == "down":
                    direction = "down"
                # print("Setting direction to: ", direction)
                candle = restart_candle(candle, program, speed, direction)

            if 'program' in data:
                program = data['program']
                logging.info("Recieved program %s from API", program)
                if data['program'] == "stop":
                    # This function does not work after refactoring the serial_controller.
                    # It should probably be implemented in a new endpoint.
                    print("Stopping")
                    candle.terminate()
                    candle.join()
                    candle = Process(target=rgb_serial.blank)
                    candle.start()
                else:
                    # Recreate a new process:
                    candle = restart_candle(candle, program, speed, direction)

            if 'speed' in data:
                # print("Setting speed to: ", data['speed'])
                speed.value = int(data['speed'])

            if 'color' in data:
                '''Here we are receiving a HTML color code from the API'''
                rgb_color = html_color_to_rgb(data['color'])
                logging.debug("Starting set_color function with initial color: %s", rgb_color)
                candle.terminate()
                candle.join()
                candle = Process(target=rgb_serial.set_color, args=(controller, rgb_color))
                candle.start()

        except Empty:
            if program_override:
                # Reset candle to default if we haven't got a API call:
                logging.info("No event received within 1 minute. Restarting and resetting")
                speed = Value('i', 10)
                direction = None
                program = "random"
                candle = candle = restart_candle(candle, program, speed, direction)
                program_override = False

        except Exception as e:
            print("Unknown exception occurred:")
            print(e)
            traceback.print_exc()
            print("Exiting")
            sys.exit(1)
            print("Returning")
            return(1)

def setup_logging(log_level: str):
    """
    Configures the logging level based on user input.
    
    Args:
        log_level (str): The logging level provided by the user.
    """
    print(f"Setting log level {log_level}")
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    log_format = "{name:<20} - {levelname:<6} - {message}"
    logging.basicConfig(level=numeric_level, format=log_format, style='{')

def parse_args():
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="A script with log level argument parsing.")
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the logging level (default: INFO)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.log_level)
    sys.exit(main())
