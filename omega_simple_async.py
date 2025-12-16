#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA - SIMPLE ASYNC COMMAND CENTER
Uses Threading instead of Eventlet for maximum compatibility
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

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.urandom(24)
# Use threading instead of eventlet for better compatibility
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables
system_status = {
    "mode": "SIMPLE",
    "security_level": "MONITOR",
    "websocket_connected": False,
    "modules_loaded": 2,
    "total_modules": 4,
    "threat_score": 0.0,
    "cpu_usage": 0.0,
    "memory_usage": 0.0,
    "network_traffic": 0.0,
    "last_update": datetime.now().isoformat()
}

class SimpleThreatPredictor:
    """Simplified threat prediction without complex dependencies"""
    def __init__(self):
        self.model_loaded = False
        try:
            if os.path.exists('threat_model.pkl'):
                with open('threat_model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                self.model_loaded = True
                logging.info("[THREAT] Model loaded successfully")
        except:
            logging.info("[THREAT] Running in simulation mode")
    
    def predict(self):
        """Simple threat prediction"""
        if self.model_loaded:
            try:
                features = [random.random() for _ in range(11)]
                features_array = np.array(features).reshape(1, -1)
                anomaly_score = self.model.decision_function(features_array)[0]
                return min(max((anomaly_score + 0.5) * 100, 0), 100)
            except:
                pass
        return random.uniform(10.0, 40.0)

class SimpleVoiceModule:
    """Simplified voice module"""
    def __init__(self):
        self.tts_available = False
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_available = True
            logging.info("[VOICE] TTS initialized")
        except:
            logging.info("[VOICE] TTS not available")
    
    def speak(self, text):
        if self.tts_available:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            except:
                pass
        return False

# Initialize modules
threat_predictor = SimpleThreatPredictor()
voice_module = SimpleVoiceModule()

def simulate_metrics():
    """Generate system metrics"""
    return {
        "cpu": round(random.uniform(5.0, 45.0), 1),
        "memory": round(random.uniform(30.0, 80.0), 1),
        "network": round(random.uniform(1.0, 50.0), 2),
        "threat": round(threat_predictor.predict(), 1)
    }

def metrics_thread():
    """Background thread for real-time updates"""
    while True:
        try:
            metrics = simulate_metrics()
            system_status.update({
                "cpu_usage": metrics["cpu"],
                "memory_usage": metrics["memory"],
                "network_traffic": metrics["network"],
                "threat_score": metrics["threat"],
                "last_update": datetime.now().isoformat()
            })
            
            socketio.emit('metrics_update', {
                'metrics': metrics,
                'status': system_status
            })
            
            time.sleep(2)
        except Exception as e:
            logging.error(f"Metrics error: {e}")
            time.sleep(5)

@app.route('/')
def index():
    session['session_id'] = f"omega_{int(time.time())}"
    return render_template('simple_command_center.html')

@app.route('/api/status')
def api_status():
    return jsonify(system_status)

@app.route('/api/switch_mode', methods=['POST'])
def switch_mode():
    data = request.get_json()
    mode = data.get('mode', 'SIMPLE')
    
    if mode in ['SIMPLE', 'ADVANCED']:
        system_status['mode'] = mode
        socketio.emit('mode_change', {'mode': mode})
        return jsonify({'success': True, 'mode': mode})
    
    return jsonify({'success': False, 'error': 'Invalid mode'}), 400

@socketio.on('connect')
def handle_connect():
    logging.info(f"[WEBSOCKET] Client connected")
    system_status['websocket_connected'] = True
    emit('connection_ack', {
        'message': 'Connected to Omega Command Center',
        'status': system_status
    })

@socketio.on('disconnect')
def handle_disconnect():
    logging.info(f"[WEBSOCKET] Client disconnected")
    system_status['websocket_connected'] = False

@socketio.on('command')
def handle_command(data):
    command = data.get('command', '').lower()
    logging.info(f"[COMMAND] {command}")
    
    response = {"status": "unknown", "message": "Command not recognized"}
    
    if command in ['status', 'help']:
        response = {
            "status": "success",
            "message": "Omega Command Center v2.0 (Threading Mode)",
            "mode": system_status['mode']
        }
    elif command == 'voice':
        text = data.get('text', 'Omega system operational')
        if voice_module.speak(text):
            response = {"status": "success", "message": f"Spoke: {text}"}
        else:
            response = {"status": "info", "message": "TTS not available"}
    elif command == 'threat':
        response = {
            "status": "success",
            "message": f"Threat level: {system_status['threat_score']:.1f}",
            "threat_score": system_status['threat_score']
        }
    
    emit('command_response', response)

def main():
    # Start background thread
    threading.Thread(target=metrics_thread, daemon=True).start()
    
    print("=" * 70)
    print("   PROJECT OMEGA - SIMPLE THREADING MODE")
    print("   Port 8081 • Maximum Compatibility • No Eventlet Issues")
    print("=" * 70)
    print("\n📊 SYSTEM READY:")
    print(f"   • WebSocket: Threading mode")
    print(f"   • Interface: {system_status['mode']}")
    print(f"   • Threat Model: {'Loaded' if threat_predictor.model_loaded else 'Simulation'}")
    print(f"   • Voice: {'Available' if voice_module.tts_available else 'Not available'}")
    
    print("\n🌐 ACCESS: http://localhost:8081")
    print("\n" + "=" * 70)
    
    # Start server
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, use_reloader=False)

if __name__ == '__main__':
    main()
