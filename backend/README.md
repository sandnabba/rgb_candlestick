# Backend Server

This is the central backend server that manages WebSocket connections from multiple candlestick controllers and provides a REST API for the web frontend.

## Architecture

The backend uses a reversed architecture where:
- **Controllers** connect to the backend via WebSocket (push model)
- **Web frontend** queries the backend via REST API
- The backend acts as a central hub managing multiple candlestick devices

## Requirements

The backend is designed to run in Docker and includes:
* Python 3.10+
* FastAPI
* uvicorn
* websockets
* pydantic

## Building and Running with Docker

The recommended way to run the backend is using Docker. The Dockerfile is a multi-stage build that:
1. Builds the web frontend (React/TypeScript/Vite)
2. Creates the Python backend image with the compiled frontend

### Build the Docker image

```sh
docker build -t rgb-candlestick-backend .
```

### Run the container

```sh
docker run -d -p 8000:8000 --name rgb-backend rgb-candlestick-backend
```

The server will be available at `http://localhost:8000`

### Development with Docker

To rebuild after changes:
```sh
docker build -t rgb-candlestick-backend . && docker rm -f rgb-backend && docker run -d -p 8000:8000 --name rgb-backend rgb-candlestick-backend
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
