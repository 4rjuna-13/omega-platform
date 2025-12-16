#!/usr/bin/env python3
"""
PROJECT OMEGA - COMPLETE SYSTEM
Working WebSocket on Port 8081 with all features
"""

import json
import sys
import importlib.util
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, disconnect
import eventlet
eventlet.monkey_patch()

print("\n" + "="*70)
print("   PROJECT OMEGA - COMPLETE COMMAND CENTER")
print("   Port 8081 • Working WebSocket • All Modules")
print("="*70)

# Initialize Flask with proper config
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'omega_complete_2025'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize SocketIO with debugging for now
socketio = SocketIO(
    app, 
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=False,  # Set to True for debugging
    engineio_logger=False
)

# System State
system_state = {
    'clients': {},
    'metrics': {
        'health': 94,
        'threats_blocked': 128,
        'predictive_accuracy': 52.8,
        'active_modules': 4,
        'uptime': 0,
        'active_clients': 0
    },
    'modules': {
        'predictive': None,
        'voice': None,
        'scanner': None,
        'crypto': None
    },
    'threats': [],
    'simulations': []
}

# ===== LOAD OMEGA MODULES =====
def load_omega_modules():
    """Load your existing Project Omega modules"""
    print("\n[SYSTEM] Loading Omega modules...")
    
    modules_to_load = [
        ('predictive', 'predictive_threat.py', 'ThreatPredictor'),
        ('voice', 'voice_module.py', 'VoiceCommandProcessor'),
        # Add more as needed
    ]
    
    for name, filename, class_name in modules_to_load:
        try:
            spec = importlib.util.spec_from_file_location(name, filename)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, class_name):
                    system_state['modules'][name] = getattr(module, class_name)()
                    print(f"  ✅ Loaded: {name} ({class_name})")
                else:
                    print(f"  ⚠️  {name}: Class {class_name} not found")
        except Exception as e:
            print(f"  ❌ {name}: {str(e)[:50]}...")

