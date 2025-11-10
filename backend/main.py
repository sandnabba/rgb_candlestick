#!/usr/bin/env python3

import uvicorn
import argparse
import logging

# Import the app instance so uvicorn can find it when running "uvicorn main:app"
from app import app

def setup_logging(log_level: str):
    """Configure logging level based on user input."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    log_format = "%(asctime)s - %(name)-20s - %(levelname)-6s - %(message)s"
    logging.basicConfig(level=numeric_level, format=log_format)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="RGB Candlestick Backend Server")
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Set the logging level (default: INFO)"
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help="Enable auto-reload on code changes"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    setup_logging(args.log_level)
    
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower()
    )
