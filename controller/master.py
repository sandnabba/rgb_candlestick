#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Global modules:
from multiprocessing import Process, Queue, Value, Array, Event
import time
import queue
import signal
import sys

import logging
logging.basicConfig(level=logging.DEBUG)


# Local files:
from http_server import server as http_server
import rgb_serial

#
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    # self.server.terminate()
    sys.exit(0)

def httpProcess(messagebus):
    logging.info("Starting HTTP process")
    http_server.run(messagebus)

def restart_candle(candle, program, speed, direction):
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

    while True:
        logging.debug("Waiting for message from HTTP server...")
        data = messagebus.get()
        print("Main recieved: ", data)

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
            if data['program'] == "stop":
                print("Stopping")
                candle.terminate()
                candle.join()
                candle = Process(target=rgb_serial.blank)
                candle.start()
            elif data['program'] == "rgb_color":
                print("Stopping for RGB")
                candle.terminate()
                candle.join()
                update = Event()
                candle = Process(target=rgb_serial.color, args=(rgb_color, update))
                candle.start()
            else:
                # Recreate a new process:
                candle = restart_candle(candle, program, speed, direction)

        if 'speed' in data:
            # print("Setting speed to: ", data['speed'])
            speed.value = int(data['speed'])

        if 'color' in data:
            if program != "rgb_color":
                break
            rgb_color[0] = data['color']["r"]
            rgb_color[1] = data['color']["g"]
            rgb_color[2] = data['color']["b"]
            update.set()
            print("Leaving color func")

    server.join()
    logging.info("Exiting Main Thread")

main()
