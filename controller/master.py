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

def main():
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting Main Thread")
    speed = Value('i', 1)

    # Start HTTP server:
    messagebus = Queue()
    server = Process(target=httpProcess, args=(messagebus,))
    server.start()
    print("HTTP Server started")


    # Start a default program:
    candle = Process(target=rgb_serial.run, args=("rb", speed))
    candle.start()

    while True:
        print("Waiting for message....")
        data = messagebus.get()

        try:
            if data['program'] != None:
                if candle.is_alive():
                    candle.terminate()
                if data['program'] == "stop":
                    print("Stopping")
                else:
                    # Recreate a new process:
                    candle = Process(target=rgb_serial.run, args=(data['program'], speed))
                    candle.start()
        except KeyError:
            pass

        try:
            if data['speed'] != None:
                print("Setting speed to: ", data['speed'])
                speed.value = int(data['speed'])
        except KeyError:
            pass

    server.join()
    print("Exiting Main Thread")

main()
