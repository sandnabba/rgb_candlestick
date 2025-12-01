"""
Pydantic models for the RGB Candlestick Backend API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageType(str, Enum):
    """WebSocket message types"""
    STATUS = "status"
    HEARTBEAT = "heartbeat"
    COMMAND = "command"


class CandlestickCommand(BaseModel):
    """Command to send to a candlestick"""
    program: Optional[str] = Field(None, description="Program/pattern to run (e.g., 'rb', 'wave', 'random')")
    speed: Optional[int] = Field(None, ge=1, le=100, description="Speed of the program (1-100)")
    direction: Optional[str] = Field(None, description="Direction: 'left', 'right', 'up', 'down'")
    color: Optional[str] = Field(None, description="HTML color code (e.g., '#ff0000')")

    model_config = {
        "json_schema_extra": {
            "example": {
                "program": "rb",
                "speed": 15,
                "direction": "right",
                "color": None
            }
        }
    }


class CandlestickState(BaseModel):
    """Current state of a candlestick"""
    id: str = Field(..., description="Unique identifier for the candlestick")
    connected: bool = Field(..., description="Whether the candlestick is currently connected")
    program: Optional[str] = Field(None, description="Currently running program")
    random: Optional[bool] = Field(None, description="Whether random mode is active")
    speed: Optional[int] = Field(None, description="Current speed setting")
    direction: Optional[str] = Field(None, description="Current direction")
    color: Optional[str] = Field(None, description="Current color (if in static color mode)")
    last_seen: datetime = Field(..., description="Last time the candlestick was seen")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "candlestick_001",
                "connected": True,
                "program": "rainbow",
                "speed": 10,
                "direction": "right",
                "color": None,
                "last_seen": "2025-10-16T10:30:00"
            }
        }
    }


class CandlestickListResponse(BaseModel):
    """Response containing list of all candlesticks"""
    candlesticks: List[CandlestickState]


class WebSocketMessage(BaseModel):
    """Base WebSocket message structure"""
    type: MessageType
    
    model_config = {
        "use_enum_values": True
    }


class StatusMessage(WebSocketMessage):
    """Status update from controller"""
    type: MessageType = MessageType.STATUS
    program: Optional[str] = None
    random: Optional[bool] = None
    speed: Optional[int] = None
    direction: Optional[str] = None
    color: Optional[str] = None


class HeartbeatMessage(WebSocketMessage):
    """Heartbeat from controller"""
    type: MessageType = MessageType.HEARTBEAT


class CommandMessage(WebSocketMessage):
    """Command to controller"""
    type: MessageType = MessageType.COMMAND
    program: Optional[str] = None
    speed: Optional[int] = None
    direction: Optional[str] = None
    color: Optional[str] = None
