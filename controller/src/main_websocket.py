#!/usr/bin/env python3
"""
Controller application with WebSocket backend connection.
This version connects to a central backend server instead of running a local HTTP server.
"""

from multiprocessing import Process, Queue, Value, Array
import signal
import sys
import argparse
import logging
import asyncio
import os

from backend_client import BackendClient
import candlestick as rgb_serial

logger = logging.getLogger(__name__)

# Global state
current_program = "random"
current_speed = Value('i', 10)
current_direction = None
current_color = None
candle_process = None
controller = None


def signal_handler(signal, frame):
    """Handle Ctrl+C gracefully"""
    logger.info('Received interrupt signal, shutting down...')
    if candle_process and candle_process.is_alive():
        candle_process.terminate()
        candle_process.join()
    sys.exit(0)


def restart_candle(program, speed, direction):
    """Restart the candlestick program with new parameters"""
    global candle_process
    
    logger.info(f"Starting/restarting candle: program={program}, speed={speed.value}, direction={direction}")
    
    if candle_process and candle_process.is_alive():
        candle_process.terminate()
        candle_process.join()
    
    candle_process = Process(target=rgb_serial.run_program, args=(program, speed, direction))
    candle_process.start()
    return candle_process


def html_color_to_rgb(color_code):
    """Convert HTML color code to RGB array"""
    if color_code.startswith('#'):
        color_code = color_code[1:]
    
    red = int(color_code[0:2], 16)
    green = int(color_code[2:4], 16)
    blue = int(color_code[4:6], 16)
    
    return [red, green, blue]


def handle_backend_command(command: dict):
    """
    Handle commands received from the backend via WebSocket.
    This is called by the BackendClient when a command is received.
    """
    global current_program, current_speed, current_direction, current_color, candle_process, controller
    
    logger.info(f"Received command from backend: {command}")
    
    try:
        if 'direction' in command:
            current_direction = command['direction']
            restart_candle(current_program, current_speed, current_direction)
        
        if 'program' in command:
            current_program = command['program']
            logger.info(f"Switching to program: {current_program}")
            
            if current_program == "stop":
                if candle_process and candle_process.is_alive():
                    candle_process.terminate()
                    candle_process.join()
                candle_process = Process(target=rgb_serial.blank)
                candle_process.start()
            else:
                restart_candle(current_program, current_speed, current_direction)
        
        if 'speed' in command:
            current_speed.value = int(command['speed'])
            logger.info(f"Speed changed to: {current_speed.value}")
        
        if 'color' in command:
            current_color = command['color']
            rgb_color = html_color_to_rgb(current_color)
            logger.info(f"Setting static color: {current_color} -> {rgb_color}")
            
            if candle_process and candle_process.is_alive():
                candle_process.terminate()
                candle_process.join()
            
            candle_process = Process(target=rgb_serial.set_color, args=(controller, rgb_color))
            candle_process.start()
            
    except Exception as e:
        logger.error(f"Error handling command: {e}", exc_info=True)


async def run_with_backend(backend_url: str, candlestick_id: str):
    """
    Main async function that runs the controller with backend connection.
    """
    global candle_process, controller, current_program, current_speed, current_direction
    
    logger.info("Starting controller with backend connection")
    
    # Initialize serial controller
    controller = rgb_serial.SerialController()
    
    # Start default program
    candle_process = restart_candle(current_program, current_speed, current_direction)
    
    # Initialize backend client
    client = BackendClient(
        backend_url=backend_url,
        candlestick_id=candlestick_id,
        command_callback=handle_backend_command
    )
    
    # Send initial status
    await client.connect()
    if client.connected:
        await client.send_status(
            program=current_program,
            speed=current_speed.value,
            direction=current_direction,
            color=current_color
        )
    
    # Run the client (this will keep reconnecting if connection is lost)
    try:
        await client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        await client.disconnect()
        if candle_process and candle_process.is_alive():
            candle_process.terminate()
            candle_process.join()


def main():
    """Main entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    
    args = parse_args()
    setup_logging(args.log_level)
    
    logger.info("Starting RGB Candlestick Controller with WebSocket backend")
    
    # Get configuration from command line or environment
    backend_url = args.backend_url or os.getenv('BACKEND_URL', 'ws://localhost:8000')
    candlestick_id = args.candlestick_id or os.getenv('CANDLESTICK_ID', 'candlestick_001')
    
    logger.info(f"Backend URL: {backend_url}")
    logger.info(f"Candlestick ID: {candlestick_id}")
    
    # Run the async application
    try:
        asyncio.run(run_with_backend(backend_url, candlestick_id))
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0


def setup_logging(log_level: str):
    """Configure logging level based on user input"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    log_format = "{name:<20} - {levelname:<6} - {message}"
    logging.basicConfig(level=numeric_level, format=log_format, style='{')


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="RGB Candlestick Controller - WebSocket Backend Mode"
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the logging level (default: INFO)"
    )
    parser.add_argument(
        '--backend-url',
        help="WebSocket URL of the backend server (default: ws://localhost:8000 or BACKEND_URL env var)"
    )
    parser.add_argument(
        '--candlestick-id',
        help="Unique identifier for this candlestick (default: candlestick_001 or CANDLESTICK_ID env var)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