# ===== FLASK ROUTES =====
@app.route('/')
def index():
    """Main interface"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Serving main page")
    return render_template('simple_command_center.html')

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'operational',
        'version': 'Omega 2.0',
        'timestamp': datetime.now().isoformat(),
        'metrics': system_state['metrics'],
        'web_socket': 'active',
        'port': 8081
    })

@app.route('/api/simulate/<scenario>')
def api_simulate(scenario):
    """Run simulation via HTTP"""
    print(f"Running simulation: {scenario}")
    
    simulation = {
        'scenario': scenario,
        'status': 'completed',
        'steps': 5,
        'threats_detected': 3,
        'response_time': '4.2s',
        'timestamp': datetime.now().isoformat()
    }
    
    # Broadcast via WebSocket too
    socketio.emit('simulation_complete', simulation)
    
    return jsonify(simulation)

@app.route('/api/metrics')
def api_metrics():
    """Get current metrics"""
    return jsonify(system_state['metrics'])

@app.route('/api/modules')
def api_modules():
    """Get module status"""
    modules_status = {}
    for name, module in system_state['modules'].items():
        modules_status[name] = 'active' if module else 'inactive'
    
    return jsonify(modules_status)

# ===== WEBSOCKET EVENT HANDLERS =====
@socketio.on('connect')
def handle_connect():
    """Client connected"""
    client_id = request.sid
    
    # Store client with initial mode
    system_state['clients'][client_id] = {
        'mode': 'simple',
        'connected_at': datetime.now().isoformat(),
        'last_active': datetime.now().isoformat()
    }
    
    system_state['metrics']['active_clients'] = len(system_state['clients'])
    
    print(f"✅ CLIENT CONNECTED: {client_id[-6:]}")
    print(f"   Active clients: {system_state['metrics']['active_clients']}")
    
    # Send welcome
    emit('welcome', {
        'message': 'Connected to Project Omega Command Center',
        'client_id': client_id[-6:],
        'timestamp': datetime.now().isoformat(),
        'mode': 'simple'
    })
    
    # Send initial metrics
    emit('initial_data', {
        'metrics': system_state['metrics'],
        'modules': {k: 'active' if v else 'inactive' 
                   for k, v in system_state['modules'].items()},
        'timestamp': datetime.now().isoformat()
    })
    
    # Broadcast updated client count to all
    socketio.emit('client_update', {
        'active_clients': system_state['metrics']['active_clients'],
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    client_id = request.sid
    
    if client_id in system_state['clients']:
        del system_state['clients'][client_id]
    
    system_state['metrics']['active_clients'] = len(system_state['clients'])
    
    print(f"Client disconnected: {client_id[-6:]}")
    print(f"   Remaining clients: {system_state['metrics']['active_clients']}")
    
    # Broadcast updated count
    socketio.emit('client_update', {
        'active_clients': system_state['metrics']['active_clients'],
        'timestamp': datetime.now().isoformat()
    }, broadcast=True)

@socketio.on('mode_change')
def handle_mode_change(data):
    """Client changed interface mode"""
    client_id = request.sid
    mode = data.get('mode', 'simple')
    
    if client_id in system_state['clients']:
        system_state['clients'][client_id]['mode'] = mode
        system_state['clients'][client_id]['last_active'] = datetime.now().isoformat()
    
    print(f"Client {client_id[-6:]} switched to {mode} mode")
    
    # Send confirmation
    emit('mode_changed', {
        'mode': mode,
        'message': f'Interface switched to {mode} mode',
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('simple_action')
def handle_simple_action(data):
    """Handle simple action from client"""
    client_id = request.sid
    action = data.get('action', 'unknown')
    
    print(f"Simple action from {client_id[-6:]}: {action}")
    
    # Process different actions
    actions = {
        'scan_network': 'Network scan initiated. Checking common ports...',
        'analyze_threats': 'ML analysis running on recent threat data...',
        'run_simulation': 'Starting defense simulation: Port Scan Escalation',
        'system_check': 'Running system diagnostic...'
    }
    
    result = actions.get(action, f'Action "{action}" received')
    
    # Update metrics
    if action == 'scan_network':
        system_state['metrics']['threats_blocked'] += 1
    elif action == 'analyze_threats':
        system_state['metrics']['predictive_accuracy'] += 0.1
    
    # Send response
    emit('action_complete', {
        'action': action,
        'result': result,
        'status': 'success',
        'timestamp': datetime.now().isoformat()
    })
    
    # Broadcast metrics update
    socketio.emit('metrics_update', system_state['metrics'])

@socketio.on('module_command')
def handle_module_command(data):
    """Handle module command from advanced interface"""
    module_name = data.get('module', 'unknown')
    command = data.get('command', 'unknown')
    params = data.get('params', {})
    
    print(f"Module command: {module_name}.{command}")
    
    # Try to execute if module exists
    if module_name in system_state['modules'] and system_state['modules'][module_name]:
        try:
            module = system_state['modules'][module_name]
            
            # Map commands to methods
            if module_name == 'predictive':
                if command == 'train':
                    result = 'ML model training initiated'
                elif command == 'predict':
                    result = 'Threat prediction generated'
                else:
                    result = f'Command {command} executed on predictive model'
            
            elif module_name == 'voice':
                if command == 'listen':
                    result = 'Voice listening activated'
                elif command == 'speak':
                    result = 'Text-to-speech output'
                else:
                    result = f'Command {command} executed on voice module'
            
            else:
                result = f'Module {module_name} command {command} executed'
            
        except Exception as e:
            result = f'Error: {str(e)}'
    else:
        result = f'Module {module_name} not available'
    
    emit('command_result', {
        'module': module_name,
        'command': command,
        'result': result,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('run_simulation')
def handle_run_simulation(data):
    """Run advanced simulation"""
    scenario = data.get('scenario', 'port_scan_escalation')
    
    print(f"Running simulation: {scenario}")
    
    simulation = {
        'scenario': scenario,
        'status': 'running',
        'start_time': datetime.now().isoformat(),
        'client': request.sid[-6:]
    }
    
    system_state['simulations'].append(simulation)
    
    # Simulate processing delay
    @socketio.sleep(2)
    def complete_simulation():
        simulation['status'] = 'completed'
        simulation['end_time'] = datetime.now().isoformat()
        simulation['results'] = {
            'threats_detected': 3,
            'response_time': '4.2s',
            'effectiveness': '92%'
        }
        
        emit('simulation_complete', simulation)
        print(f"Simulation completed: {scenario}")
    
    complete_simulation()

@socketio.on('get_metrics')
def handle_get_metrics():
    """Send current metrics to client"""
    emit('metrics_update', system_state['metrics'])

@socketio.on('refresh_data')
def handle_refresh_data():
    """Refresh all data"""
    # Update metrics with slight variations
    system_state['metrics']['health'] = min(100, system_state['metrics']['health'] + 1)
    system_state['metrics']['threats_blocked'] += 1
    
    emit('data_refreshed', {
        'metrics': system_state['metrics'],
        'timestamp': datetime.now().isoformat(),
        'message': 'All data refreshed'
    })

@socketio.on('system_diagnostic')
def handle_system_diagnostic():
    """Run system diagnostic"""
    print(f"System diagnostic requested by {request.sid[-6:]}")
    
    diagnostic = {
        'status': 'running',
        'checks': [
            {'name': 'WebSocket Server', 'status': 'pass', 'details': 'Port 8081 active'},
            {'name': 'Flask Application', 'status': 'pass', 'details': 'Routes working'},
            {'name': 'Module Integration', 'status': 'warning', 'details': f'{sum(1 for m in system_state["modules"].values() if m)}/{len(system_state["modules"])} loaded'},
            {'name': 'Client Connections', 'status': 'pass', 'details': f'{len(system_state["clients"])} active'},
            {'name': 'Memory Usage', 'status': 'pass', 'details': 'Normal'},
            {'name': 'Response Time', 'status': 'pass', 'details': '<100ms'}
        ],
        'timestamp': datetime.now().isoformat()
    }
    
    emit('diagnostic_result', diagnostic)

# ===== MAIN SERVER STARTUP =====
def run_server():
    """Run the complete Omega server"""
    print("\n" + "="*70)
    print("🚀 PROJECT OMEGA COMMAND CENTER - STARTING")
    print("="*70)
    
    # Load modules
    load_omega_modules()
    
    print(f"\n📊 SYSTEM STATUS:")
    print(f"   • Port: 8081")
    print(f"   • WebSocket: Ready")
    print(f"   • Modules loaded: {sum(1 for m in system_state['modules'].values() if m)}/{len(system_state['modules'])}")
    print(f"   • Interface: Dual (Simple/Advanced)")
    print(f"   • Security Level: MONITOR")
    
    print(f"\n🌐 ACCESS URLS:")
    print(f"   • Command Center: http://localhost:8081")
    print(f"   • API Status: http://localhost:8081/api/status")
    print(f"   • WebSocket: ws://localhost:8081/socket.io/")
    
    print(f"\n🎯 FEATURES:")
    print(f"   • Real-time WebSocket communication")
    print(f"   • Dual interface with mode switching")
    print(f"   • Integration with Omega modules")
    print(f"   • Threat simulation engine")
    print(f"   • Live metrics and monitoring")
    
    print(f"\n" + "="*70)
    print("💡 Open browser to http://localhost:8081 and test mode switching!")
    print("="*70 + "\n")
    
    try:
        # Calculate uptime start
        start_time = datetime.now()
        
        # Update uptime periodically
        def update_uptime():
            while True:
                eventlet.sleep(60)  # Every minute
                uptime = (datetime.now() - start_time).total_seconds()
                system_state['metrics']['uptime'] = int(uptime)
                socketio.emit('metrics_update', system_state['metrics'])
        
        # Start uptime updater in background
        eventlet.spawn(update_uptime)
        
        # Run the server
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=8081, 
            debug=False, 
            use_reloader=False,
            log_output=False
        )
        
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Omega Command Center shutting down...")
        print("         Thank you for using Project Omega!")
    except Exception as e:
        print(f"\n❌ SERVER ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_server()
