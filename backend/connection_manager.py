"""
WebSocket Connection Manager
Manages active WebSocket connections and candlestick states.
"""

from fastapi import WebSocket
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import asyncio
import json

from models import CandlestickState, CandlestickCommand, MessageType

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections and candlestick states"""
    
    def __init__(self):
        # Active controller WebSocket connections: candlestick_id -> WebSocket
        self.controller_connections: Dict[str, WebSocket] = {}
        # Active web client WebSocket connections: client_id -> WebSocket
        self.web_client_connections: Dict[str, WebSocket] = {}
        # Candlestick states: candlestick_id -> CandlestickState
        self.states: Dict[str, CandlestickState] = {}
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()
        # Counter for web client IDs
        self._client_id_counter = 0
    
    async def connect_controller(self, websocket: WebSocket, candlestick_id: str):
        """Accept a new controller WebSocket connection and initialize state"""
        await websocket.accept()
        
        async with self._lock:
            self.controller_connections[candlestick_id] = websocket
            
            # Initialize or update state
            if candlestick_id in self.states:
                # Reconnection - update existing state
                self.states[candlestick_id].connected = True
                self.states[candlestick_id].last_seen = datetime.now()
            else:
                # New connection - create new state
                self.states[candlestick_id] = CandlestickState(
                    id=candlestick_id,
                    connected=True,
                    last_seen=datetime.now()
                )
        
        logger.info(f"Controller '{candlestick_id}' connected. Total controllers: {len(self.controller_connections)}")
    
    def disconnect_controller(self, candlestick_id: str):
        """Remove a controller WebSocket connection and mark as disconnected"""
        if candlestick_id in self.controller_connections:
            del self.controller_connections[candlestick_id]
        
        if candlestick_id in self.states:
            self.states[candlestick_id].connected = False
            self.states[candlestick_id].last_seen = datetime.now()
        
        logger.info(f"Controller '{candlestick_id}' disconnected. Remaining controllers: {len(self.controller_connections)}")
    
    async def connect_web_client(self, websocket: WebSocket) -> str:
        """Accept a new web client WebSocket connection"""
        await websocket.accept()
        
        async with self._lock:
            self._client_id_counter += 1
            client_id = f"web_client_{self._client_id_counter}"
            self.web_client_connections[client_id] = websocket
        
        logger.info(f"Web client '{client_id}' connected. Total web clients: {len(self.web_client_connections)}")
        return client_id
    
    def disconnect_web_client(self, client_id: str):
        """Remove a web client WebSocket connection"""
        if client_id in self.web_client_connections:
            del self.web_client_connections[client_id]
        
        logger.info(f"Web client '{client_id}' disconnected. Remaining web clients: {len(self.web_client_connections)}")
    
    async def disconnect_all(self):
        """Disconnect all active connections (both controllers and web clients)"""
        # Disconnect controllers
        for candlestick_id in list(self.controller_connections.keys()):
            try:
                websocket = self.controller_connections[candlestick_id]
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing controller connection for {candlestick_id}: {e}")
            finally:
                self.disconnect_controller(candlestick_id)
        
        # Disconnect web clients
        for client_id in list(self.web_client_connections.keys()):
            try:
                websocket = self.web_client_connections[client_id]
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing web client connection for {client_id}: {e}")
            finally:
                self.disconnect_web_client(client_id)
    
    def is_connected(self, candlestick_id: str) -> bool:
        """Check if a candlestick controller is currently connected"""
        return candlestick_id in self.controller_connections
    
    def get_state(self, candlestick_id: str) -> Optional[CandlestickState]:
        """Get the current state of a candlestick"""
        return self.states.get(candlestick_id)
    
    def get_all_states(self) -> Dict[str, CandlestickState]:
        """Get states of all candlesticks"""
        return self.states
    
    def update_state(
        self,
        candlestick_id: str,
        program: Optional[str] = None,
        random: Optional[bool] = None,
        speed: Optional[int] = None,
        direction: Optional[str] = None,
        color: Optional[str] = None
    ):
        """Update the state of a candlestick"""
        if candlestick_id not in self.states:
            logger.warning(f"Attempted to update state for unknown candlestick: {candlestick_id}")
            return
        
        state = self.states[candlestick_id]
        
        # Always update these fields (they can be None to clear the value)
        state.program = program if program is not None else state.program
        state.direction = direction  # Always update, can be None
        state.color = color  # Always update, can be None
        
        # Only update these if a value is provided
        if random is not None:
            state.random = random
        if speed is not None:
            state.speed = speed
        
        state.last_seen = datetime.now()
    
    def update_heartbeat(self, candlestick_id: str):
        """Update the last_seen timestamp for a candlestick"""
        if candlestick_id in self.states:
            self.states[candlestick_id].last_seen = datetime.now()
    
    async def send_command(self, candlestick_id: str, command: CandlestickCommand):
        """Send a command to a specific candlestick controller"""
        if candlestick_id not in self.controller_connections:
            raise ValueError(f"Candlestick '{candlestick_id}' is not connected")
        
        websocket = self.controller_connections[candlestick_id]
        
        # Prepare command message
        message = {
            "type": MessageType.COMMAND,
            **command.model_dump(exclude_none=True)
        }
        
        try:
            await websocket.send_text(json.dumps(message))
            logger.debug(f"Sent command to {candlestick_id}: {message}")
            
            # Update local state to reflect the command
            self.update_state(
                candlestick_id,
                program=command.program,
                speed=command.speed,
                direction=command.direction,
                color=command.color
            )
        except Exception as e:
            logger.error(f"Failed to send command to {candlestick_id}: {e}")
            raise
    
    async def broadcast_to_web_clients(self, message: dict):
        """Broadcast a message to all connected web clients"""
        if not self.web_client_connections:
            return
        
        message_text = json.dumps(message)
        disconnected_clients = []
        
        for client_id, websocket in self.web_client_connections.items():
            try:
                await websocket.send_text(message_text)
                logger.debug(f"Sent message to web client {client_id}")
            except Exception as e:
                logger.error(f"Failed to send message to web client {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect_web_client(client_id)
    
    async def cleanup_stale_connections(self, timeout_minutes: int = 5):
        """
        Background task to clean up stale connection states.
        Runs periodically to remove disconnected candlesticks that haven't been seen recently.
        """
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                now = datetime.now()
                stale_ids = []
                
                for candlestick_id, state in self.states.items():
                    if not state.connected:
                        time_since_seen = now - state.last_seen
                        if time_since_seen > timedelta(minutes=timeout_minutes):
                            stale_ids.append(candlestick_id)
                
                for candlestick_id in stale_ids:
                    logger.info(f"Removing stale state for {candlestick_id}")
                    del self.states[candlestick_id]
                    
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
