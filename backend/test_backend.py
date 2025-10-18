#!/usr/bin/env python3
"""
Test script for the backend API and WebSocket connection.
Tests basic functionality without requiring actual hardware.
"""

import asyncio
import websockets
import json
import requests
import time
from typing import Dict, Any


class MockController:
    """Mock controller for testing WebSocket connection"""
    
    def __init__(self, backend_url: str, candlestick_id: str):
        self.backend_url = backend_url
        self.candlestick_id = candlestick_id
        self.ws_url = f"{backend_url}/ws/{candlestick_id}"
        self.websocket = None
        self.current_state = {
            "program": "random",
            "speed": 10,
            "direction": "right",
            "color": None
        }
    
    async def connect_and_listen(self, duration: int = 10):
        """Connect to backend and listen for commands"""
        print(f"Connecting to {self.ws_url}...")
        
        async with websockets.connect(self.ws_url) as websocket:
            self.websocket = websocket
            print(f"✓ Connected as {self.candlestick_id}")
            
            # Send initial status
            await self.send_status()
            
            # Listen for commands for the specified duration
            start_time = time.time()
            try:
                while time.time() - start_time < duration:
                    try:
                        message = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=2.0
                        )
                        data = json.loads(message)
                        print(f"Received command: {data}")
                        
                        if data.get("type") == "command":
                            # Update state based on command
                            if "program" in data:
                                self.current_state["program"] = data["program"]
                            if "speed" in data:
                                self.current_state["speed"] = data["speed"]
                            if "direction" in data:
                                self.current_state["direction"] = data["direction"]
                            if "color" in data:
                                self.current_state["color"] = data["color"]
                            
                            # Send updated status
                            await self.send_status()
                            print(f"Updated state: {self.current_state}")
                            
                    except asyncio.TimeoutError:
                        # Send heartbeat
                        await self.send_heartbeat()
                        
            except KeyboardInterrupt:
                print("\nInterrupted by user")
    
    async def send_status(self):
        """Send status update to backend"""
        message = {
            "type": "status",
            **self.current_state
        }
        await self.websocket.send(json.dumps(message))
        print(f"Sent status: {self.current_state}")
    
    async def send_heartbeat(self):
        """Send heartbeat"""
        message = {"type": "heartbeat"}
        await self.websocket.send(json.dumps(message))
        print("Sent heartbeat")


def test_rest_api(base_url: str, candlestick_id: str):
    """Test REST API endpoints"""
    print("\n" + "="*60)
    print("Testing REST API")
    print("="*60)
    
    # Test health check
    print("\n1. Testing health check...")
    response = requests.get(f"{base_url}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test list candlesticks
    print("\n2. Testing list candlesticks...")
    response = requests.get(f"{base_url}/api/candlesticks")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Found {len(data['candlesticks'])} candlestick(s)")
    for cs in data['candlesticks']:
        print(f"   - {cs['id']}: connected={cs['connected']}, program={cs['program']}")
    
    # Test get specific candlestick
    print(f"\n3. Testing get candlestick '{candlestick_id}'...")
    response = requests.get(f"{base_url}/api/candlesticks/{candlestick_id}")
    if response.status_code == 200:
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    else:
        print(f"   Status: {response.status_code} (candlestick not found - expected if not connected)")
    
    # Test send command
    print(f"\n4. Testing send command to '{candlestick_id}'...")
    command = {
        "program": "rb",
        "speed": 15,
        "direction": "left"
    }
    response = requests.post(
        f"{base_url}/api/candlesticks/{candlestick_id}/command",
        json=command
    )
    if response.status_code == 200:
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    else:
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   (Candlestick not connected - expected if WebSocket client not running)")


async def test_websocket(ws_url: str, candlestick_id: str, duration: int = 10):
    """Test WebSocket connection"""
    print("\n" + "="*60)
    print("Testing WebSocket Connection")
    print("="*60)
    
    controller = MockController(ws_url, candlestick_id)
    await controller.connect_and_listen(duration)


async def main():
    """Main test function"""
    # Configuration
    http_url = "http://localhost:8000"
    ws_url = "ws://localhost:8000"
    candlestick_id = "test_candlestick"
    
    print("="*60)
    print("RGB Candlestick Backend Test")
    print("="*60)
    print(f"Backend URL: {http_url}")
    print(f"WebSocket URL: {ws_url}")
    print(f"Test Candlestick ID: {candlestick_id}")
    
    # First test REST API without connection
    print("\n[Phase 1: Testing REST API without connected devices]")
    try:
        test_rest_api(http_url, candlestick_id)
    except Exception as e:
        print(f"❌ REST API test failed: {e}")
        print("Make sure the backend is running: python3 backend/main.py")
        return
    
    # Test WebSocket connection
    print("\n\n[Phase 2: Testing WebSocket connection]")
    print("Mock controller will connect and listen for 10 seconds...")
    print("While it's running, you can test sending commands via API:")
    print(f"\n  curl -X POST {http_url}/api/candlesticks/{candlestick_id}/command \\")
    print(f"       -H 'Content-Type: application/json' \\")
    print(f"       -d '{{\"program\": \"wave\", \"speed\": 20}}'")
    print()
    
    try:
        await test_websocket(ws_url, candlestick_id, duration=10)
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return
    
    # Test REST API after connection
    print("\n\n[Phase 3: Testing REST API after disconnection]")
    try:
        test_rest_api(http_url, candlestick_id)
    except Exception as e:
        print(f"❌ REST API test failed: {e}")
    
    print("\n" + "="*60)
    print("✓ Tests completed!")
    print("="*60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
