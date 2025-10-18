"""
FastAPI Backend for RGB Candlestick Controller
Manages WebSocket connections from controllers and provides REST API for web frontend.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import logging
import json
import asyncio

from models import (
    CandlestickState,
    CandlestickCommand,
    CandlestickListResponse,
    MessageType
)
from connection_manager import ConnectionManager

# Setup logging
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RGB Candlestick Backend",
    description="Central backend managing candlestick controllers via WebSocket",
    version="1.0.0",
    redoc_url=None  # Disable ReDoc, use Swagger only
)

# CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection manager for WebSocket connections
manager = ConnectionManager()


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "RGB Candlestick Backend",
        "connected_candlesticks": len(manager.get_all_states())
    }


@app.get("/api/candlesticks", response_model=CandlestickListResponse)
async def list_candlesticks():
    """
    List all candlesticks and their current state.
    Returns both connected and recently disconnected candlesticks.
    """
    states = manager.get_all_states()
    return CandlestickListResponse(candlesticks=list(states.values()))


@app.get("/api/candlesticks/{candlestick_id}", response_model=CandlestickState)
async def get_candlestick(candlestick_id: str):
    """
    Get the current state of a specific candlestick.
    """
    state = manager.get_state(candlestick_id)
    if not state:
        raise HTTPException(status_code=404, detail="Candlestick not found")
    return state


@app.post("/api/candlesticks/{candlestick_id}/command")
async def send_command(candlestick_id: str, command: CandlestickCommand):
    """
    Send a command to a specific candlestick.
    The candlestick must be connected via WebSocket.
    """
    if not manager.is_connected(candlestick_id):
        raise HTTPException(
            status_code=404,
            detail=f"Candlestick '{candlestick_id}' is not connected"
        )
    
    try:
        await manager.send_command(candlestick_id, command)
        logger.info(f"Command sent to {candlestick_id}: {command.dict(exclude_none=True)}")
        return {"status": "success", "message": "Command sent to candlestick"}
    except Exception as e:
        logger.error(f"Failed to send command to {candlestick_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{candlestick_id}")
async def websocket_endpoint(websocket: WebSocket, candlestick_id: str):
    """
    WebSocket endpoint for candlestick controllers to connect.
    Each controller maintains a persistent connection and receives commands from the backend.
    """
    await manager.connect(websocket, candlestick_id)
    logger.info(f"Candlestick '{candlestick_id}' connected")
    
    try:
        while True:
            # Receive messages from the controller
            data = await websocket.receive_text()
            message = json.loads(data)
            
            logger.debug(f"Received from {candlestick_id}: {message}")
            
            # Handle different message types
            msg_type = message.get("type")
            
            if msg_type == MessageType.STATUS:
                # Update the state with status information
                manager.update_state(
                    candlestick_id,
                    program=message.get("program"),
                    speed=message.get("speed"),
                    direction=message.get("direction"),
                    color=message.get("color")
                )
                logger.debug(f"Updated state for {candlestick_id}")
                
            elif msg_type == MessageType.HEARTBEAT:
                # Just update last_seen timestamp
                manager.update_heartbeat(candlestick_id)
                
            else:
                logger.warning(f"Unknown message type from {candlestick_id}: {msg_type}")
                
    except WebSocketDisconnect:
        logger.info(f"Candlestick '{candlestick_id}' disconnected")
        manager.disconnect(candlestick_id)
    except Exception as e:
        logger.error(f"Error in WebSocket connection for {candlestick_id}: {e}")
        manager.disconnect(candlestick_id)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Backend server starting up")
    # Start background task for cleaning up stale connections
    asyncio.create_task(manager.cleanup_stale_connections())


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Backend server shutting down")
    await manager.disconnect_all()


# Serve static files (frontend application) - MUST be last!
# This catches all remaining routes and serves static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")
