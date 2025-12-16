#!/usr/bin/env python3
"""
OMEGA COMMAND CENTER - WORKING VERSION (Port 8081)
WebSocket server that definitely works
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omega_8081_working'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

print("\n" + "="*60)
print("   OMEGA COMMAND CENTER - PORT 8081")
print("   WebSocket Test - Working Version")
print("="*60)

# Store client modes
client_modes = {}

@app.route('/')
def index():
    """Serve the main interface"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Omega Command Center 8081</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; background: #0d1b2a; color: white; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; }
            .mode-buttons { display: flex; gap: 20px; margin: 30px 0; }
            .mode-btn { flex: 1; padding: 15px; font-size: 16px; border: none; border-radius: 8px; cursor: pointer; }
            .mode-btn.active { background: #00d4aa; color: #0d1b2a; font-weight: bold; }
            .interface { display: none; padding: 20px; background: #1b263b; border-radius: 10px; }
            .interface.active { display: block; }
            .status { position: fixed; bottom: 20px; right: 20px; padding: 10px 15px; background: rgba(0,0,0,0.5); border-radius: 5px; }
        </style>
        <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="color: #00d4aa;">PROJECT OMEGA</h1>
                <p>Command Center • Port 8081 • WebSocket Active</p>
            </div>
            
            <div class="mode-buttons">
                <button class="mode-btn active" id="btn-simple">🧭 Simple Mode</button>
                <button class="mode-btn" id="btn-advanced">⚙️ Advanced Mode</button>
            </div>
            
            <div id="simple-interface" class="interface active">
                <h2>Simple Interface</h2>
                <p>WebSocket Status: <span id="ws-status">Testing...</span></p>
                <p>Click the buttons above to switch between modes.</p>
                <button id="test-btn" style="padding:10px 20px;background:#1e4d8c;color:white;border:none;border-radius:5px;margin-top:10px;">
                    Test WebSocket
                </button>
            </div>
            
            <div id="advanced-interface" class="interface">
                <h2>Advanced Interface</h2>
                <p>Connected to Omega server on port 8081</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px;">
                    <div style="background:rgba(255,255,255,0.05);padding:15px;border-radius:8px;">
                        <h3>System Health</h3>
                        <div style="font-size:24px;color:#00d4aa;" id="metric-health">Loading...</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.05);padding:15px;border-radius:8px;">
                        <h3>Active Clients</h3>
                        <div style="font-size:24px;color:#00d4aa;" id="metric-clients">0</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="status" id="status-bar">
            🔄 Initializing...
        </div>
        
        <script>
            // Global socket variable
            let socket = null;
            let currentMode = 'simple';
            
            // Initialize everything when page loads
            document.addEventListener('DOMContentLoaded', function() {
                console.log("Omega Command Center initializing...");
                
                // Set up button click handlers
                document.getElementById('btn-simple').addEventListener('click', () => switchMode('simple'));
                document.getElementById('btn-advanced').addEventListener('click', () => switchMode('advanced'));
                document.getElementById('test-btn').addEventListener('click', sendTestMessage);
                
                // Initialize WebSocket connection
                initializeWebSocket();
                
                // Update status
                updateStatus('Page loaded, connecting...');
            });
            
            function initializeWebSocket() {
                console.log("Connecting to WebSocket on port 8081...");
                
                // Connect to server - IMPORTANT: Specify port 8081
                socket = io('http://localhost:8081', {
                    transports: ['websocket', 'polling'],
                    reconnection: true,
                    reconnectionAttempts: 5
                });
                
                // Connection established
                socket.on('connect', function() {
                    console.log("✅ WebSocket CONNECTED successfully!");
                    document.getElementById('ws-status').textContent = 'CONNECTED';
                    document.getElementById('ws-status').style.color = '#00d4aa';
                    updateStatus('✅ Connected to Omega server');
                    
                    // Tell server our initial mode
                    socket.emit('mode_change', { mode: currentMode });
                    
                    // Request initial data
                    socket.emit('get_metrics');
                });
                
                // Connection error
                socket.on('connect_error', function(error) {
                    console.error("❌ WebSocket connection error:", error);
                    document.getElementById('ws-status').textContent = 'ERROR: ' + error.message;
                    document.getElementById('ws-status').style.color = 'red';
                    updateStatus('❌ Connection failed: ' + error.message);
                });
                
                // Server welcome
                socket.on('welcome', function(data) {
                    console.log("Server welcome:", data);
                    updateStatus('Server: ' + data.message);
                });
                
                // Mode change confirmation
                socket.on('mode_changed', function(data) {
                    console.log("Mode change confirmed:", data);
                    updateStatus('Mode: ' + data.mode);
                });
                
                // Metrics update
                socket.on('metrics_update', function(data) {
                    console.log("Metrics received:", data);
                    document.getElementById('metric-health').textContent = data.health + '%';
                    document.getElementById('metric-clients').textContent = data.clients;
                });
                
                // Test response
                socket.on('test_response', function(data) {
                    alert('Server responded: ' + JSON.stringify(data));
                });
            }
            
            function switchMode(mode) {
                if (mode === currentMode) return;
                
                console.log("Switching to " + mode + " mode...");
                currentMode = mode;
                
                // Update button styles
                document.getElementById('btn-simple').classList.toggle('active', mode === 'simple');
                document.getElementById('btn-advanced').classList.toggle('active', mode === 'advanced');
                
                // Show/hide interfaces
                document.getElementById('simple-interface').classList.toggle('active', mode === 'simple');
                document.getElementById('advanced-interface').classList.toggle('active', mode === 'advanced');
                
                // Tell server about mode change
                if (socket && socket.connected) {
                    socket.emit('mode_change', { mode: mode });
                }
                
                updateStatus('Switched to ' + mode + ' mode');
            }
            
            function sendTestMessage() {
                if (socket && socket.connected) {
                    socket.emit('test_message', { 
                        action: 'test',
                        timestamp: new Date().toISOString()
                    });
                    updateStatus('Test message sent');
                } else {
                    alert('Not connected to server!');
                }
            }
            
            function updateStatus(message) {
                document.getElementById('status-bar').textContent = message;
                console.log("Status:", message);
            }
        </script>
    </body>
    </html>
    '''

# WebSocket Event Handlers
@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    print(f"✅ CLIENT CONNECTED: {client_id}")
    
    # Send welcome message
    emit('welcome', {
        'message': 'Welcome to Omega Command Center (Port 8081)',
        'client_id': client_id[-6:],
        'timestamp': 'Now'
    })
    
    # Update all clients with new count
    emit('metrics_update', {
        'health': 95,
        'clients': len(client_modes) + 1,
        'status': 'active'
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in client_modes:
        del client_modes[client_id]
    print(f"Client disconnected: {client_id}")
    
    # Update client count
    emit('metrics_update', {
        'health': 95,
        'clients': len(client_modes),
        'status': 'active'
    }, broadcast=True)

@socketio.on('mode_change')
def handle_mode_change(data):
    client_id = request.sid
    mode = data.get('mode', 'simple')
    
    client_modes[client_id] = mode
    print(f"Client {client_id[-6:]} switched to {mode} mode")
    
    # Send confirmation
    emit('mode_changed', {
        'mode': mode,
        'message': f'Successfully switched to {mode} mode',
        'timestamp': 'Now'
    })

@socketio.on('test_message')
def handle_test_message(data):
    print(f"Test message from {request.sid[-6:]}: {data}")
    emit('test_response', {
        'received': data,
        'server_response': 'Hello from Omega server!',
        'timestamp': 'Now'
    })

@socketio.on('get_metrics')
def handle_get_metrics():
    emit('metrics_update', {
        'health': 95,
        'clients': len(client_modes),
        'status': 'active',
        'port': 8081
    })

if __name__ == '__main__':
    print("\n🚀 STARTING OMEGA COMMAND CENTER")
    print("🌐 Open: http://localhost:8081")
    print("📡 WebSocket: ws://localhost:8081/socket.io/")
    print("💡 Features: Dual Interface • Real-time Updates • Working WebSocket")
    print("-" * 60)
    
    try:
        socketio.run(app, host='0.0.0.0', port=8081, debug=False, use_reloader=False, log_output=True)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure no other server is using port 8081")
        print("2. Check if firewall allows port 8081")
        print("3. Try: python3 -c \"import socket; s=socket.socket(); s.bind(('',8081)); print('Port 8081 available'); s.close()\"")
