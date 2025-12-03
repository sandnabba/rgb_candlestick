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
import time

from backend_client import BackendClient
import candlestick as rgb_serial

logger = logging.getLogger(__name__)

# Default settings (used on startup and after inactivity timeout)
DEFAULT_PROGRAM = "random"
DEFAULT_SPEED = 10
DEFAULT_DIRECTION = None
DEFAULT_COLOR = None
INACTIVITY_TIMEOUT_SECONDS = 60

# Global state
current_program = DEFAULT_PROGRAM
random_mode = True  # Track if we're in random mode
current_speed = Value('i', DEFAULT_SPEED)
current_direction = DEFAULT_DIRECTION
current_color = DEFAULT_COLOR
candle_process = None
controller = None
backend_client = None  # Global reference to backend client for status updates
last_command_time = None  # Track when the last command was received
# Shared arrays to communicate the actual running state from the subprocess
# Size 20 should be enough for program names and direction
current_program_shared = Array('c', 20)
current_direction_shared = Array('c', 10)


def signal_handler(signal, frame):
    """Handle Ctrl+C gracefully"""
    logger.info('Received interrupt signal, shutting down...')
    if candle_process and candle_process.is_alive():
        candle_process.terminate()
        candle_process.join()
    sys.exit(0)


def restart_candle(program, speed, direction):
    """Restart the candlestick program with new parameters"""
    global candle_process, current_program_shared, current_direction_shared
    
    logger.info(f"Starting/restarting candle: program={program}, speed={speed.value}, direction={direction}")
    
    if candle_process and candle_process.is_alive():
        candle_process.terminate()
        candle_process.join()
    
    # Clear the shared values
    current_program_shared.value = b''
    current_direction_shared.value = b''
    
    candle_process = Process(target=rgb_serial.run_program, args=(program, speed, direction, None, current_program_shared, current_direction_shared))
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


async def handle_backend_command(command: dict):
    """
    Handle commands received from the backend via WebSocket.
    This is called by the BackendClient when a command is received.
    """
    global current_program, random_mode, current_speed, current_direction, current_color, candle_process, controller, backend_client, last_command_time
    
    logger.info(f"Received command from backend: {command}")
    
    # Update last command time for inactivity tracking
    last_command_time = time.time()
    
    try:
        if 'direction' in command:
            current_direction = command['direction']
            restart_candle(current_program, current_speed, current_direction)
        
        if 'program' in command:
            requested_program = command['program']
            random_mode = (requested_program == "random")
            # Clear color when switching to a program (not static color mode)
            current_color = None
            logger.info(f"Switching to program: {requested_program}, random_mode: {random_mode}")
            
            if requested_program == "stop":
                current_program = "stop"
                if candle_process and candle_process.is_alive():
                    candle_process.terminate()
                    candle_process.join()
                candle_process = Process(target=rgb_serial.blank_wrapper)
                candle_process.start()
            else:
                # Don't update current_program yet for random mode - let the monitor task report it
                if not random_mode:
                    current_program = requested_program
                restart_candle(requested_program, current_speed, current_direction)
        
        if 'speed' in command:
            current_speed.value = int(command['speed'])
            logger.info(f"Speed changed to: {current_speed.value}")
        
        if 'color' in command:
            current_color = command['color']
            rgb_color = html_color_to_rgb(current_color)
            logger.info(f"Setting static color: {current_color} -> {rgb_color}")
            
            # When setting static color, we're in a special mode
            current_program = "static_color"
            current_direction = None
            random_mode = False
            
            if candle_process and candle_process.is_alive():
                candle_process.terminate()
                candle_process.join()
            
            # Clear shared values since no animated program is running
            current_program_shared.value = b''
            current_direction_shared.value = b''
            
            candle_process = Process(target=rgb_serial.set_color, args=(controller, rgb_color))
            candle_process.start()
        
        # Send status update back to backend after handling command
        # For random mode with program change, wait for monitor task to report actual program
        should_send_status = True
        if 'program' in command and random_mode and command['program'] == 'random':
            should_send_status = False
            logger.debug("Waiting for monitor task to report actual program in random mode")
        
        if should_send_status and backend_client and backend_client.connected:
            await backend_client.send_status(
                program=current_program,
                random=random_mode,
                speed=current_speed.value,
                direction=current_direction,
                color=current_color
            )
            logger.debug("Sent status update to backend")
            
    except Exception as e:
        logger.error(f"Error handling command: {e}", exc_info=True)


