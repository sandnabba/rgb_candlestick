#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Global modules:
from multiprocessing import Process, Queue
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
    messagebus = Queue()
    server = Process(target=httpProcess, args=(messagebus,))
    server.start()
    print("HTTP Server started")
    # Start a default program:
    candle = Process(target=rgb_serial.run, args=("studs",))
    candle.start()

    while True:
        print("Waiting for message....")
        program = messagebus.get()
        if candle.is_alive():
            candle.terminate()
        if program == "stop":
            print("Stopping")
        else:
            # Recreate a new process:
            candle = Process(target=rgb_serial.run, args=(program,))
            candle.start()

    server.join()
    print("Exiting Main Thread")

main()
