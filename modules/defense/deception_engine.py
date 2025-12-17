"""
DECEPTION ENGINE MODULE - Phase 2E
Project Omega - Active Defense Subsystem
"""

import json
import random
import socket
import threading
import time
import logging
from datetime import datetime
import subprocess
import os

class DeceptionEngine:
    def __init__(self, omega_server):
        self.server = omega_server
        self.active_honeypots = {}
        self.deception_log = []
        self.honeypot_counter = 0
        self.is_active = False
        self.deception_level = "LOW"
        
        # Honeypot templates
        self.honeypot_templates = {
            "fake_ssh": {
                "name": "Fake SSH Server",
                "port": 2222,
                "banner": "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1"
            },
            "fake_web": {
                "name": "Fake Web Admin Panel",
                "port": 8088,
                "template": "admin_panel.html"
            },
            "fake_db": {
                "name": "Fake MySQL Database",
                "port": 3307,
                "banner": "5.7.35 MySQL Community Server"
            }
        }
        
        self.attack_patterns = {}
        self.setup_logging()
        
    def setup_logging(self):
        """Setup deception logging"""
        os.makedirs('deception_engine/logs', exist_ok=True)
        self.logger = logging.getLogger('deception_engine')
        handler = logging.FileHandler('deception_engine/logs/deception.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def start_deception_mode(self, level="MEDIUM"):
        """Activate deception engine"""
        self.is_active = True
        self.deception_level = level
        self.logger.info(f"Deception Engine activated at {level} level")
        
        if level == "LOW":
            self.deploy_honeypot("fake_web")
        elif level == "MEDIUM":
            self.deploy_honeypot("fake_ssh")
            self.deploy_honeypot("fake_web")
        elif level == "HIGH":
            for honeypot in ["fake_ssh", "fake_web", "fake_db"]:
                self.deploy_honeypot(honeypot)
            
        self.server.socketio.emit('deception_update', {
            'status': 'active',
            'level': level,
            'honeypots': list(self.active_honeypots.keys())
        })
        
        return {"status": "success", "message": f"Deception Engine activated at {level} level"}
    
    def deploy_honeypot(self, honeypot_type):
        """Deploy a specific honeypot"""
        if honeypot_type not in self.honeypot_templates:
            return {"status": "error", "message": f"Unknown honeypot type: {honeypot_type}"}
        
        template = self.honeypot_templates[honeypot_type]
        honeypot_id = f"{honeypot_type}_{self.honeypot_counter}"
        self.honeypot_counter += 1
        
        thread = threading.Thread(
            target=self.run_honeypot,
            args=(honeypot_id, template),
            daemon=True
        )
        thread.start()
        
        self.active_honeypots[honeypot_id] = {
            'id': honeypot_id,
            'type': honeypot_type,
            'port': template['port'],
            'start_time': datetime.now().isoformat(),
            'connections': 0
        }
        
        self.logger.info(f"Deployed honeypot: {honeypot_id} on port {template['port']}")
        
        self.server.socketio.emit('honeypot_deployed', {
            'honeypot_id': honeypot_id,
            'type': honeypot_type,
            'port': template['port'],
            'name': template['name']
        })
        
        return {"status": "success", "honeypot_id": honeypot_id}
    
    def run_honeypot(self, honeypot_id, template):
        """Run the honeypot service"""
        port = template['port']
        
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(5)
            server_socket.settimeout(1)
            
            self.logger.info(f"Honeypot {honeypot_id} listening on port {port}")
            
            while self.is_active and honeypot_id in self.active_honeypots:
                try:
                    client_socket, client_address = server_socket.accept()
                    self.active_honeypots[honeypot_id]['connections'] += 1
                    client_ip = client_address[0]
                    
                    self.log_deception_event(
                        honeypot_id=honeypot_id,
                        event_type="CONNECTION_ATTEMPT",
                        source_ip=client_ip,
                        details=f"Connection to {template['name']} on port {port}",
                        severity="MEDIUM"
                    )
                    
                    if template.get('banner'):
                        client_socket.send(f"{template['banner']}\n".encode())
                    
                    client_socket.close()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    self.logger.error(f"Honeypot error: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Failed to start honeypot {honeypot_id}: {e}")
    
    def log_deception_event(self, honeypot_id, event_type, source_ip, details, severity):
        """Log deception events"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'honeypot_id': honeypot_id,
            'event_type': event_type,
            'source_ip': source_ip,
            'details': details,
            'severity': severity
        }
        
        self.deception_log.append(event)
        self.logger.info(f"Deception Event: {event_type} from {source_ip}")
        
        self.server.socketio.emit('deception_event', event)
        
        if severity in ["HIGH", "CRITICAL"]:
            self.trigger_threat_detection(event)
    
    def trigger_threat_detection(self, event):
        """Trigger threat detection"""
        threat_data = {
            'timestamp': event['timestamp'],
            'source': event['source_ip'],
            'type': 'DECEPTION_TRAP_TRIGGERED',
            'description': f"Honeypot triggered: {event['details']}",
            'confidence': 0.85,
            'severity': event['severity']
        }
        
        self.server.socketio.emit('threat_detected', threat_data)
    
    def get_deception_stats(self):
        """Get deception statistics"""
        total_connections = sum(hp['connections'] for hp in self.active_honeypots.values())
        
        return {
            'active': self.is_active,
            'level': self.deception_level,
            'honeypots_active': len(self.active_honeypots),
            'total_connections': total_connections,
            'unique_attackers': len(self.attack_patterns),
            'deception_events': len(self.deception_log)
        }
    
    def stop_deception_mode(self):
        """Deactivate all honeypots"""
        self.is_active = False
        self.active_honeypots.clear()
        self.logger.info("Deception Engine deactivated")
        
        self.server.socketio.emit('deception_update', {
            'status': 'inactive',
            'level': 'OFF',
            'honeypots': []
        })
        
        return {"status": "success", "message": "Deception Engine deactivated"}

