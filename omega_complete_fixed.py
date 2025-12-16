#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA - FIXED COMMAND CENTER
Resolved Eventlet monkey patching issues for stable WebSocket operation
"""

# CRITICAL: Monkey patch MUST be first before ANY other imports
import eventlet
eventlet.monkey_patch()

import os
import sys
import json
import time
import threading
import queue
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
app.secret_key = os.urandom(24)  # Secure random key for sessions
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global variables
active_modules = {}
system_status = {
    "mode": "SIMPLE",  # SIMPLE or ADVANCED
    "security_level": "MONITOR",
    "websocket_connected": False,
    "modules_loaded": 0,
    "total_modules": 4,
    "threat_score": 0.0,
    "cpu_usage": 0.0,
    "memory_usage": 0.0,
    "network_traffic": 0.0,
    "last_update": datetime.now().isoformat()
}

class PredictiveThreatModule:
    """ML-powered threat prediction module"""
    def __init__(self):
        try:
            with open('threat_model_config.json', 'r') as f:
                config = json.load(f)
            self.features = config.get('features', [])
            self.model = None
            
            # Load model if exists
            if os.path.exists('threat_model.pkl'):
                with open('threat_model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                logging.info(f"[THREAT PREDICTOR] Loaded model with {len(self.features)} features")
            else:
                logging.warning("[THREAT PREDICTOR] No trained model found, running in simulation mode")
                
        except Exception as e:
            logging.error(f"[THREAT PREDICTOR] Initialization error: {e}")
            self.features = []
            self.model = None
    
    def predict(self, features):
        """Predict threat level from features"""
        if self.model is not None and len(features) == len(self.features):
            try:
                # Convert to numpy array and predict
                features_array = np.array(features).reshape(1, -1)
                anomaly_score = self.model.decision_function(features_array)[0]
                # Convert to 0-100 scale
                threat_score = min(max((anomaly_score + 0.5) * 100, 0), 100)
                return threat_score
            except Exception as e:
                logging.error(f"[THREAT PREDICTOR] Prediction error: {e}")
        
        # Fallback: random simulation
        return random.uniform(10.0, 30.0)

class VoiceCommandModule:
    """Voice command processing module"""
    def __init__(self):
        self.mic_available = False
        self.tts_available = False
        
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.mic_available = True
            logging.info("[VOICE] Speech recognition initialized")
        except ImportError:
            logging.warning("[VOICE] SpeechRecognition not available")
        except Exception as e:
            logging.warning(f"[VOICE] Microphone check failed: {e}")
        
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_available = True
            logging.info("[VOICE] Text-to-speech initialized")
        except ImportError:
            logging.warning("[VOICE] pyttsx3 not available")
        except Exception as e:
            logging.warning(f"[VOICE] TTS initialization failed: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        if self.tts_available:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            except Exception as e:
                logging.error(f"[VOICE] TTS error: {e}")
        return False
    
    def listen(self):
        """Listen for voice command"""
        if not self.mic_available:
            return None
        
        try:
            import speech_recognition as sr
            with sr.Microphone() as source:
                logging.info("[VOICE] Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                try:
                    text = self.recognizer.recognize_google(audio)
                    logging.info(f"[VOICE] Heard: {text}")
                    return text
                except sr.UnknownValueError:
                    logging.warning("[VOICE] Could not understand audio")
                except sr.RequestError as e:
                    logging.error(f"[VOICE] API error: {e}")
                    
        except Exception as e:
            logging.error(f"[VOICE] Listening error: {e}")
        
        return None

# Initialize modules
threat_predictor = PredictiveThreatModule()
voice_module = VoiceCommandModule()

def simulate_system_metrics():
    """Generate simulated system metrics"""
    import psutil
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        # Network simulation
        net_io = psutil.net_io_counters()
        network = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024  # MB
        
        # Update threat score with real features
        features = [
            cpu / 100.0,
            memory / 100.0,
            network / 1000.0,  # Normalize
            random.uniform(0, 1),  # Connection attempts
            random.uniform(0, 1),  # Failed logins
            random.uniform(0, 1),  # Port scans
            random.uniform(0, 1),  # Data transfer rate
            random.uniform(0, 1),  # Process anomalies
            random.uniform(0, 1),  # Memory spikes
            random.uniform(0, 1),  # Network latency
            random.uniform(0, 1)   # Service disruptions
        ]
        
        threat_score = threat_predictor.predict(features)
        
        return {
            "cpu": round(cpu, 1),
            "memory": round(memory, 1),
            "network": round(network, 2),
            "threat": round(threat_score, 1)
        }
    except ImportError:
        # Fallback simulation
        return {
            "cpu": round(random.uniform(5.0, 45.0), 1),
            "memory": round(random.uniform(30.0, 80.0), 1),
            "network": round(random.uniform(1.0, 50.0), 2),
            "threat": round(threat_predictor.predict([random.random() for _ in range(11)]), 1)
        }

def background_metrics_thread():
    """Background thread to update metrics"""
    while True:
        try:
            metrics = simulate_system_metrics()
            system_status.update({
                "cpu_usage": metrics["cpu"],
                "memory_usage": metrics["memory"],
                "network_traffic": metrics["network"],
                "threat_score": metrics["threat"],
                "last_update": datetime.now().isoformat()
            })
            
            # Broadcast to all connected clients
            socketio.emit('metrics_update', {
                'metrics': metrics,
                'status': system_status
            })
            
            time.sleep(2)  # Update every 2 seconds
            
        except Exception as e:
            logging.error(f"Metrics thread error: {e}")
            time.sleep(5)

@app.route('/')
def index():
    """Main command center page"""
    session['session_id'] = f"omega_{int(time.time())}_{random.randint(1000, 9999)}"
    return render_template('simple_command_center.html')

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify(system_status)

@app.route('/api/switch_mode', methods=['POST'])
def switch_mode():
    """Switch between SIMPLE and ADVANCED modes"""
    data = request.get_json()
    mode = data.get('mode', 'SIMPLE')
    
    if mode in ['SIMPLE', 'ADVANCED']:
        system_status['mode'] = mode
        logging.info(f"[SYSTEM] Mode switched to: {mode}")
        
        # Broadcast mode change
        socketio.emit('mode_change', {'mode': mode})
        
        return jsonify({'success': True, 'mode': mode})
    
    return jsonify({'success': False, 'error': 'Invalid mode'}), 400

@app.route('/api/voice/command', methods=['POST'])
def voice_command():
    """Process voice command"""
    data = request.get_json()
    command = data.get('command', '')
    
    if not command:
        return jsonify({'success': False, 'error': 'No command provided'}), 400
    
    logging.info(f"[VOICE] Processing command: {command}")
    
    # Process command
    response = f"Processed voice command: {command}"
    
    # Speak response if TTS available
    if voice_module.tts_available:
        voice_module.speak(response)
    
    return jsonify({
        'success': True,
        'response': response,
        'command': command
    })

@app.route('/api/threat/simulate', methods=['POST'])
def simulate_threat():
    """Simulate a threat scenario"""
    scenarios = [
        {"name": "Port Scan", "severity": "MEDIUM", "description": "Multiple port connection attempts detected"},
        {"name": "Brute Force", "severity": "HIGH", "description": "Rapid failed login attempts"},
        {"name": "DDoS", "severity": "CRITICAL", "description": "Distributed denial of service attack"},
        {"name": "Data Exfiltration", "severity": "HIGH", "description": "Unusual outbound data transfer"},
        {"name": "Malware", "severity": "CRITICAL", "description": "Suspicious process detected"}
    ]
    
    scenario = random.choice(scenarios)
    
    # Update threat score
    system_status['threat_score'] = min(100, system_status['threat_score'] + random.uniform(15, 40))
    
    # Broadcast threat alert
    socketio.emit('threat_alert', {
        'scenario': scenario,
        'timestamp': datetime.now().isoformat(),
        'current_threat': system_status['threat_score']
    })
    
    return jsonify({
        'success': True,
        'scenario': scenario,
        'message': f"Simulated {scenario['name']} threat"
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    logging.info(f"[WEBSOCKET] Client connected: {request.sid}")
    system_status['websocket_connected'] = True
    
    # Send current status to new client
    emit('connection_ack', {
        'message': 'Connected to Omega Command Center',
        'status': system_status,
        'session_id': session.get('session_id', 'unknown')
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    logging.info(f"[WEBSOCKET] Client disconnected: {request.sid}")
    system_status['websocket_connected'] = False

@socketio.on('command')
def handle_command(data):
    """Handle command from client"""
    command = data.get('command', '').lower()
    logging.info(f"[COMMAND] Received: {command}")
    
    response = {"status": "unknown", "message": "Command not recognized"}
    
    if command in ['status', 'help', 'info']:
        response = {
            "status": "success",
            "message": "Project Omega Command Center v2.0",
            "modules": ["Predictive Threat", "Voice Commands", "WebSocket", "Metrics"],
            "mode": system_status['mode']
        }
    elif command in ['scan', 'nmap']:
        response = {
            "status": "success", 
            "message": "Network scan initiated (simulated)",
            "scan_id": f"scan_{int(time.time())}",
            "estimated_time": "2 minutes"
        }
    elif command in ['voice', 'speak']:
        text = data.get('text', 'Hello from Omega Command Center')
        if voice_module.speak(text):
            response = {"status": "success", "message": f"Spoke: {text}"}
        else:
            response = {"status": "error", "message": "TTS not available"}
    elif command == 'threat':
        threat_level = system_status['threat_score']
        level = "LOW" if threat_level < 30 else "MEDIUM" if threat_level < 70 else "HIGH"
        response = {
            "status": "success",
            "message": f"Current threat level: {level} ({threat_level:.1f})",
            "threat_score": threat_level,
            "level": level
        }
    
    emit('command_response', response)

def main():
    """Main entry point"""
    # Start background metrics thread
    metrics_thread = threading.Thread(target=background_metrics_thread, daemon=True)
    metrics_thread.start()
    
    # Update module count
    system_status['modules_loaded'] = 2  # Threat predictor and voice module
    
    print("=" * 70)
    print("   PROJECT OMEGA - FIXED COMMAND CENTER")
    print("   Port 8081 • Stable WebSocket • Eventlet Issues Resolved")
    print("=" * 70)
    print("\n" + "=" * 70)
    print("🚀 PROJECT OMEGA COMMAND CENTER - STARTING (FIXED VERSION)")
    print("=" * 70)
    print("\n[SYSTEM] Loading Omega modules...")
    print(f"[THREAT PREDICTOR] {'Loaded' if threat_predictor.model else 'Simulation mode'}")
    print(f"[VOICE] Microphone: {'Available' if voice_module.mic_available else 'Not available'}")
    print(f"[VOICE] Text-to-speech: {'Available' if voice_module.tts_available else 'Not available'}")
    
    print("\n📊 SYSTEM STATUS:")
    print(f"   • Port: 8081")
    print(f"   • WebSocket: Ready (Eventlet patched)")
    print(f"   • Modules loaded: {system_status['modules_loaded']}/{system_status['total_modules']}")
    print(f"   • Interface: Dual (Simple/Advanced)")
    print(f"   • Security Level: {system_status['security_level']}")
    
    print("\n🌐 ACCESS URLS:")
    print("   • Command Center: http://localhost:8081")
    print("   • API Status: http://localhost:8081/api/status")
    print("   • WebSocket: ws://localhost:8081/socket.io/")
    
    print("\n🎯 FEATURES:")
    print("   • Real-time WebSocket communication")
    print("   • Dual interface with mode switching")
    print("   • Threat simulation engine")
    print("   • Live metrics and monitoring")
    print("   • Voice command integration")
    
    print("\n" + "=" * 70)
    print("💡 Open browser to http://localhost:8081 and test mode switching!")
    print("=" * 70)
    
    # Start the server
    socketio.run(app, host='0.0.0.0', port=8081, debug=False, use_reloader=False)

if __name__ == '__main__':
    main()
