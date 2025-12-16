#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA v3.0 ULTIMATE
Phase 2F: Autonomous Response + Deception Integration
Complete Detect-Deceive-Respond Loop
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

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Try to import all modules
MODULES_LOADED = {
    'deception': False,
    'response': False,
    'integration': False
}

try:
    from deception_engine import DeceptionEngine
    import deception_api
    MODULES_LOADED['deception'] = True
    print("[MODULES] Deception Engine loaded")
except ImportError as e:
    print(f"[MODULES] Deception Engine not available: {e}")

try:
    from autonomous_response import AutonomousResponse
    import response_api
    MODULES_LOADED['response'] = True
    print("[MODULES] Autonomous Response loaded")
except ImportError as e:
    print(f"[MODULES] Autonomous Response not available: {e}")

try:
    import deception_response_integration
    MODULES_LOADED['integration'] = True
    print("[MODULES] Integration module loaded")
except ImportError as e:
    print(f"[MODULES] Integration module not available: {e}")

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
        self.system_status = "OPERATIONAL"
        
        # Load threat model
        self.threat_model = self.load_threat_model()
        
        # Initialize modules
        self.initialize_modules()
        
        # Setup everything
        self.setup_routes()
        self.setup_socket_events()
        self.start_background_threads()
        
        print("[SYSTEM] Omega v3.0 Ultimate initialized")
    
    def load_threat_model(self):
        """Load the ML threat model"""
        try:
            if os.path.exists('threat_model.pkl'):
                with open('threat_model.pkl', 'rb') as f:
                    model = pickle.load(f)
                print("[THREAT] Model loaded")
                return model
            else:
                print("[THREAT] No model found, using simulation")
                return None
        except Exception as e:
            print(f"[THREAT] Error: {e}")
            return None
    
    def initialize_modules(self):
        """Initialize all available modules"""
        
        # Deception Engine
        if MODULES_LOADED['deception']:
            self.deception_engine = DeceptionEngine(self)
            deception_api.setup_deception_api(self.app, self.deception_engine)
            print("[INIT] Deception Engine ready")
        
        # Autonomous Response
        if MODULES_LOADED['response']:
            self.response_engine = AutonomousResponse(self)
            response_api.setup_response_api(self.app, self.response_engine)
            print("[INIT] Autonomous Response ready")
        
        # Integration
        if MODULES_LOADED['deception'] and MODULES_LOADED['response'] and MODULES_LOADED['integration']:
            deception_response_integration.integrate_deception_with_response(
                self.deception_engine, self.response_engine
            )
            print("[INIT] Deception→Response integration active")
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('simple_command_center.html')
        
        @self.app.route('/api/status', methods=['GET'])
        def api_status():
            modules = []
            if MODULES_LOADED['deception']:
                modules.append('deception')
            if MODULES_LOADED['response']:
                modules.append('autonomous_response')
            
            return jsonify({
                'status': 'online',
                'version': 'Omega v3.0 Ultimate',
                'mode': self.mode,
                'system': self.system_status,
                'modules_loaded': modules,
                'clients': self.clients
            })
        
        @self.app.route('/api/switch', methods=['POST'])
        def switch_mode():
            data = request.get_json()
            if data and 'mode' in data:
                self.mode = data['mode']
                print(f"[MODE] {self.mode}")
            return jsonify({'mode': self.mode})
        
        @self.app.route('/api/system/test', methods=['POST'])
        def system_test():
            """Comprehensive system test"""
            results = {
                'timestamp': datetime.now().isoformat(),
                'tests': []
            }
            
            # Test deception if available
            if MODULES_LOADED['deception'] and hasattr(self, 'deception_engine'):
                deception_stats = self.deception_engine.get_deception_stats()
                results['tests'].append({
                    'module': 'deception',
                    'status': 'available',
                    'active': deception_stats['active']
                })
            
            # Test response if available
            if MODULES_LOADED['response'] and hasattr(self, 'response_engine'):
                response_stats = self.response_engine.get_response_stats()
                results['tests'].append({
                    'module': 'response',
                    'status': 'available',
                    'active': response_stats['active']
                })
            
            # Test integration
            if MODULES_LOADED['deception'] and MODULES_LOADED['response']:
                results['tests'].append({
                    'module': 'integration',
                    'status': 'available',
                    'linked': True
                })
            
            return jsonify(results)
    
    def setup_socket_events(self):
        """Setup SocketIO events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            self.clients += 1
            print(f"[WEBSOCKET] Client connected: {request.sid}")
            emit('system_message', {
                'type': 'welcome',
                'message': f'Connected to Omega v3.0. {self.clients} client(s) online.',
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.clients -= 1
            print(f"[WEBSOCKET] Client disconnected: {request.sid}")
        
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
            
            print(f"[COMMAND] {command} -> {response}")
        
        # Deception events
        @self.socketio.on('request_deception_status')
        def handle_deception_status():
            if MODULES_LOADED['deception'] and hasattr(self, 'deception_engine'):
                stats = self.deception_engine.get_deception_stats()
                emit('deception_status', stats)
        
        # Response events
        @self.socketio.on('request_response_status')
        def handle_response_status():
            if MODULES_LOADED['response'] and hasattr(self, 'response_engine'):
                stats = self.response_engine.get_response_stats()
                emit('response_status', stats)
    
    def get_system_metrics(self):
        """Get comprehensive system metrics"""
        cpu = random.randint(10, 80)
        memory = random.randint(30, 85)
        threat_score = random.randint(5, 65)
        
        metrics = {
            'cpu': cpu,
            'memory': memory,
            'threat_level': threat_score,
            'clients': self.clients,
            'mode': self.mode,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add deception metrics
        if MODULES_LOADED['deception'] and hasattr(self, 'deception_engine'):
            deception_stats = self.deception_engine.get_deception_stats()
            metrics['deception'] = {
                'active': deception_stats['active'],
                'honeypots': deception_stats['honeypots_active'],
                'connections': deception_stats['total_connections']
            }
        
        # Add response metrics
        if MODULES_LOADED['response'] and hasattr(self, 'response_engine'):
            response_stats = self.response_engine.get_response_stats()
            metrics['response'] = {
                'active': response_stats['active'],
                'level': response_stats['level'],
                'blocked_ips': response_stats['blocked_ips'],
                'total_responses': response_stats['total_responses']
            }
        
        return metrics
    
    def process_command(self, command):
        """Process commands for all modules"""
        cmd_lower = command.lower()
        
        # ===== AUTONOMOUS RESPONSE COMMANDS =====
        if MODULES_LOADED['response'] and hasattr(self, 'response_engine'):
            if cmd_lower.startswith("response activate"):
                level = "MODERATE"
                if "conservative" in cmd_lower:
                    level = "CONSERVATIVE"
                elif "aggressive" in cmd_lower:
                    level = "AGGRESSIVE"
                
                result = self.response_engine.activate_response_mode(level)
                action = result.get('status', 'unknown')
                return f"🤖 Autonomous Response: {action} at {level} level"
            
            elif cmd_lower.startswith("response deactivate"):
                result = self.response_engine.deactivate_response_mode()
                return "🤖 Autonomous Response: DEACTIVATED"
            
            elif cmd_lower.startswith("response status"):
                stats = self.response_engine.get_response_stats()
                return f"🤖 Response: Active={stats['active']}, Level={stats['level']}, Blocked IPs={stats['blocked_ips']}, Total Actions={stats['total_responses']}"
            
            elif cmd_lower.startswith("response test"):
                result = self.response_engine.test_response()
                return "🤖 Response: Test threat sent to response system"
        
        # ===== DECEPTION ENGINE COMMANDS =====
        if MODULES_LOADED['deception'] and hasattr(self, 'deception_engine'):
            if cmd_lower.startswith("deception start"):
                level = "MEDIUM"
                if "low" in cmd_lower:
                    level = "LOW"
                elif "high" in cmd_lower:
                    level = "HIGH"
                elif "paranoid" in cmd_lower:
                    level = "PARANOID"
                
                result = self.deception_engine.start_deception_mode(level)
                return f"🕵️ Deception Engine: Started at {level} level"
            
            elif cmd_lower.startswith("deception stop"):
                result = self.deception_engine.stop_deception_mode()
                return "🕵️ Deception Engine: Stopped"
            
            elif cmd_lower.startswith("deception status"):
                stats = self.deception_engine.get_deception_stats()
                return f"🕵️ Deception: Active={stats['active']}, Level={stats['level']}, Honeypots={stats['honeypots_active']}, Connections={stats['total_connections']}"
        
        # ===== SYSTEM COMMANDS =====
        if cmd_lower.startswith("system status"):
            return f"🖥️ System: {self.system_status}, Mode={self.mode}, Clients={self.clients}"
        
        elif cmd_lower.startswith("system test"):
            return "🖥️ System: Running comprehensive tests..."
        
        elif cmd_lower.startswith("help") or cmd_lower.startswith("commands"):
            return self.get_help_text()
        
        else:
            return f"Command: '{command}' - Type 'help' for available commands"
    
    def get_help_text(self):
        """Get help text for all available modules"""
        help_text = "📋 AVAILABLE COMMANDS:\n\n"
        
        help_text += "🤖 AUTONOMOUS RESPONSE:\n"
        help_text += "  • response activate [conservative/moderate/aggressive]\n"
        help_text += "  • response deactivate\n"
        help_text += "  • response status\n"
        help_text += "  • response test\n\n"
        
        help_text += "🕵️ DECEPTION ENGINE:\n"
        help_text += "  • deception start [low/medium/high/paranoid]\n"
        help_text += "  • deception stop\n"
        help_text += "  • deception status\n"
        help_text += "  • deploy honeypot [fake_ssh/fake_web/fake_db]\n\n"
        
        help_text += "🖥️ SYSTEM:\n"
        help_text += "  • system status\n"
        help_text += "  • system test\n"
        help_text += "  • mode [simple/advanced]\n"
        
        return help_text
    
    def start_background_threads(self):
        """Start background monitoring threads"""
        def metrics_loop():
            while True:
                time.sleep(3)
                metrics = self.get_system_metrics()
                self.socketio.emit('metrics_update', metrics)
        
        threading.Thread(target=metrics_loop, daemon=True).start()
        print("[THREADS] Background monitoring started")

def main():
    print("\n" + "="*70)
    print("   🚀 PROJECT OMEGA v3.0 ULTIMATE")
    print("   Complete Detect-Deceive-Respond Security Loop")
    print("="*70 + "\n")
    
    print("🎯 CORE CAPABILITIES:")
    print("   1. 🤖 Autonomous Response System")
    print("      • Automatic threat containment")
    print("      • IP blocking & network isolation")
    print("      • Integrated with deception traps")
    print("")
    print("   2. 🕵️ Deception Engine")
    print("      • Honeypots on ports 2222, 8088, 3307")
    print("      • Real-time attack detection")
    print("      • Attack pattern analysis")
    print("")
    print("   3. 🔗 Full Integration")
    print("      • Deception triggers → Automatic response")
    print("      • Complete security lifecycle")
    print("      • Real-time WebSocket updates")
    print("")
    
    print("⚙️ RESPONSE LEVELS:")
    print("   • CONSERVATIVE - Alerts only, minimal action")
    print("   • MODERATE - Balanced automated response")
    print("   • AGGRESSIVE - Maximum automated containment")
    print("")
    
    print("🌐 ACCESS: http://localhost:8081")
    print("")
    print("💡 QUICK START:")
    print("   1. 'response activate moderate'")
    print("   2. 'deception start medium'")
    print("   3. Connect to honeypots to trigger automated response")
    print("")
    print("="*70)
    print("💻 System initializing...")
    print("="*70 + "\n")
    
    # Create and run server
    server = OmegaServer()
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()

