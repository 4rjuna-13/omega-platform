"""
Omega v4 with Phase 2G Integration
Fixed version with proper deception_api integration
"""

import asyncio
import json
import threading
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

from tutorial_engine import TutorialEngine
from tutorial_api import TutorialAPI
from tutorial_integration import TutorialIntegration

# PHASE 2G IMPORTS
try:
    from tutorial_system import TutorialSystem
    PHASE_2G_AVAILABLE = True
except ImportError:
    PHASE_2G_AVAILABLE = False

class OmegaV4WithPhase2G:
    def __init__(self):
        print("\n" + "="*60)
        print("🚀 OMEGA v4 WITH PHASE 2G INTEGRATION")
        print("="*60)
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'omega_secret_key_phase_2g'
        self.socketio = SocketIO(self.app, async_mode='eventlet', cors_allowed_origins="*")
        
        # Initialize core modules
        self.tutorial_engine = TutorialEngine()
        self.tutorial_api = TutorialAPI()
        self.tutorial_integration = TutorialIntegration()
        
        # Initialize Phase 2G if available
        if PHASE_2G_AVAILABLE:
            self.tutorial_system = TutorialSystem(self.tutorial_engine)
            print("✅ Phase 2G Tutorial System Initialized")
        
        print("✅ Omega v4 with Phase 2G Initialized")
        
        # Setup routes
        self.setup_routes()
        self.setup_socketio()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('war_room.html')
        
        @self.app.route('/api/status')
        def status():
            return jsonify({
                "status": "online",
                "version": "v4.0 with Phase 2G",
                "phase_2g": PHASE_2G_AVAILABLE,
                "features": [
                    "Tutorial System",
                    "Beginner Sandbox Mode" if PHASE_2G_AVAILABLE else None,
                    "First 15 Minutes Experience" if PHASE_2G_AVAILABLE else None,
                    "Deception Engine",
                    "Autonomous Response"
                ]
            })
        
        @self.app.route('/api/start_tutorial', methods=['POST'])
        def start_tutorial():
            data = request.json
            tutorial_id = data.get('tutorial_id', 'beginner_path')
            
            if tutorial_id == 'phase_2g_beginner' and PHASE_2G_AVAILABLE:
                # Launch Phase 2G beginner experience
                result = self.tutorial_system.launch_tutorial_mode()
                return jsonify({
                    "success": result,
                    "message": "Phase 2G Beginner Tutorial Started",
                    "tutorial": "first_15_minutes"
                })
            else:
                # Regular tutorial
                return jsonify({
                    "success": True,
                    "message": f"Tutorial {tutorial_id} started",
                    "tutorial": tutorial_id
                })
    
    def setup_socketio(self):
        """Setup SocketIO events"""
        
        @self.socketio.on('connect')
        def handle_connect():
            print(f"Client connected: {request.sid}")
            emit('welcome', {
                'message': 'Welcome to Omega v4 with Phase 2G',
                'phase_2g': PHASE_2G_AVAILABLE
            })
        
        @self.socketio.on('start_phase_2g')
        def handle_start_phase_2g():
            if PHASE_2G_AVAILABLE:
                emit('phase_2g_status', {'status': 'starting'})
                # Run in background thread
                threading.Thread(target=self.tutorial_system.launch_tutorial_mode).start()
                emit('phase_2g_status', {'status': 'started'})
            else:
                emit('phase_2g_status', {'status': 'unavailable'})
    
    def run(self, host='0.0.0.0', port=8081):
        """Run the Omega server"""
        print(f"\n🌐 Starting Omega v4 with Phase 2G on http://{host}:{port}")
        print("💡 Access the beginner tutorial at: http://localhost:8081")
        
        if PHASE_2G_AVAILABLE:
            print("\n🎯 PHASE 2G FEATURES AVAILABLE:")
            print("   • First 15 Minutes Experience")
            print("   • Safe Sandbox Mode")
            print("   • Beginner Learning Path")
            print("   • Marketing Metrics Tracking")
        
        self.socketio.run(self.app, host=host, port=port, debug=True)

def main():
    """Main entry point"""
    omega = OmegaV4WithPhase2G()
    omega.run()

if __name__ == "__main__":
    main()
