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
        # Active WebSocket connections: candlestick_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # Candlestick states: candlestick_id -> CandlestickState
        self.states: Dict[str, CandlestickState] = {}
        # Lock for thread-safe operations
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket, candlestick_id: str):
        """Accept a new WebSocket connection and initialize state"""
        await websocket.accept()
        
        async with self._lock:
            self.active_connections[candlestick_id] = websocket
            
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
        
        logger.info(f"Candlestick '{candlestick_id}' connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, candlestick_id: str):
        """Remove a WebSocket connection and mark as disconnected"""
        if candlestick_id in self.active_connections:
            del self.active_connections[candlestick_id]
        
        if candlestick_id in self.states:
            self.states[candlestick_id].connected = False
            self.states[candlestick_id].last_seen = datetime.now()
        
        logger.info(f"Candlestick '{candlestick_id}' disconnected. Remaining connections: {len(self.active_connections)}")
    
    async def disconnect_all(self):
        """Disconnect all active connections"""
        for candlestick_id in list(self.active_connections.keys()):
            try:
                websocket = self.active_connections[candlestick_id]
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing connection for {candlestick_id}: {e}")
            finally:
                self.disconnect(candlestick_id)
    
    def is_connected(self, candlestick_id: str) -> bool:
        """Check if a candlestick is currently connected"""
        return candlestick_id in self.active_connections
    
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
        speed: Optional[int] = None,
        direction: Optional[str] = None,
        color: Optional[str] = None
    ):
        """Update the state of a candlestick"""
        if candlestick_id not in self.states:
            logger.warning(f"Attempted to update state for unknown candlestick: {candlestick_id}")
            return
        
        state = self.states[candlestick_id]
        
        if program is not None:
            state.program = program
        if speed is not None:
            state.speed = speed
        if direction is not None:
            state.direction = direction
        if color is not None:
            state.color = color
        
        state.last_seen = datetime.now()
    
    def update_heartbeat(self, candlestick_id: str):
        """Update the last_seen timestamp for a candlestick"""
        if candlestick_id in self.states:
            self.states[candlestick_id].last_seen = datetime.now()
    
    async def send_command(self, candlestick_id: str, command: CandlestickCommand):
        """Send a command to a specific candlestick"""
        if candlestick_id not in self.active_connections:
            raise ValueError(f"Candlestick '{candlestick_id}' is not connected")
        
        websocket = self.active_connections[candlestick_id]
        
        # Prepare command message
        message = {
            "type": MessageType.COMMAND,
            **command.dict(exclude_none=True)
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
