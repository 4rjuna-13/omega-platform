#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA - COMMAND CENTER v2.0 with DECEPTION ENGINE
Phase 2E: Active Deception Implementation
"""

import os
import sys
import json
import time
import threading
import logging
from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO, emit
import numpy as np
import pickle
from datetime import datetime
import random

# Try to import deception engine
try:
    from deception_engine import DeceptionEngine
    import deception_api
    DECEPTION_AVAILABLE = True
except ImportError as e:
    DECEPTION_AVAILABLE = False
    print(f"[DECEPTION] Module not available: {e}")

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'omega_secure_key_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

class OmegaServer:
    def __init__(self):
        self.app = app
        self.socketio = socketio
        self.mode = "SIMPLE"
        self.clients = 0
        
        # Load threat model
        self.threat_model = self.load_threat_model()
        
        # Initialize deception engine
        if DECEPTION_AVAILABLE:
            self.deception_engine = DeceptionEngine(self)
            deception_api.setup_deception_api(self.app, self.deception_engine)
            print("[DECEPTION] Engine initialized")
        
        # Setup
        self.setup_routes()
        self.setup_socket_events()
        self.start_background_threads()
    
    def load_threat_model(self):
        try:
            with open('threat_model.pkl', 'rb') as f:
                model = pickle.load(f)
            print("[THREAT] Model loaded")
            return model
        except:
            print("[THREAT] Using simulated model")
            return None
    
    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('simple_command_center.html')
        
        @self.app.route('/api/status', methods=['GET'])
        def api_status():
            return jsonify({
                'status': 'online',
                'mode': self.mode,
                'deception_available': DECEPTION_AVAILABLE,
                'version': 'Omega v2.0 with Deception Engine'
            })
        
        @self.app.route('/api/switch', methods=['POST'])
        def switch_mode():
            data = request.get_json()
            if data and 'mode' in data:
                self.mode = data['mode']
                print(f"[MODE] {self.mode}")
            return jsonify({'mode': self.mode})
        
        @self.app.route('/api/threat/simulate', methods=['POST'])
        def simulate_threat():
            threat_level = random.randint(20, 95)
            threat_data = {
                'threat_score': threat_level,
                'timestamp': datetime.now().isoformat(),
            }
            self.socketio.emit('threat_update', threat_data)
            return jsonify(threat_data)
        
        @self.app.route('/api/scan', methods=['POST'])
        def start_scan():
            scan_id = f"scan_{int(time.time())}"
            scan_data = {'scan_id': scan_id, 'status': 'running'}
            
            def simulate_scan():
                for i in range(1, 11):
                    time.sleep(0.5)
                    self.socketio.emit('scan_update', {
                        'scan_id': scan_id,
                        'progress': i * 10
                    })
                self.socketio.emit('scan_complete', {
                    'scan_id': scan_id,
                    'status': 'completed'
                })
            
            threading.Thread(target=simulate_scan, daemon=True).start()
            return jsonify(scan_data)
    
    def setup_socket_events(self):
        @self.socketio.on('connect')
        def handle_connect():
            self.clients += 1
            print(f"[WEBSOCKET] Client connected: {request.sid}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.clients -= 1
        
        @self.socketio.on('get_metrics')
        def handle_get_metrics():
            metrics = self.get_system_metrics()
            self.socketio.emit('metrics_update', metrics)
        
        @self.socketio.on('send_command')
        def handle_command(data):
            command = data.get('command', '')
            response = self.process_command(command)
            self.socketio.emit('command_response', {
                'command': command,
                'response': response
            })
    
    def get_system_metrics(self):
        cpu = random.randint(5, 85)
        memory = random.randint(30, 90)
        threat_score = random.randint(10, 60)
        
        metrics = {
            'cpu': cpu,
            'memory': memory,
            'threat_level': threat_score,
            'timestamp': datetime.now().isoformat(),
            'mode': self.mode,
            'clients': self.clients
        }
        
        # Add deception metrics
        if DECEPTION_AVAILABLE and hasattr(self, 'deception_engine'):
            deception_stats = self.deception_engine.get_deception_stats()
            metrics['deception'] = {
                'active': deception_stats['active'],
                'level': deception_stats['level'],
                'honeypots': deception_stats['honeypots_active'],
                'connections': deception_stats['total_connections']
            }
        
        return metrics
    
    def process_command(self, command):
        cmd_lower = command.lower()
        
        # Deception commands
        if DECEPTION_AVAILABLE and hasattr(self, 'deception_engine'):
            if cmd_lower.startswith("deception start"):
                level = "MEDIUM"
                if "high" in cmd_lower:
                    level = "HIGH"
                elif "low" in cmd_lower:
                    level = "LOW"
                
                result = self.deception_engine.start_deception_mode(level)
                return f"Deception Engine started at {level} level"
            
            elif cmd_lower.startswith("deception stop"):
                result = self.deception_engine.stop_deception_mode()
                return "Deception Engine stopped"
            
            elif cmd_lower.startswith("deception status"):
                stats = self.deception_engine.get_deception_stats()
                return f"Deception: Active={stats['active']}, Honeypots={stats['honeypots_active']}"
        
        # Original commands
        if 'status' in cmd_lower:
            return "System operational"
        elif 'scan' in cmd_lower:
            return "Starting network scan"
        elif 'help' in cmd_lower:
            return "Commands: status, scan, deception [start/stop/status]"
        else:
            return f"Command: {command}"
    
    def start_background_threads(self):
        def metrics_loop():
            while True:
                time.sleep(2)
                metrics = self.get_system_metrics()
                self.socketio.emit('metrics_update', metrics)
        
        threading.Thread(target=metrics_loop, daemon=True).start()
        print("[THREADS] Background metrics started")

def main():
    print("\n" + "="*70)
    print("   🚀 PROJECT OMEGA v2.0 with DECEPTION ENGINE")
    print("   Port 8081 • Phase 2E: Active Deception")
    print("="*70 + "\n")
    
    if DECEPTION_AVAILABLE:
        print("📡 DECEPTION ENGINE READY:")
        print("   • Fake SSH Server (port 2222)")
        print("   • Fake Web Admin (port 8088)")
        print("   • Fake MySQL (port 3307)")
        print("")
    
    print("🌐 ACCESS: http://localhost:8081")
    print("💡 Commands: deception start [low/medium/high], deception stop, deception status")
    print("="*70 + "\n")
    
    server = OmegaServer()
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()

