#!/usr/bin/env python3
"""
Basic WebSocket Test Server
"""

from flask import Flask
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

print("\n" + "="*60)
print("   BASIC WEBSOCKET TEST SERVER")
print("="*60)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>WebSocket Test</title></head>
    <body style="background:#0d1b2a;color:white;padding:20px;">
        <h1>🔌 WebSocket Connection Test</h1>
        <p>Click the button to test WebSocket connection:</p>
        <button onclick="testWS()" style="padding:10px 20px;background:#00d4aa;color:#0d1b2a;border:none;border-radius:5px;cursor:pointer;">
            Test WebSocket
        </button>
        <p id="result" style="margin-top:20px;"></p>
        
        <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
        <script>
            function testWS() {
                const result = document.getElementById('result');
                result.innerHTML = "Connecting...";
                result.style.color = "yellow";
                
                console.log("Starting WebSocket test...");
                
                // Try to connect
                const socket = io({
                    transports: ['websocket', 'polling'],
                    reconnection: false,
                    timeout: 5000
                });
                
                socket.on('connect', () => {
                    console.log("✅ CONNECTED!");
                    result.innerHTML = "✅ WebSocket CONNECTED successfully!";
                    result.style.color = "#00d4aa";
                    socket.emit('hello', {message: 'Test from client'});
                });
                
                socket.on('connect_error', (error) => {
                    console.error("❌ Connection error:", error);
                    result.innerHTML = "❌ Connection failed: " + error.message;
                    result.style.color = "red";
                });
                
                socket.on('hello_response', (data) => {
                    console.log("Server response:", data);
                    result.innerHTML += "<br>📨 Server replied: " + JSON.stringify(data);
                });
                
                // Timeout after 3 seconds
                setTimeout(() => {
                    if (!socket.connected) {
                        result.innerHTML = "⏰ Connection timeout - server may not be running";
                        result.style.color = "orange";
                    }
                }, 3000);
            }
            
            // Auto-test on page load
            window.addEventListener('load', () => {
                setTimeout(testWS, 1000);
            });
        </script>
    </body>
    </html>
    '''

@socketio.on('connect')
def handle_connect():
    print(f"✅ Client connected: {request.sid}")
    return {'status': 'connected'}

@socketio.on('hello')
def handle_hello(data):
    print(f"📨 Received: {data}")
    return {'response': 'Hello from Omega server!', 'your_data': data}

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    print("\n🚀 Starting test server on PORT 8080")
    print("🌐 Open: http://localhost:8080")
    print("💡 Browser will auto-test WebSocket connection")
    print("-" * 60)
    
    try:
        socketio.run(app, host='0.0.0.0', port=8080, debug=False, use_reloader=False, log_output=True)
    except Exception as e:
        print(f"\n❌ ERROR starting server: {e}")
        print("\nPossible issues:")
        print("1. Port 8080 is already in use")
        print("2. Firewall blocking the port")
        print("3. Permission issue")
        print("\nTry: sudo netstat -tulpn | grep :8080")
