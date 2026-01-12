"""
Distributed Messaging System for Project Omega
Enables communication between nodes across platforms
"""
import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List, Any
import logging

logger = logging.getLogger("OmegaMessaging")

class MessageBus:
    """Distributed message bus for Omega nodes"""
    
    def __init__(self, host: str = "localhost", port: int = 1883):
        self.host = host
        self.port = port
        self.subscriptions: Dict[str, List] = {}
        self.connected = False
        logger.info(f"MessageBus initialized: {host}:{port}")
    
    async def connect(self):
        """Connect to message bus"""
        # TODO: Implement actual MQTT/WebSocket connection
        self.connected = True
        logger.info("✅ Connected to message bus")
        return True
    
    async def publish(self, topic: str, message: Dict[str, Any]):
        """Publish message to topic"""
        if not self.connected:
            await self.connect()
        
        payload = {
            "topic": topic,
            "message": message,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Notify subscribers
        if topic in self.subscriptions:
            for callback in self.subscriptions[topic]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(payload)
                else:
                    callback(payload)
        
        logger.info(f"📤 Published to {topic}: {message.get('type', 'data')}")
        return payload
    
    def subscribe(self, topic: str, callback):
        """Subscribe to topic"""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(callback)
        logger.info(f"📥 Subscribed to {topic}")
    
    async def broadcast_system_status(self, status: Dict):
        """Broadcast system status to all nodes"""
        return await self.publish("omega/system/status", status)

class CrossPlatformCommunicator:
    """Handle communication across different platforms"""
    
    PLATFORM_PROFILES = {
        "android": {"protocol": "websocket", "compression": True},
        "linux": {"protocol": "mqtt", "compression": False},
        "windows": {"protocol": "websocket", "compression": True},
        "raspberry": {"protocol": "mqtt", "compression": True}
    }
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.platform_adapters = {}
        logger.info("CrossPlatformCommunicator initialized")
    
    async def send_command(self, target_node: str, command: Dict) -> bool:
        """Send command to specific node"""
        message = {
            "command": command,
            "target": target_node,
            "requires_ack": True
        }
        
        result = await self.message_bus.publish(
            f"omega/command/{target_node}",
            message
        )
        
        logger.info(f"📨 Command sent to {target_node}: {command.get('action')}")
        return True

# Quick test
async def test_messaging():
    print("🧪 Testing Distributed Messaging...")
    
    bus = MessageBus()
    await bus.connect()
    
    # Test publish/subscribe
    async def handle_message(msg):
        print(f"📩 Received: {msg['topic']} - {msg['message']}")
    
    bus.subscribe("omega/test", handle_message)
    
    await bus.publish("omega/test", {
        "type": "test_message",
        "content": "Omega messaging operational"
    })
    
    await asyncio.sleep(0.1)  # Give time for async processing
    print("✅ Distributed messaging test complete")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    asyncio.run(test_messaging())