async def monitor_program_changes():
    """
    Background task that monitors the shared program and direction values and sends status updates
    when the actual running state changes (happens in random mode)
    """
    global current_program_shared, current_direction_shared, backend_client, random_mode, current_direction, current_program
    
    last_reported_program = ""
    last_reported_direction = ""
    
    while True:
        await asyncio.sleep(0.5)  # Check every 0.5 seconds for faster updates
        
        if not backend_client or not backend_client.connected:
            continue
        
        # Read the actual running program and direction from shared memory
        try:
            actual_program = current_program_shared.value.decode('utf-8').rstrip('\x00')
            actual_direction = current_direction_shared.value.decode('utf-8').rstrip('\x00')
            
            # Only send updates if we have a program running (not in static color mode)
            if actual_program and (actual_program != last_reported_program or actual_direction != last_reported_direction):
                logger.info(f"State changed - program: {actual_program}, direction: {actual_direction}, random_mode: {random_mode}")
                last_reported_program = actual_program
                last_reported_direction = actual_direction
                
                # Update global values if they changed
                if actual_direction:
                    current_direction = actual_direction
                if actual_program:
                    current_program = actual_program
                
                # Send status update with the actual program and direction
                await backend_client.send_status(
                    program=actual_program,
                    random=random_mode,
                    speed=current_speed.value,
                    direction=actual_direction if actual_direction else current_direction,
                    color=current_color
                )
        except Exception as e:
            logger.error(f"Error monitoring program changes: {e}")


async def reset_to_defaults():
    """
    Reset the candlestick to default settings.
    Called after inactivity timeout or can be called manually.
    """
    global current_program, random_mode, current_speed, current_direction, current_color, backend_client
    
    logger.info("Resetting to default settings")
    
    current_program = DEFAULT_PROGRAM
    random_mode = True
    current_speed.value = DEFAULT_SPEED
    current_direction = DEFAULT_DIRECTION
    current_color = DEFAULT_COLOR
    
    # Restart with default program
    restart_candle(current_program, current_speed, current_direction)
    
    # Send status update to backend
    if backend_client and backend_client.connected:
        await backend_client.send_status(
            program=current_program,
            random=random_mode,
            speed=current_speed.value,
            direction=current_direction,
            color=current_color
        )
        logger.info("Sent default status to backend after reset")


async def monitor_inactivity(timeout_seconds: int = INACTIVITY_TIMEOUT_SECONDS):
    """
    Background task that monitors for inactivity and resets to defaults
    after timeout_seconds of no commands from the frontend.
    
    Args:
        timeout_seconds: Seconds of inactivity before resetting to defaults
    """
    global last_command_time
    
    while True:
        await asyncio.sleep(5)  # Check every 5 seconds
        
        # Skip if no command has been received yet (still on defaults)
        if last_command_time is None:
            continue
        
        # Check if we've exceeded the inactivity timeout
        elapsed = time.time() - last_command_time
        if elapsed >= timeout_seconds:
            logger.info(f"Inactivity timeout reached ({timeout_seconds}s), resetting to defaults")
            await reset_to_defaults()
            # Reset the timer to prevent repeated resets
            last_command_time = None


async def run_with_backend(backend_url: str, candlestick_id: str, inactivity_timeout: int = INACTIVITY_TIMEOUT_SECONDS):
    """
    Main async function that runs the controller with backend connection.
    
    Args:
        backend_url: WebSocket URL of the backend server
        candlestick_id: Unique identifier for this candlestick
        inactivity_timeout: Seconds of inactivity before resetting to defaults
    """
    global candle_process, controller, current_program, current_speed, current_direction, backend_client
    
    logger.info("Starting controller with backend connection")
    
    # Initialize serial controller
    controller = rgb_serial.SerialController()
    
    # Start default program
    candle_process = restart_candle(current_program, current_speed, current_direction)
    
    # Initialize backend client and store globally
    backend_client = BackendClient(
        backend_url=backend_url,
        candlestick_id=candlestick_id,
        command_callback=handle_backend_command
    )
    
    # Send initial status
    await backend_client.connect()
    if backend_client.connected:
        logger.info(f"Sending initial status: program={current_program}, random={random_mode}, speed={current_speed.value}, direction={current_direction}, color={current_color}")
        await backend_client.send_status(
            program=current_program,
            random=random_mode,
            speed=current_speed.value,
            direction=current_direction,
            color=current_color
        )
        logger.info("Initial status sent")
    
    # Start background task to monitor program changes
    monitor_task = asyncio.create_task(monitor_program_changes())
    
    # Start background task to monitor inactivity and reset to defaults
    inactivity_task = asyncio.create_task(monitor_inactivity(inactivity_timeout))
    
    # Run the client (this will keep reconnecting if connection is lost)
    try:
        await backend_client.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        monitor_task.cancel()
        inactivity_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        try:
            await inactivity_task
        except asyncio.CancelledError:
            pass
        
        await backend_client.disconnect()
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
    inactivity_timeout = args.inactivity_timeout or int(os.getenv('INACTIVITY_TIMEOUT', str(INACTIVITY_TIMEOUT_SECONDS)))
    
    logger.info(f"Backend URL: {backend_url}")
    logger.info(f"Candlestick ID: {candlestick_id}")
    logger.info(f"Inactivity timeout: {inactivity_timeout}s")
    
    # Run the async application
    try:
        asyncio.run(run_with_backend(backend_url, candlestick_id, inactivity_timeout))
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
    parser.add_argument(
        '--inactivity-timeout',
        type=int,
        help=f"Seconds of inactivity before resetting to defaults (default: {INACTIVITY_TIMEOUT_SECONDS} or INACTIVITY_TIMEOUT env var)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
