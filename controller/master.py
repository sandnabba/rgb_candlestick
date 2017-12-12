#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Global modules:
from multiprocessing import Process, Queue, Value
import time
import queue
import signal
import sys

# Local files:
from http_server import server as http_server
import rgb_serial

#
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    # self.server.terminate()
    sys.exit(0)

def httpProcess(messagebus):
    print("Starting httpProcess")
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
    print("Starting Main Thread")

    # Defaults:
    speed = Value('i', 10)
    # direction = "left"
    direction = None
    program = "random"

    # Start HTTP server:
    messagebus = Queue()
    server = Process(target=httpProcess, args=(messagebus,))
    server.start()
    print("HTTP Server started")


    # Start a default program:
    candle = Process(target=rgb_serial.run, args=(program, speed, direction))
    candle.start()

    while True:
        print("Waiting for message....")
        data = messagebus.get()
        # print("Main recieved: ", data)

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
            else:
                # Recreate a new process:
                candle = restart_candle(candle, program, speed, direction)

        if 'speed' in data:
            # print("Setting speed to: ", data['speed'])
            speed.value = int(data['speed'])


    server.join()
    print("Exiting Main Thread")

main()
