"""
from typing import List, Dict, Any
Working adapter for deception engine integration
This bridges the new module system with the legacy deception engine
"""

import sys
import os
import importlib.util
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class WorkingDeceptionAdapter:
    """Adapter that actually works with the deception engine"""
    
    def __init__(self, config: Dict[str, Any], engine=None):
        self.config = config
        self.engine = engine
        self.honeypots = []
        self.running = False
        self.legacy_module = None
        self._load_legacy_engine()
    
    def _load_legacy_engine(self):
        """Load the legacy deception engine"""
        try:
            legacy_path = os.path.join(os.path.dirname(__file__), 'legacy')
            
            # Add to Python path
            if legacy_path not in sys.path:
                sys.path.insert(0, legacy_path)
            
            # Check what's available
            python_files = []
            for root, dirs, files in os.walk(legacy_path):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        python_files.append(os.path.join(root, file))
            
            logger.info(f"Found {len(python_files)} Python files in legacy deception")
            
            if python_files:
                # Try to import the main deception module
                try:
                    # First, check for deception_api
                    api_path = os.path.join(legacy_path, 'deception_api.py')
                    if os.path.exists(api_path):
                        spec = importlib.util.spec_from_file_location("deception_api", api_path)
                        if spec and spec.loader:
                            self.legacy_module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(self.legacy_module)
                            logger.info("Loaded deception_api module")
                            
                            # Initialize if there's an init function
                            if hasattr(self.legacy_module, 'initialize'):
                                self.legacy_module.initialize(self.config)
                                logger.info("Initialized deception engine")
                    else:
                        logger.warning("deception_api.py not found in legacy directory")
                        
                except Exception as e:
                    logger.error(f"Failed to load deception_api: {e}")
            
            # If no module loaded, create a mock for development
            if not self.legacy_module:
                logger.warning("Creating mock deception engine for development")
                self.legacy_module = self._create_mock_engine()
                
        except Exception as e:
            logger.error(f"Failed to load legacy deception engine: {e}")
            self.legacy_module = self._create_mock_engine()
    
    def _create_mock_engine(self):
        """Create a mock deception engine for development"""
        class MockDeceptionEngine:
            def __init__(self):
                self.honeypots = []
                self.logs = []
                self.config = {}
            
            def initialize(self, config):
                self.config = config
                # Create mock honeypots based on config
                honeypot_configs = config.get('honeypots', [])
                for hp_config in honeypot_configs:
                    self.honeypots.append({
                        'id': hp_config.get('name', 'unknown').lower().replace(' ', '_'),
                        'name': hp_config.get('name', 'Unnamed Honeypot'),
                        'type': hp_config.get('type', 'unknown'),
                        'port': hp_config.get('port', 0),
                        'running': True,
                        'config': hp_config,
                    })
                return True
            
            def get_honeypots(self):
                return self.honeypots
            
            def log_interaction(self, honeypot_id, interaction_data):
                log_entry = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'honeypot_id': honeypot_id,
                    'data': interaction_data,
                    'detected': True,  # Mock detection
                }
                self.logs.append(log_entry)
                return log_entry
            
            def simulate_attack(self, honeypot_id, attack_type, params):
                """Simulate an attack against a honeypot"""
                honeypot = next((hp for hp in self.honeypots if hp['id'] == honeypot_id), None)
                if not honeypot:
                    return {'success': False, 'error': 'Honeypot not found'}
                
                # Simulate different attack types
                import random
                import time
                
                time.sleep(0.5)  # Simulate processing time
                
                result = {
                    'success': random.random() > 0.3,  # 70% success rate
                    'honeypot_id': honeypot_id,
                    'honeypot_name': honeypot['name'],
                    'attack_type': attack_type,
                    'timestamp': datetime.utcnow().isoformat(),
                }
                
                # Type-specific results
                if attack_type == 'port_scan':
                    result['ports_found'] = [honeypot['port'], 80, 443, 8080]
                    result['services'] = [honeypot['type'], 'http', 'https']
                elif attack_type == 'brute_force':
                    result['attempts'] = params.get('attempts', 100)
                    result['credentials_found'] = ['admin:password123'] if random.random() > 0.8 else []
                elif attack_type == 'exploit':
                    result['vulnerability'] = 'CVE-2023-12345'
                    result['payload_delivered'] = True
                
                # Log the interaction
                self.log_interaction(honeypot_id, {
                    'attack_type': attack_type,
                    'result': result,
                    'simulation': True,
                })
                
                return result
        
        return MockDeceptionEngine()
    
    def start(self):
        """Start the deception adapter"""
        logger.info("Starting Working Deception Adapter...")
        
        if self.legacy_module:
            try:
                # Initialize if not already
                if hasattr(self.legacy_module, 'initialize'):
                    self.legacy_module.initialize(self.config)
                
                # Get honeypots
                if hasattr(self.legacy_module, 'get_honeypots'):
                    self.honeypots = self.legacy_module.get_honeypots()
                    logger.info(f"Loaded {len(self.honeypots)} honeypots")
                else:
                    # Create from config
                    honeypot_configs = self.config.get('honeypots', [])
                    self.honeypots = []
                    for hp_config in honeypot_configs:
                        self.honeypots.append({
                            'id': hp_config.get('name', 'unknown').lower().replace(' ', '_'),
                            'name': hp_config.get('name', 'Unnamed Honeypot'),
                            'type': hp_config.get('type', 'unknown'),
                            'port': hp_config.get('port', 0),
                            'running': True,
                            'config': hp_config,
                        })
                    logger.info(f"Created {len(self.honeypots)} honeypots from config")
            
            except Exception as e:
                logger.error(f"Failed to initialize deception engine: {e}")
                # Create mock honeypots
                self._create_mock_honeypots()
        
        self.running = True
        logger.info("Working Deception Adapter started")
        return True
    
    def _create_mock_honeypots(self):
        """Create mock honeypots if real ones fail"""
        default_honeypots = [
            {
                'id': 'ssh_honeypot',
                'name': 'SSH Honeypot',
                'type': 'ssh',
                'port': 2222,
                'running': True,
                'config': {'banner': 'SSH-2.0-OpenSSH_7.9p1'},
            },
            {
                'id': 'http_honeypot',
                'name': 'Web Honeypot',
                'type': 'http',
                'port': 8081,
                'running': True,
                'config': {'template': 'default_website'},
            },
            {
                'id': 'mysql_honeypot',
                'name': 'MySQL Honeypot',
                'type': 'mysql',
                'port': 3306,
                'running': True,
                'config': {'version': '5.7.0'},
            },
        ]
        
        # Merge with config
        config_honeypots = self.config.get('honeypots', [])
        for hp_config in config_honeypots:
            hp_id = hp_config.get('name', 'unknown').lower().replace(' ', '_')
            if not any(hp['id'] == hp_id for hp in default_honeypots):
                default_honeypots.append({
                    'id': hp_id,
                    'name': hp_config.get('name', 'Unnamed Honeypot'),
                    'type': hp_config.get('type', 'unknown'),
                    'port': hp_config.get('port', 0),
                    'running': True,
                    'config': hp_config,
                })
        
        self.honeypots = default_honeypots
    
    def stop(self):
        """Stop the deception adapter"""
        logger.info("Stopping Working Deception Adapter...")
        self.running = False
        logger.info("Working Deception Adapter stopped")
    
    def get_honeypots(self) -> List[Dict[str, Any]]:
        """Get all available honeypots"""
        return self.honeypots
    
    def attack_honeypot(self, honeypot_id: str, attack_type: str, 
                        parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute an attack against a honeypot"""
        if not self.running:
            return {'success': False, 'error': 'Adapter not running'}
        
        parameters = parameters or {}
        
        # Find the honeypot
        honeypot = next((hp for hp in self.honeypots if hp['id'] == honeypot_id), None)
        if not honeypot:
            return {'success': False, 'error': f'Honeypot not found: {honeypot_id}'}
        
        logger.info(f"Attacking honeypot {honeypot['name']} with {attack_type}")
        
        # Use legacy engine if available
        if self.legacy_module and hasattr(self.legacy_module, 'simulate_attack'):
            try:
                result = self.legacy_module.simulate_attack(honeypot_id, attack_type, parameters)
            except Exception as e:
                logger.error(f"Legacy simulate_attack failed: {e}")
                result = self._simulate_attack(honeypot, attack_type, parameters)
        else:
            result = self._simulate_attack(honeypot, attack_type, parameters)
        
        # Log the interaction
        self._log_attack(honeypot, attack_type, result)
        
        # Notify engine if available
        if self.engine:
            self._notify_engine(honeypot, attack_type, result)
        
        return result
    
    def _simulate_attack(self, honeypot: Dict[str, Any], attack_type: str,
                        parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate an attack (used if legacy engine doesn't have the method)"""
        import random
        import time
        
        time.sleep(0.3)  # Simulate processing
        
        result = {
            'success': random.random() > 0.3,  # 70% success rate
            'honeypot_id': honeypot['id'],
            'honeypot_name': honeypot['name'],
            'attack_type': attack_type,
            'timestamp': datetime.utcnow().isoformat(),
            'parameters': parameters,
        }
        
        # Add type-specific details
        if attack_type == 'port_scan':
            result['ports_found'] = [honeypot['port'], 80, 443, 8080, 8443]
            result['services'] = [honeypot['type'], 'http', 'https', 'ssh', 'telnet']
            result['os_guess'] = 'Linux 4.15.0'
            
        elif attack_type == 'brute_force':
            attempts = parameters.get('attempts', 100)
            result['attempts'] = attempts
            result['credentials_found'] = []
            
            # Simulate finding credentials
            if random.random() > 0.7:  # 30% chance
                common_creds = [
                    'admin:admin',
                    'root:password',
                    'user:123456',
                    'administrator:password123',
                ]
                result['credentials_found'] = [random.choice(common_creds)]
                
        elif attack_type == 'exploit':
            result['vulnerability'] = parameters.get('cve', 'CVE-2023-12345')
            result['payload_delivered'] = True
            result['shell_obtained'] = random.random() > 0.5
            
        elif attack_type == 'sql_injection':
            result['injection_successful'] = random.random() > 0.4
            if result['injection_successful']:
                result['data_extracted'] = [
                    'users table (25 records)',
                    'passwords table (25 records)',
                    'config settings',
                ]
                
        else:
            result['details'] = f"Simulated {attack_type} attack"
        
        return result
    
    def _log_attack(self, honeypot: Dict[str, Any], attack_type: str,
                   result: Dict[str, Any]):
        """Log the attack"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'honeypot_id': honeypot['id'],
            'honeypot_name': honeypot['name'],
            'attack_type': attack_type,
            'result': result,
            'detected': True,  # Honeypots always detect attacks
        }
        
        # Store in module logs
        if not hasattr(self, 'attack_logs'):
            self.attack_logs = []
        self.attack_logs.append(log_entry)
        
        logger.info(f"Attack logged: {attack_type} on {honeypot['name']} - "
                   f"Success: {result.get('success', False)}")
    
    def _notify_engine(self, honeypot: Dict[str, Any], attack_type: str,
                      result: Dict[str, Any]):
        """Notify the engine about the attack"""
        if self.engine and hasattr(self.engine, 'notify_modules'):
            try:
                self.engine.notify_modules('deception_attack', {
                    'honeypot': honeypot,
                    'attack_type': attack_type,
                    'result': result,
                    'timestamp': datetime.utcnow().isoformat(),
                })
            except Exception as e:
                logger.error(f"Failed to notify engine: {e}")
    
    def get_attack_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent attack logs"""
        if hasattr(self, 'attack_logs'):
            return self.attack_logs[-limit:] if self.attack_logs else []
        return []
    
    def status(self) -> Dict[str, Any]:
        """Get adapter status"""
        return {
            'running': self.running,
            'honeypots_count': len(self.honeypots),
            'legacy_engine_loaded': self.legacy_module is not None,
            'attack_logs_count': len(getattr(self, 'attack_logs', [])),
        }
