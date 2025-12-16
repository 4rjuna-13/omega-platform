"""
Web-based voice input alternative
Uses browser speech recognition via websocket
"""

import asyncio
import websockets
import json

class WebVoiceInput:
    """Voice input via web browser"""
    
    def __init__(self):
        self.connected = False
        
    async def start_server(self):
        """Start WebSocket server for browser voice input"""
        async def handler(websocket):
            self.connected = True
            print("[WEB VOICE] Browser connected. Speak into browser microphone.")
            
            async for message in websocket:
                data = json.loads(message)
                if data['type'] == 'voice':
                    print(f"[WEB VOICE] Received: {data['text']}")
                    return data['text']
        
        server = await websockets.serve(handler, "localhost", 8765)
        print("[WEB VOICE] Server started at ws://localhost:8765")
        print("[WEB VOICE] Open web_voice.html in browser")
        await server.wait_closed()
    
    def listen(self):
        """Listen for voice input via web"""
        print("[WEB VOICE] Starting web voice server...")
        asyncio.run(self.start_server())

if __name__ == "__main__":
    wvi = WebVoiceInput()
    wvi.listen()
