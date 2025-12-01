"""
WebSocket client for connecting the controller to the backend.
Maintains a persistent connection and handles commands from the backend.
"""

import asyncio
import websockets
import json
import logging
from typing import Optional, Callable, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class BackendClient:
    """WebSocket client that connects the controller to the backend"""
    
    def __init__(
        self,
        backend_url: str,
        candlestick_id: str,
        command_callback: Callable[[Dict[str, Any]], None]
    ):
        """
        Initialize the backend client.
        
        Args:
            backend_url: WebSocket URL of the backend (e.g., 'ws://localhost:8000')
            candlestick_id: Unique identifier for this candlestick
            command_callback: Function to call when receiving commands from backend
        """
        self.backend_url = backend_url
        self.candlestick_id = candlestick_id
        self.command_callback = command_callback
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.connected = False
        self.reconnect_delay = 5  # seconds
        self.heartbeat_interval = 30  # seconds
        self._running = False
        
    async def connect(self):
        """Establish WebSocket connection to the backend"""
        ws_url = f"{self.backend_url}/ws/{self.candlestick_id}"
        logger.info(f"Connecting to backend at {ws_url}")
        
        try:
            self.websocket = await websockets.connect(ws_url)
            self.connected = True
            logger.info("Connected to backend successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to backend: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Close the WebSocket connection"""
        self._running = False
        if self.websocket and not self.websocket.closed:
            await self.websocket.close()
        self.connected = False
        logger.info("Disconnected from backend")
    
    async def send_status(
        self,
        program: Optional[str] = None,
        random: Optional[bool] = None,
        speed: Optional[int] = None,
        direction: Optional[str] = None,
        color: Optional[str] = None
    ):
        """Send status update to the backend"""
        if not self.connected or not self.websocket:
            logger.warning("Cannot send status - not connected to backend")
            return
        
        message = {
            "type": "status",
            "program": program,
            "random": random,
            "speed": speed,
            "direction": direction,
            "color": color
        }
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.info(f"Sent status update: {message}")
        except Exception as e:
            logger.error(f"Failed to send status: {e}")
            self.connected = False
    
    async def send_heartbeat(self):
        """Send heartbeat to keep connection alive"""
        if not self.connected or not self.websocket:
            return
        
        message = {"type": "heartbeat"}
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.debug("Sent heartbeat")
        except Exception as e:
            logger.error(f"Failed to send heartbeat: {e}")
            self.connected = False
    
    async def receive_messages(self):
        """Receive and process messages from the backend"""
        if not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    logger.debug(f"Received message: {data}")
                    
                    if data.get("type") == "command":
                        # Pass command to callback (handle both sync and async callbacks)
                        if asyncio.iscoroutinefunction(self.command_callback):
                            await self.command_callback(data)
                        else:
                            self.command_callback(data)
                    else:
                        logger.warning(f"Unknown message type: {data.get('type')}")
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")
            self.connected = False
    
    async def heartbeat_loop(self):
        """Send periodic heartbeats to the backend"""
        while self._running:
            if self.connected:
                await self.send_heartbeat()
            await asyncio.sleep(self.heartbeat_interval)
    
    async def run(self):
        """
        Main run loop with automatic reconnection.
        This maintains the connection and handles reconnection on failure.
        """
        self._running = True
        
        while self._running:
            if not self.connected:
                # Try to connect/reconnect
                success = await self.connect()
                if not success:
                    logger.info(f"Retrying connection in {self.reconnect_delay} seconds...")
                    await asyncio.sleep(self.reconnect_delay)
                    continue
            
            # Start heartbeat task
            heartbeat_task = asyncio.create_task(self.heartbeat_loop())
            
            # Receive messages (blocks until disconnection)
            await self.receive_messages()
            
            # Cancel heartbeat task
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass
            
            # Connection lost, retry
            if self._running:
                logger.info(f"Connection lost. Reconnecting in {self.reconnect_delay} seconds...")
                await asyncio.sleep(self.reconnect_delay)
        
        # Cleanup
        if self.websocket:
            await self.websocket.close()
