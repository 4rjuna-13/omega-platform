#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA v3.0 - Integrated Autonomous Response
"""

import os
import sys
import json
import time
import threading
import logging
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import numpy as np
import pickle
from datetime import datetime
import random

# Try to import modules
try:
    from deception_engine import DeceptionEngine
    import deception_api
    DECEPTION_AVAILABLE = True
except ImportError:
    DECEPTION_AVAILABLE = False

try:
    from autonomous_response import AutonomousResponse
    import response_api
    RESPONSE_AVAILABLE = True
except ImportError:
    RESPONSE_AVAILABLE = False

# Setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
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
        
        # Initialize modules
        self.init_modules()
        
        # Setup
        self.setup_routes()
        self.setup_socket_events()
        self.start_background_threads()
        
        print("[SYSTEM] Omega v3.0 Integrated ready")
    
    def load_threat_model(self):
        try:
            with open('threat_model.pkl', 'rb') as f:
                model = pickle.load(f)
            print("[THREAT] Model loaded")
            return model
        except:
            print("[THREAT] Using simulation")
            return None
    
    def init_modules(self):
        # Deception Engine
        if DECEPTION_AVAILABLE:
            self.deception_engine = DeceptionEngine(self)
            deception_api.setup_deception_api(self.app, self.deception_engine)
            print("[MODULES] Deception Engine ready")
        
        # Autonomous Response
        if RESPONSE_AVAILABLE:
            self.response_engine = AutonomousResponse(self)
            response_api.setup_response_api(self.app, self.response_engine)
            print("[MODULES] Autonomous Response ready")
            
            # Link deception to response
            self.link_deception_response()
    
    def link_deception_response(self):
        """Link deception events to response system"""
        if not DECEPTION_AVAILABLE or not RESPONSE_AVAILABLE:
            return
        
        original_log = self.deception_engine.log_deception_event
        
        def enhanced_log(honeypot_id, event_type, source_ip, details, severity):
            # Original logging
            original_log(honeypot_id, event_type, source_ip, details, severity)
            
            # Trigger response if active
            if self.response_engine.is_active:
                threat_data = {
                    'event_type': event_type,
                    'source_ip': source_ip,
                    'details': details,
                    'severity': severity,
                    'honeypot_id': honeypot_id,
                    'timestamp': datetime.now().isoformat()
                }
                
                self.response_engine.handle_threat(threat_data)
                print(f"[INTEGRATION] Deception → Response: {event_type} from {source_ip}")
        
        self.deception_engine.log_deception_event = enhanced_log
        print("[INTEGRATION] Deception linked to Response")
    
    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('simple_command_center.html')
        
        @self.app.route('/api/status', methods=['GET'])
        def api_status():
            return jsonify({
                'status': 'online',
                'version': 'Omega v3.0 Integrated',
                'mode': self.mode,
                'deception': DECEPTION_AVAILABLE,
                'response': RESPONSE_AVAILABLE,
                'clients': self.clients
            })
        
        @self.app.route('/api/switch', methods=['POST'])
        def switch_mode():
            data = request.get_json()
            if data and 'mode' in data:
                self.mode = data['mode']
                print(f"[MODE] {self.mode}")
            return jsonify({'mode': self.mode})
    
    def setup_socket_events(self):
        @self.socketio.on('connect')
        def handle_connect():
            self.clients += 1
            print(f"[WEBSOCKET] Client connected: {request.sid}")
            emit('system_message', {
                'message': 'Connected to Omega v3.0',
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.clients -= 1
        
        @self.socketio.on('get_metrics')
        def handle_get_metrics():
            metrics = self.get_system_metrics()
            emit('metrics_update', metrics)
        
        @self.socketio.on('send_command')
        def handle_command(data):
            command = data.get('command', '')
            response = self.process_command(command)
            emit('command_response', {
                'command': command,
                'response': response,
                'timestamp': datetime.now().isoformat()
            })
    
    def get_system_metrics(self):
        cpu = random.randint(10, 80)
        memory = random.randint(30, 85)
        
        metrics = {
            'cpu': cpu,
            'memory': memory,
            'threat_level': random.randint(5, 65),
            'mode': self.mode,
            'clients': self.clients,
            'timestamp': datetime.now().isoformat()
        }
        
        if DECEPTION_AVAILABLE and hasattr(self, 'deception_engine'):
            stats = self.deception_engine.get_deception_stats()
            metrics['deception'] = {
                'active': stats['active'],
                'honeypots': stats['honeypots_active'],
                'connections': stats['total_connections']
            }
        
        if RESPONSE_AVAILABLE and hasattr(self, 'response_engine'):
            stats = self.response_engine.get_response_stats()
            metrics['response'] = {
                'active': stats['active'],
                'level': stats['level'],
                'blocked_ips': stats['blocked_ips'],
                'total_responses': stats['total_responses']
            }
        
        return metrics
    
    def process_command(self, command):
        cmd_lower = command.lower()
        
        # Response commands
        if RESPONSE_AVAILABLE and hasattr(self, 'response_engine'):
            if cmd_lower.startswith("response activate"):
                level = "MODERATE"
                if "conservative" in cmd_lower:
                    level = "CONSERVATIVE"
                elif "aggressive" in cmd_lower:
                    level = "AGGRESSIVE"
                
                result = self.response_engine.activate_response_mode(level)
                return f"🤖 Response: ACTIVATED at {level} level"
            
            elif cmd_lower.startswith("response deactivate"):
                result = self.response_engine.deactivate_response_mode()
                return "🤖 Response: DEACTIVATED"
            
            elif cmd_lower.startswith("response status"):
                stats = self.response_engine.get_response_stats()
                return f"🤖 Response: Active={stats['active']}, Level={stats['level']}, Blocked IPs={stats['blocked_ips']}"
            
            elif cmd_lower.startswith("response test"):
                result = self.response_engine.test_response()
                return "🤖 Response: Test threat sent"
        
        # Deception commands
        if DECEPTION_AVAILABLE and hasattr(self, 'deception_engine'):
            if cmd_lower.startswith("deception start"):
                level = "MEDIUM"
                if "low" in cmd_lower:
                    level = "LOW"
                elif "high" in cmd_lower:
                    level = "HIGH"
                
                result = self.deception_engine.start_deception_mode(level)
                return f"🕵️ Deception: Started at {level} level"
            
            elif cmd_lower.startswith("deception stop"):
                result = self.deception_engine.stop_deception_mode()
                return "🕵️ Deception: Stopped"
            
            elif cmd_lower.startswith("deception status"):
                stats = self.deception_engine.get_deception_stats()
                return f"🕵️ Deception: Active={stats['active']}, Honeypots={stats['honeypots_active']}"
        
        # System commands
        if 'help' in cmd_lower:
            help_text = "📋 COMMANDS:\n"
            if RESPONSE_AVAILABLE:
                help_text += "🤖 response activate [conservative/moderate/aggressive]\n"
                help_text += "🤖 response deactivate\n"
                help_text += "🤖 response status\n"
                help_text += "🤖 response test\n"
            if DECEPTION_AVAILABLE:
                help_text += "🕵️ deception start [low/medium/high]\n"
                help_text += "🕵️ deception stop\n"
                help_text += "🕵️ deception status\n"
            return help_text
        
        return f"Command: '{command}' (type 'help')"
    
    def start_background_threads(self):
        def metrics_loop():
            while True:
                time.sleep(3)
                metrics = self.get_system_metrics()
                self.socketio.emit('metrics_update', metrics)
        
        threading.Thread(target=metrics_loop, daemon=True).start()
        print("[THREADS] Background monitoring started")

def main():
    print("\n" + "="*70)
    print("   🚀 PROJECT OMEGA v3.0 - AUTONOMOUS RESPONSE INTEGRATED")
    print("="*70 + "\n")
    
    print("🎯 COMPLETE SECURITY LOOP:")
    print("   Detection → Deception → Automated Response")
    print("")
    
    if DECEPTION_AVAILABLE:
        print("🕵️ DECEPTION ENGINE: Available")
    else:
        print("🕵️ DECEPTION ENGINE: Not available")
    
    if RESPONSE_AVAILABLE:
        print("🤖 AUTONOMOUS RESPONSE: Available")
        print("   • Levels: CONSERVATIVE, MODERATE, AGGRESSIVE")
        print("   • Actions: IP blocking, alerts, network isolation")
    else:
        print("🤖 AUTONOMOUS RESPONSE: Not available")
    
    print("")
    print("🌐 ACCESS: http://localhost:8081")
    print("")
    print("💡 QUICK TEST:")
    print("   1. 'response activate moderate'")
    print("   2. 'deception start medium'")
    print("   3. Connect to honeypots to trigger automated response")
    print("="*70 + "\n")
    
    server = OmegaServer()
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()

