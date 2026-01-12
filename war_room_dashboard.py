#!/usr/bin/env python3
"""
Project Omega - War Room Dashboard
Phase 2D: Real-time Security Visualization Interface
"""

import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

class WarRoomDashboard:
    """Web-based dashboard for real-time security monitoring"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'omega_secret_key_2025'
        self.socketio = SocketIO(self.app, async_mode='eventlet', cors_allowed_origins="*")
        
        # Dashboard data
        self.threat_events = []
        self.active_nodes = []
        self.security_level = "MONITOR"
        self.metrics = {
            'threats_blocked': 0,
            'scans_completed': 0,
            'anomalies_detected': 0,
            'active_connections': 0,
            'predictive_accuracy': 52.8  # From your ML model
        }
        
        # Setup routes
        self.setup_routes()
        self.setup_socket_events()
        print("[WAR ROOM] Dashboard initialized")
        
    def setup_routes(self):
        """Setup Flask routes"""
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/status')
        def get_status():
            return jsonify({
                'status': 'operational',
                'security_level': self.security_level,
                'timestamp': datetime.now().isoformat(),
                'metrics': self.metrics,
                'active_threats': len([e for e in self.threat_events if e.get('severity') == 'high']),
                'version': 'Omega 2.0'
            })
        
        @self.app.route('/api/threats')
        def get_threats():
            return jsonify(self.threat_events[-20:])  # Last 20 events
        
        @self.app.route('/api/nodes')
        def get_nodes():
            return jsonify(self.active_nodes)
        
        @self.app.route('/api/omega/command', methods=['POST'])
        def send_command():
            data = request.json
            command = data.get('command', '')
            
            response = {
                'command': command,
                'status': 'executed',
                'timestamp': datetime.now().isoformat(),
                'result': f"War Room processed: {command}"
            }
            
            # Broadcast to connected clients
            self.socketio.emit('command_response', response)
            return jsonify(response)
    
    def setup_socket_events(self):
        """Setup SocketIO event handlers"""
        @self.socketio.on('connect')
        def handle_connect():
            print(f"[WAR ROOM] Client connected")
            emit('connected', {'message': 'Connected to Omega War Room', 'time': datetime.now().isoformat()})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print(f"[WAR ROOM] Client disconnected")
        
        @self.socketio.on('request_update')
        def handle_update_request():
            emit('dashboard_update', {
                'metrics': self.metrics,
                'threat_count': len(self.threat_events),
                'timestamp': datetime.now().isoformat(),
                'security_level': self.security_level
            })
        
        @self.socketio.on('send_command')
        def handle_client_command(data):
            print(f"[WAR ROOM] Received command: {data}")
            emit('command_result', {
                'command': data,
                'result': 'Processed by Omega Intelligence',
                'timestamp': datetime.now().isoformat()
            })
    
    def add_threat_event(self, event_data):
        """Add a threat event to the dashboard"""
        event = {
            'id': len(self.threat_events) + 1,
            'timestamp': datetime.now().isoformat(),
            'type': event_data.get('type', 'unknown'),
            'severity': event_data.get('severity', 'medium'),
            'source': event_data.get('source', 'unknown'),
            'description': event_data.get('description', ''),
            'threat_score': event_data.get('threat_score', 0)
        }
        
        self.threat_events.append(event)
        
        # Update metrics
        if event['severity'] == 'high':
            self.metrics['threats_blocked'] += 1
        self.metrics['anomalies_detected'] += 1
        
        # Broadcast to connected clients
        self.socketio.emit('new_threat', event)
        
        # Keep only last 100 events
        if len(self.threat_events) > 100:
            self.threat_events = self.threat_events[-100:]
            
        return event
    
    def update_metrics(self, metric_updates):
        """Update dashboard metrics"""
        for key, value in metric_updates.items():
            if key in self.metrics:
                self.metrics[key] += value
        
        # Broadcast update
        self.socketio.emit('metrics_update', self.metrics)
    
    def generate_sample_data(self):
        """Generate sample data for testing"""
        import random
        
        print("[WAR ROOM] Generating sample threat data...")
        
        threat_types = ['port_scan', 'brute_force', 'malware', 'data_exfil', 'dos_attempt', 'phishing']
        sources = ['192.168.1.105', '10.0.0.22', 'external_probe', 'suspicious_domain']
        descriptions = [
            'Multiple SSH login attempts',
            'Unusual port scanning pattern',
            'Data exfiltration detected',
            'Predictive model flagged anomaly',
            'Possible brute force attack'
        ]
        
        for i in range(15):
            event = {
                'type': random.choice(threat_types),
                'severity': random.choice(['low', 'medium', 'high']),
                'source': random.choice(sources),
                'description': f"{random.choice(descriptions)} #{i+1}",
                'threat_score': random.randint(25, 92)
            }
            self.add_threat_event(event)
        
        # Add active nodes (from your Project Omega)
        self.active_nodes = [
            {'id': 'node_001', 'name': 'Omega Command Center', 'status': 'online', 'type': 'linux', 'ip': 'localhost'},
            {'id': 'node_002', 'name': 'Predictive Threat Model', 'status': 'online', 'type': 'ml', 'accuracy': '52.8%'},
            {'id': 'node_003', 'name': 'Voice Interface', 'status': 'online', 'type': 'audio', 'mode': 'active'},
            {'id': 'node_004', 'name': 'Security Scanner', 'status': 'standby', 'type': 'scan', 'last_scan': '5m ago'}
        ]
        
        # Set initial metrics
        self.metrics = {
            'threats_blocked': 8,
            'scans_completed': 127,
            'anomalies_detected': 42,
            'active_connections': 4,
            'predictive_accuracy': 52.8
        }
        
        print("[WAR ROOM] Sample data generated")
    
    def integrate_with_omega(self):
        """Connect with existing Omega components"""
        try:
            # Try to import and connect with predictive threat model
            from predictive_threat import ThreatPredictor
            self.predictor = ThreatPredictor()
            if self.predictor.load_model():
                print("[WAR ROOM] Connected to Threat Predictor")
                self.metrics['predictive_accuracy'] = 52.8  # From your earlier output
            else:
                print("[WAR ROOM] Threat Predictor not trained yet")
        except ImportError:
            print("[WAR ROOM] Predictive threat module not available")
        
        # Add a sample integration event
        self.add_threat_event({
            'type': 'system_integration',
            'severity': 'low',
            'source': 'war_room',
            'description': 'War Room dashboard integrated with Project Omega',
            'threat_score': 0
        })
    
    def run(self, host='0.0.0.0', port=8080):
        """Run the dashboard server"""
        print(f"\n{'='*60}")
        print("   PROJECT OMEGA - WAR ROOM DASHBOARD")
        print("           Phase 2D: Real-time Visualization")
        print(f"{'='*60}\n")
        
        # Generate sample data
        self.generate_sample_data()
        
        # Try to integrate with Omega
        self.integrate_with_omega()
        
        print(f"[WAR ROOM] Starting dashboard server...")
        print(f"[WAR ROOM] 🌐 Web Interface: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
        print(f"[WAR ROOM] 📊 API Status: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/api/status")
        print(f"[WAR ROOM] 🎯 Real-time WebSocket: ws://{host if host != '0.0.0.0' else 'localhost'}:{port}")
        print(f"[WAR ROOM] Press Ctrl+C to stop\n")
        
        # Run the server
        try:
            self.socketio.run(self.app, host=host, port=port, debug=False, use_reloader=False, log_output=False)
        except KeyboardInterrupt:
            print("\n[WAR ROOM] Dashboard stopped")
        except Exception as e:
            print(f"[WAR ROOM] Error: {e}")

def main():
    """Main entry point"""
    dashboard = WarRoomDashboard()
    dashboard.run(port=8080)

if __name__ == "__main__":
    main()
