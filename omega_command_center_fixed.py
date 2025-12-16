#!/usr/bin/env python3
"""
PROJECT OMEGA - COMMAND CENTER (FIXED)
Fixed WebSocket and CSP issues for dual-interface functionality.
"""

import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'omega_fixed_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

print(f"\n{'='*70}")
print("   PROJECT OMEGA - COMMAND CENTER (FIXED)")
print("   Fixed CSP • Working WebSockets • Dual Interface")
print(f"{'='*70}")

# Store active clients and their modes
client_modes = {}

@app.route('/')
def index():
    """Serve the fixed HTML template"""
    return render_template('command_center_fixed.html')

@app.route('/api/simulate/<scenario>')
def run_simulation(scenario):
    """Run a simulation scenario"""
    simulations = {
        'port_scan_escalation': {
            'scenario': 'port_scan_escalation',
            'steps': [
                {'time': 'T+0m', 'event': 'Initial reconnaissance', 'severity': 'low'},
                {'time': 'T+2m', 'event': 'Deep port scanning', 'severity': 'medium'},
                {'time': 'T+5m', 'event': 'Vulnerability detection', 'severity': 'high'},
                {'time': 'T+8m', 'event': 'Exploit attempt', 'severity': 'critical'}
            ],
            'results': {
                'detection_probability': 0.92,
                'time_to_detect': '4.2 minutes',
                'recommended_response': 'Auto-block source IP'
            }
        }
    }
    
    if scenario in simulations:
        # Broadcast to all connected clients
        socketio.emit('simulation_complete', {
            'scenario': scenario,
            'results': simulations[scenario],
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify(simulations[scenario])
    
    return jsonify({'error': 'Unknown scenario'}), 404

# ===== WEB SOCKET EVENT HANDLERS =====
@socketio.on('connect')
def handle_connect():
    """Client connected"""
    client_id = request.sid
    client_modes[client_id] = 'simple'
    
    print(f"[SERVER] Client connected: {client_id}")
    
    # Send welcome message
    emit('connected', {
        'message': 'Welcome to Omega Command Center (Fixed)',
        'timestamp': datetime.now().isoformat(),
        'client_id': client_id[-6:]  # Short ID for display
    })
    
    # Also send to the specific client
    emit('mode_changed', {
        'mode': 'simple',
        'message': 'Initialized in Simple mode'
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    client_id = request.sid
    if client_id in client_modes:
        del client_modes[client_id]
    print(f"[SERVER] Client disconnected: {client_id}")

@socketio.on('mode_change')
def handle_mode_change(data):
    """Client changed interface mode"""
    client_id = request.sid
    new_mode = data.get('mode', 'simple')
    
    if new_mode in ['simple', 'advanced']:
        client_modes[client_id] = new_mode
        
        print(f"[SERVER] Client {client_id[-6:]} switched to {new_mode} mode")
        
        # Send confirmation back to client
        emit('mode_changed', {
            'mode': new_mode,
            'message': f'Successfully switched to {new_mode} mode',
            'timestamp': datetime.now().isoformat()
        })

@socketio.on('simple_action')
def handle_simple_action(data):
    """Handle simple action from client"""
    client_id = request.sid
    action = data.get('action', 'unknown')
    
    print(f"[SERVER] Simple action from {client_id[-6:]}: {action}")
    
    # Process the action
    action_results = {
        'scan_network': 'Network scan initiated. Scanning common ports...',
        'analyze_threats': 'ML analysis running on recent threat data...',
        'run_simulation': 'Starting defense simulation scenario...'
    }
    
    result = action_results.get(action, f'Action "{action}" received')
    
    # Send result back to client
    emit('action_complete', {
        'action': action,
        'result': result,
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    })

@socketio.on('module_command')
def handle_module_command(data):
    """Handle module command from advanced interface"""
    module = data.get('module', 'unknown')
    command = data.get('command', 'unknown')
    
    print(f"[SERVER] Module command: {module}.{command}")
    
    # Simulate processing
    emit('action_complete', {
        'action': f'{module}.{command}',
        'result': f'Module command executed: {module}.{command}',
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    })

@socketio.on('run_simulation')
def handle_run_simulation(data):
    """Handle simulation request"""
    scenario = data.get('scenario', 'port_scan_escalation')
    
    print(f"[SERVER] Running simulation: {scenario}")
    
    # Run the simulation
    simulation_result = {
        'scenario': scenario,
        'status': 'completed',
        'steps_executed': 4,
        'threats_detected': 3,
        'response_time': '4.2s',
        'timestamp': datetime.now().isoformat()
    }
    
    emit('simulation_complete', simulation_result)

@socketio.on('refresh_data')
def handle_refresh_data():
    """Handle data refresh request"""
    client_id = request.sid
    
    print(f"[SERVER] Data refresh requested by {client_id[-6:]}")
    
    # Send updated metrics
    emit('action_complete', {
        'action': 'refresh_data',
        'result': 'All data refreshed successfully',
        'timestamp': datetime.now().isoformat(),
        'status': 'success'
    })

@socketio.on('get_initial_data')
def handle_initial_data():
    """Send initial data to newly connected client"""
    client_id = request.sid
    
    print(f"[SERVER] Sending initial data to {client_id[-6:]}")
    
    initial_data = {
        'system_status': 'operational',
        'modules_active': ['predictive', 'voice', 'core'],
        'threat_level': 'low',
        'metrics': {
            'threats_blocked': 128,
            'anomalies_detected': 42,
            'predictive_accuracy': 52.8,
            'active_connections': len(client_modes)
        },
        'timestamp': datetime.now().isoformat()
    }
    
    emit('initial_data', initial_data)

def run_server(host='0.0.0.0', port=8080):
    """Run the fixed server"""
    print(f"\n{'🚀'*10} SERVER STARTUP {'🚀'*10}")
    print(f"📡 URL: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print(f"🔗 WebSocket: ws://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print(f"🎯 Features: Fixed CSP • Dual Interface • Real-Time WebSocket")
    print(f"{'─'*60}")
    print("💡 Open in browser and try switching between Simple/Advanced modes!")
    print(f"{'─'*60}\n")
    
    try:
        socketio.run(app, host=host, port=port, debug=False, use_reloader=False, log_output=False)
    except KeyboardInterrupt:
        print("\n[SERVER] Graceful shutdown")
    except Exception as e:
        print(f"\n[SERVER] Error: {e}")

if __name__ == "__main__":
    run_server(port=8080)
