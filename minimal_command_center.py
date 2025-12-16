#!/usr/bin/env python3
"""
MINIMAL OMEGA COMMAND CENTER
Working WebSocket server for dual interface
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omega_minimal_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

print("\n" + "="*60)
print("   MINIMAL OMEGA COMMAND CENTER")
print("   Working WebSocket • Dual Interface")
print("="*60)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Omega Minimal</title>
        <style>
            body { font-family: Arial; background: #0d1b2a; color: white; padding: 20px; }
            .mode-buttons { display: flex; gap: 20px; margin: 20px 0; }
            .mode-btn { padding: 15px 30px; font-size: 18px; border: none; border-radius: 10px; cursor: pointer; }
            .mode-btn.active { background: #00d4aa; color: #0d1b2a; }
            .interface { display: none; padding: 20px; background: #1b263b; border-radius: 10px; margin-top: 20px; }
            .interface.active { display: block; }
        </style>
        <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
    </head>
    <body>
        <h1>Omega Minimal Command Center</h1>
        <p>Testing WebSocket connectivity</p>
        
        <div class="mode-buttons">
            <button class="mode-btn active" onclick="switchToSimple()">Simple</button>
            <button class="mode-btn" onclick="switchToAdvanced()">Advanced</button>
        </div>
        
        <div id="simple" class="interface active">
            <h2>Simple Interface</h2>
            <p>WebSocket Status: <span id="ws-status">Disconnected</span></p>
            <button onclick="sendTest()">Send Test Message</button>
        </div>
        
        <div id="advanced" class="interface">
            <h2>Advanced Interface</h2>
            <p>Connected Clients: <span id="client-count">0</span></p>
            <button onclick="getMetrics()">Get Metrics</button>
        </div>
        
        <script>
            let socket = null;
            
            function connectWebSocket() {
                socket = io();
                
                socket.on('connect', () => {
                    document.getElementById('ws-status').textContent = 'Connected';
                    document.getElementById('ws-status').style.color = '#00d4aa';
                });
                
                socket.on('welcome', (data) => {
                    console.log('Welcome:', data);
                });
                
                socket.on('mode_changed', (data) => {
                    console.log('Mode changed:', data);
                });
                
                socket.on('client_count', (data) => {
                    document.getElementById('client-count').textContent = data.count;
                });
            }
            
            function switchToSimple() {
                document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                document.querySelector('.mode-btn:nth-child(1)').classList.add('active');
                document.getElementById('simple').classList.add('active');
                document.getElementById('advanced').classList.remove('active');
                if (socket) socket.emit('mode_change', { mode: 'simple' });
            }
            
            function switchToAdvanced() {
                document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                document.querySelector('.mode-btn:nth-child(2)').classList.add('active');
                document.getElementById('simple').classList.remove('active');
                document.getElementById('advanced').classList.add('active');
                if (socket) socket.emit('mode_change', { mode: 'advanced' });
            }
            
            function sendTest() {
                if (socket) socket.emit('test_message', { text: 'Hello from client' });
            }
            
            function getMetrics() {
                if (socket) socket.emit('get_metrics');
            }
            
            // Initialize
            document.addEventListener('DOMContentLoaded', connectWebSocket);
        </script>
    </body>
    </html>
    '''

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")
    emit('welcome', {'message': 'Connected to Omega Minimal', 'time': 'Now'})
    
    # Update client count for all
    global active_clients
    active_clients += 1
    emit('client_count', {'count': active_clients}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
    global active_clients
    active_clients -= 1
    emit('client_count', {'count': active_clients}, broadcast=True)

@socketio.on('mode_change')
def handle_mode_change(data):
    mode = data.get('mode', 'simple')
    print(f"Client {request.sid[-6:]} switched to {mode} mode")
    emit('mode_changed', {'mode': mode, 'message': f'Switched to {mode}'})

@socketio.on('test_message')
def handle_test(data):
    print(f"Test message from {request.sid[-6:]}: {data}")
    emit('test_response', {'received': data, 'timestamp': 'Now'})

@socketio.on('get_metrics')
def handle_metrics():
    emit('metrics', {
        'health': 95,
        'clients': active_clients,
        'status': 'operational'
    })

if __name__ == '__main__':
    print("\n🚀 Server: http://localhost:8080")
    print("💡 Open in browser and test mode switching with WebSocket")
    print("-" * 60)
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)
