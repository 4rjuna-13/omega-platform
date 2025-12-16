"""
AUTONOMOUS RESPONSE ENGINE - Phase 2F
Project Omega - Automated Threat Containment
"""

import json
import threading
import time
import logging
from datetime import datetime
import os
import random

class AutonomousResponse:
    def __init__(self, omega_server):
        self.server = omega_server
        self.is_active = False
        self.response_level = "MODERATE"
        self.response_log = []
        self.response_counter = 0
        self.blocked_ips = set()
        
        self.setup_logging()
        print("[RESPONSE] Autonomous Response Engine initialized")
        
    def setup_logging(self):
        """Setup response logging"""
        os.makedirs('autonomous_response/logs', exist_ok=True)
        self.logger = logging.getLogger('autonomous_response')
        handler = logging.FileHandler('autonomous_response/logs/response.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def activate_response_mode(self, level="MODERATE"):
        """Activate autonomous response system"""
        self.is_active = True
        self.response_level = level
        self.logger.info(f"Autonomous Response activated at {level} level")
        
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('response_update', {
                'status': 'active',
                'level': level,
                'message': '🤖 Autonomous Response ACTIVATED',
                'timestamp': datetime.now().isoformat()
            })
        
        return {"status": "success", "message": f"Autonomous Response activated at {level} level"}
    
    def deactivate_response_mode(self):
        """Deactivate response system"""
        self.is_active = False
        self.logger.info("Autonomous Response deactivated")
        
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('response_update', {
                'status': 'inactive',
                'level': 'OFF',
                'message': 'Autonomous Response DEACTIVATED',
                'timestamp': datetime.now().isoformat()
            })
        
        return {"status": "success", "message": "Autonomous Response deactivated"}
    
    def handle_threat(self, threat_data):
        """Handle incoming threat"""
        if not self.is_active:
            return {"status": "inactive", "message": "Response system not active"}
        
        threat_type = threat_data.get('event_type', 'UNKNOWN')
        source_ip = threat_data.get('source_ip', '0.0.0.0')
        
        # Create response
        response = self.create_response(threat_type, source_ip, threat_data)
        
        # Execute response
        result = self.execute_response(response)
        
        # Log everything
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'threat': threat_data,
            'response': response,
            'result': result
        }
        self.response_log.append(log_entry)
        
        # Send to WebSocket
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('threat_response', {
                'threat': threat_data,
                'response': response,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
        
        return result
    
    def create_response(self, threat_type, source_ip, threat_data):
        """Create appropriate response based on threat"""
        response_id = f"resp_{self.response_counter}_{int(time.time())}"
        self.response_counter += 1
        
        # Determine actions based on threat type and response level
        actions = []
        
        if threat_type in ["SSH_AUTH_ATTEMPT", "BRUTEFORCE", "DECEPTION_TRAP"]:
            actions.append("BLOCK_IP")
            actions.append("ALERT_ADMIN")
        elif threat_type in ["MALWARE", "DATA_EXFIL"]:
            actions.append("ISOLATE_NETWORK")
            actions.append("BACKUP_DATA")
            actions.append("ALERT_ADMIN")
        elif threat_type in ["SCANNING", "WEB_REQUEST", "CONNECTION_ATTEMPT"]:
            if self.response_level == "AGGRESSIVE":
                actions.append("BLOCK_IP")
            actions.append("ALERT_ADMIN")
            actions.append("INCREASE_MONITORING")
        else:
            actions.append("ALERT_ADMIN")
        
        # Adjust based on response level
        if self.response_level == "CONSERVATIVE":
            actions = [a for a in actions if a != "BLOCK_IP" and a != "ISOLATE_NETWORK"]
        elif self.response_level == "AGGRESSIVE" and "BLOCK_IP" not in actions:
            actions.append("BLOCK_IP")
        
        return {
            'response_id': response_id,
            'threat_type': threat_type,
            'source_ip': source_ip,
            'actions': actions,
            'response_level': self.response_level,
            'timestamp': datetime.now().isoformat(),
            'status': 'CREATED'
        }
    
    def execute_response(self, response):
        """Execute the response actions"""
        results = []
        
        for action in response['actions']:
            if action == "BLOCK_IP":
                result = self.block_ip(response['source_ip'])
            elif action == "ALERT_ADMIN":
                result = self.alert_admin(response)
            elif action == "ISOLATE_NETWORK":
                result = self.isolate_network(response['source_ip'])
            elif action == "BACKUP_DATA":
                result = self.initiate_backup()
            elif action == "INCREASE_MONITORING":
                result = self.increase_monitoring()
            else:
                result = {"action": action, "status": "unknown"}
            
            results.append(result)
            
            # Send action update
            if hasattr(self.server, 'socketio'):
                self.server.socketio.emit('response_action', {
                    'response_id': response['response_id'],
                    'action': action,
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                })
        
        response['results'] = results
        response['status'] = 'EXECUTED'
        response['completion_time'] = datetime.now().isoformat()
        
        return response
    
    def block_ip(self, ip_address):
        """Block an IP address"""
        if ip_address in self.blocked_ips:
            return {"action": "BLOCK_IP", "status": "already_blocked", "ip": ip_address}
        
        self.blocked_ips.add(ip_address)
        self.logger.info(f"Blocked IP: {ip_address}")
        
        # In real system: iptables -A INPUT -s {ip} -j DROP
        command = f"iptables -A INPUT -s {ip_address} -j DROP"
        
        return {
            "action": "BLOCK_IP",
            "status": "success",
            "ip": ip_address,
            "message": f"IP {ip_address} added to block list",
            "command": command
        }
    
    def alert_admin(self, response):
        """Send alert to administrator"""
        alert_msg = f"🚨 Response Alert: {response['threat_type']} from {response['source_ip']}"
        
        self.logger.warning(alert_msg)
        
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('admin_alert', {
                'type': 'response_alert',
                'message': alert_msg,
                'threat': response['threat_type'],
                'source': response['source_ip'],
                'timestamp': datetime.now().isoformat()
            })
        
        return {
            "action": "ALERT_ADMIN",
            "status": "success",
            "message": alert_msg
        }
    
    def isolate_network(self, ip_address):
        """Isolate network segment"""
        segment = "192.168.1.0/24"  # Simplified
        self.logger.info(f"Isolated network segment: {segment}")
        
        return {
            "action": "ISOLATE_NETWORK",
            "status": "success",
            "segment": segment,
            "message": f"Isolated network segment {segment}"
        }
    
    def initiate_backup(self):
        """Initiate data backup"""
        backup_id = f"backup_{int(time.time())}"
        self.logger.info(f"Initiated backup: {backup_id}")
        
        # Simulate backup in background
        threading.Thread(target=self.simulate_backup, args=(backup_id,), daemon=True).start()
        
        return {
            "action": "BACKUP_DATA",
            "status": "started",
            "backup_id": backup_id,
            "message": "Critical data backup initiated"
        }
    
    def simulate_backup(self, backup_id):
        """Simulate backup process"""
        time.sleep(2)
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('backup_complete', {
                'backup_id': backup_id,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            })
    
    def increase_monitoring(self):
        """Increase monitoring levels"""
        self.logger.info("Increased monitoring levels")
        return {
            "action": "INCREASE_MONITORING",
            "status": "success",
            "message": "Monitoring levels increased"
        }
    
    def get_response_stats(self):
        """Get response system statistics"""
        return {
            'active': self.is_active,
            'level': self.response_level,
            'total_responses': len(self.response_log),
            'blocked_ips': len(self.blocked_ips),
            'last_response': self.response_log[-1]['timestamp'] if self.response_log else 'Never'
        }
    
    def get_response_log(self, limit=10):
        """Get recent response logs"""
        return self.response_log[-limit:] if self.response_log else []
    
    def test_response(self):
        """Test the response system"""
        test_threat = {
            'event_type': 'TEST_THREAT',
            'source_ip': '192.168.1.100',
            'severity': 'HIGH'
        }
        return self.handle_threat(test_threat)

