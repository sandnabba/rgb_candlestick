# Backend Server

This is the central backend server that manages WebSocket connections from multiple candlestick controllers and provides a REST API for the web frontend.

## Architecture

The backend uses a reversed architecture where:
- **Controllers** connect to the backend via WebSocket (push model)
- **Web frontend** queries the backend via REST API
- The backend acts as a central hub managing multiple candlestick devices

## Requirements

* Python 3.8+
* FastAPI
* uvicorn
* websockets
* pydantic

## Installation

### Python virtual environment

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Running

Start the backend server:
```sh
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or using the provided script:
```sh
python3 main.py
```

## API Documentation

Once the server is running, interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs

## API Endpoints

### GET /api/candlesticks
List all connected candlesticks and their current state.

**Response:**
```json
{
  "candlesticks": [
    {
      "id": "candlestick_001",
      "connected": true,
      "program": "rainbow",
      "speed": 10,
      "direction": "right",
      "color": null,
      "last_seen": "2025-10-16T10:30:00"
    }
  ]
}
```

### GET /api/candlesticks/{candlestick_id}
Get the status of a specific candlestick.

### POST /api/candlesticks/{candlestick_id}/command
Send a command to a specific candlestick.

**Request Body:**
```json
{
  "program": "rb",
  "speed": 15,
  "direction": "left",
  "color": "#ff0000"
}
```

## WebSocket Protocol

Controllers connect to: `ws://localhost:8000/ws/{candlestick_id}`

### Message Types

#### From Controller to Backend

**Status Update:**
```json
{
  "type": "status",
  "program": "rainbow",
  "speed": 10,
  "direction": "right",
  "color": null
}
```

**Heartbeat:**
```json
{
  "type": "heartbeat"
}
```

#### From Backend to Controller

**Command:**
```json
{
  "type": "command",
  "program": "rb",
  "speed": 15,
  "direction": "left",
  "color": "#ff0000"
}
```

## Future Enhancements

- Authentication for WebSocket connections
- Persistent storage of candlestick configurations
- Groups/rooms for managing multiple candlesticks
- Event logging and history
- Scheduled programs
