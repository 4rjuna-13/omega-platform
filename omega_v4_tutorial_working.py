#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA v4.0 - TUTORIAL EDITION (WORKING)
Phase 2G: Complete Learning Environment - Simplified
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

# Tutorial Engine - Phase 2G
try:
    from tutorial_engine import TutorialEngine
    import tutorial_api
    import tutorial_integration
    TUTORIAL_AVAILABLE = True
    print("[MODULES] Tutorial Engine available")
except ImportError as e:
    print(f"[MODULES] Tutorial Engine not available: {e}")
    TUTORIAL_AVAILABLE = False

# Setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'omega_secure_key_2025'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

class OmegaServer:
    def __init__(self):
        self.app = app
        self.socketio = socketio
        self.mode = "TUTORIAL"  # Start in tutorial mode
        self.clients = 0
        
        # Load threat model
        self.threat_model = self.load_threat_model()
        
        # Initialize ALL modules
        self.init_modules()
        
        # Setup everything
        self.setup_routes()
        self.setup_socket_events()
        self.start_background_threads()
        
        print(f"\n{'='*70}")
        print("🚀 PROJECT OMEGA v4.0 - TUTORIAL EDITION READY")
        print("📍 Phase 2G: Interactive Learning & Safe Sandbox")
        print(f"{'='*70}")
        print("\n✨ Key Features:")
        print("   • Complete Tutorial System (5 structured tutorials)")
        print("   • Safe Sandbox Mode for zero-risk experimentation")
        print("   • Progressive Learning Path (Beginner → Advanced)")
        print("   • Achievement & Badge System")
        print("   • Training Scenarios (Data Breach, Ransomware)")
        print(f"\n📊 Launch Status: READY FOR ONBOARDING")
        print("💡 First-time users: Type 'tutorial start welcome'")
        print(f"{'='*70}\n")
    
    def load_threat_model(self):
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
    
    def init_modules(self):
        """Initialize all available modules"""
        
        # Deception Engine
        if DECEPTION_AVAILABLE:
            self.deception_engine = DeceptionEngine(self)
            deception_api.setup_deception_api(self.app, self.deception_engine)
            print("[INIT] Deception Engine ready")
        
        # Autonomous Response
        if RESPONSE_AVAILABLE:
            self.response_engine = AutonomousResponse(self)
            response_api.setup_response_api(self.app, self.response_engine)
            print("[INIT] Autonomous Response ready")
        
        # Tutorial Engine (NEW - Phase 2G)
        if TUTORIAL_AVAILABLE:
            self.tutorial_engine = TutorialEngine(self)
            tutorial_integration.integrate_tutorial_with_commands(self, self.tutorial_engine)
            print("[INIT] Tutorial Engine ready")
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('omega_tutorial_dashboard.html')
        
        @self.app.route('/api/status', methods=['GET'])
        def api_status():
            modules = []
            if DECEPTION_AVAILABLE: modules.append('deception')
            if RESPONSE_AVAILABLE: modules.append('response')
            if TUTORIAL_AVAILABLE: modules.append('tutorial')
            
            return jsonify({
                'status': 'online',
                'version': 'Omega v4.0 - Tutorial Edition',
                'mode': self.mode,
                'modules_loaded': modules,
                'clients': self.clients,
                'welcome_message': 'Ready for learning! Type "tutorial start welcome" to begin.'
            })
        
        @self.app.route('/api/command/help', methods=['GET'])
        def command_help():
            """Comprehensive help for tutorial edition"""
            help_data = {
                'welcome': '🚀 Welcome to Project Omega v4.0 Tutorial Edition!',
                'getting_started': [
                    'tutorial start welcome - Start your first tutorial',
                    'tutorial list - See all available tutorials',
                    'tutorial status - Check your progress',
                    'sandbox activate - Enable safe experimentation mode',
                    'help - Show this help message'
                ],
                'tutorial_commands': [
                    'tutorial start defense_basics - Learn defensive security',
                    'tutorial start deception_101 - Master honeypot deployment',
                    'tutorial start autonomous_response - Learn automated defense',
                    'tutorial start sandbox_lab - Advanced experimentation'
                ]
            }
            
            if DECEPTION_AVAILABLE:
                help_data['deception_commands'] = [
                    'deception start [low/medium/high] - Start deception engine',
                    'deception stop - Stop deception engine',
                    'deception status - Check deception status'
                ]
            
            if RESPONSE_AVAILABLE:
                help_data['response_commands'] = [
                    'response activate [conservative/moderate/aggressive] - Enable response',
                    'response deactivate - Disable response',
                    'response status - Check response status'
                ]
            
            return jsonify(help_data)
        
        # Setup tutorial API if available (with socketio parameter)
        if TUTORIAL_AVAILABLE:
            # Check if tutorial_api accepts socketio parameter
            import inspect
            sig = inspect.signature(tutorial_api.setup_tutorial_api)
            params = list(sig.parameters.keys())
            
            if len(params) >= 3:  # Function accepts app, tutorial_engine, socketio
                tutorial_api.setup_tutorial_api(self.app, self.tutorial_engine, self.socketio)
            else:  # Original version without socketio
                tutorial_api.setup_tutorial_api(self.app, self.tutorial_engine)
            print("[ROUTES] Tutorial API routes added")
    
    def setup_socket_events(self):
        """Setup SocketIO events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            self.clients += 1
            client_id = request.sid
            
            # Welcome message
            emit('system_message', {
                'type': 'welcome',
                'title': '🚀 Welcome to Project Omega v4.0!',
                'message': 'The complete security learning platform. Type "tutorial start welcome" to begin your journey.',
                'timestamp': datetime.now().isoformat(),
                'priority': 'high'
            })
            
            # If tutorial engine is available, send tutorial suggestion
            if TUTORIAL_AVAILABLE and self.tutorial_engine:
                # Check if first-time user
                if not self.tutorial_engine.tutorial_progress:
                    emit('tutorial_suggestion', {
                        'message': '🎯 New to Omega? Start with the welcome tutorial!',
                        'tutorial': 'welcome',
                        'action': 'Type: tutorial start welcome',
                        'timestamp': datetime.now().isoformat()
                    })
            
            print(f"[WEBSOCKET] Client connected: {client_id}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.clients -= 1
        
        @self.socketio.on('get_system_metrics')
        def handle_get_metrics():
            metrics = self.get_system_metrics()
            emit('system_metrics', metrics)
        
        @self.socketio.on('send_command')
        def handle_command(data):
            command = data.get('command', '').strip()
            response = self.process_command(command)
            
            emit('command_response', {
                'command': command,
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'type': 'success'
            })
            
            # Log command
            print(f"[COMMAND] {command} -> {response[:50]}...")
        
        # Tutorial WebSocket events (if tutorial API doesn't handle them)
        if TUTORIAL_AVAILABLE:
            @self.socketio.on('get_tutorial_info')
            def handle_tutorial_info():
                status = self.tutorial_engine.get_tutorial_status()
                emit('tutorial_info', status)
    
    def get_system_metrics(self):
        """Get system metrics with tutorial context"""
        metrics = {
            'cpu': random.randint(5, 25),  # Lower for tutorial mode
            'memory': random.randint(20, 50),
            'threat_level': random.randint(0, 15),  # Low threat in tutorial
            'mode': self.mode,
            'clients': self.clients,
            'timestamp': datetime.now().isoformat(),
            'environment': 'tutorial_safe',
            'system_status': 'Learning Mode'
        }
        
        # Add deception metrics if available
        if DECEPTION_AVAILABLE and hasattr(self, 'deception_engine'):
            stats = self.deception_engine.get_deception_stats()
            metrics['deception'] = {
                'active': stats['active'],
                'honeypots': stats['honeypots_active'],
                'connections': stats['total_connections']
            }
        
        # Add response metrics if available
        if RESPONSE_AVAILABLE and hasattr(self, 'response_engine'):
            stats = self.response_engine.get_response_stats()
            metrics['response'] = {
                'active': stats['active'],
                'level': stats['level'],
                'blocked_ips': stats['blocked_ips']
            }
        
        # Add tutorial metrics if available
        if TUTORIAL_AVAILABLE and hasattr(self, 'tutorial_engine'):
            status = self.tutorial_engine.get_tutorial_status()
            metrics['tutorial'] = {
                'active': status['active'],
                'current': status['current_tutorial'],
                'sandbox': status['sandbox_mode'],
                'user_level': status['user_level']
            }
        
        return metrics
    
    def process_command(self, command):
        """Process commands - tutorial integration handles this"""
        # The tutorial_integration has replaced this method
        # We need to ensure it exists
        if hasattr(self, '_original_process_command'):
            return self._original_process_command(command)
        
        # Fallback
        if not command:
            return "Please enter a command. Type 'help' for assistance."
        
        return f"Command: '{command}' - Type 'tutorial start welcome' to begin learning."
    
    def start_background_threads(self):
        """Start background threads for metrics and updates"""
        def metrics_loop():
            while True:
                time.sleep(3)
                metrics = self.get_system_metrics()
                self.socketio.emit('system_metrics', metrics)
                
                # Send tutorial reminders if no activity
                if TUTORIAL_AVAILABLE and hasattr(self, 'tutorial_engine'):
                    if not self.tutorial_engine.tutorial_progress and random.random() < 0.1:
                        self.socketio.emit('tutorial_reminder', {
                            'message': '🎓 Ready to learn? Type "tutorial start welcome" to begin!',
                            'timestamp': datetime.now().isoformat()
                        })
        
        threading.Thread(target=metrics_loop, daemon=True).start()
        print("[THREADS] Background monitoring started")

def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("   🚀 PROJECT OMEGA v4.0 - TUTORIAL EDITION")
    print("="*70 + "\n")
    
    print("🎯 PHASE 2G: Interactive Learning & Safe Sandbox")
    print("   • 5 Progressive Tutorials")
    print("   • Safe Experimentation Environment")
    print("   • Achievement System")
    print("   • Real-world Training Scenarios")
    
    print("\n🌐 Starting server on http://localhost:8081")
    print("💡 Type 'tutorial start welcome' to begin!")
    print("="*70 + "\n")
    
    server = OmegaServer()
    server.socketio.run(server.app, host='0.0.0.0', port=8082, debug=False, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()

