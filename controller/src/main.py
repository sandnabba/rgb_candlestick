#!/usr/bin/env python3

from multiprocessing import Process, Queue, Value, Array, Event
from queue import Empty
import signal
import sys
import argparse
import logging

from http_server import server as http_server
import candlestick as rgb_serial

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
    candle = Process(target=rgb_serial.run, args=(program, speed, direction))
    candle.start()
    return(candle)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    logging.info("Starting Mail Thread")

    # Defaults:
    speed = Value('i', 10)
    rgb_color = Array('i', [250, 250, 250])
    direction = None
    program = "random"

    # Start HTTP server:
    messagebus = Queue()
    server = Process(target=httpProcess, args=(messagebus,))
    server.start()
    logging.info("HTTP Server started")

    # Start a default program:
    candle = Process(target=rgb_serial.run, args=(program, speed, direction))
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
                rgb_color[0] = data['color']["r"]
                rgb_color[1] = data['color']["g"]
                rgb_color[2] = data['color']["b"]
                if program == "rgb_color":
                    # Do net set the Event() function unless something is listening
                    # on the event, or the process will hit a deadlock here.
                    update.set()
                else:
                    candle.terminate()
                    candle.join()
                    update = Event()
                    candle = Process(target=rgb_serial.color, args=(rgb_color, update))
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

    # We are probably never getting down here:
    server.join()
    logging.info("Exiting Main Thread")

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
    logging.basicConfig(level=numeric_level)


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
    main()
