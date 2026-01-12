"""
from typing import List, Dict, Any
Deception Module - Advanced honeypots and deception techniques
Now with working legacy integration
"""

import logging
from omega_platform.modules import BaseModule
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DeceptionModule(BaseModule):
    """Deception engine module with working legacy support"""
    
    def __init__(self, config: Dict[str, Any], engine):
        super().__init__(config, engine)
        self.honeypots = []
        self.traps = []
        self.adapter = None
        
        # Initialize working adapter
        try:
            from .working_adapter import WorkingDeceptionAdapter
            self.adapter = WorkingDeceptionAdapter(config, engine)
            logger.info("Working deception adapter initialized")
        except Exception as e:
            logger.error(f"Failed to initialize working adapter: {e}")
            self.adapter = None
        
    def start(self):
        """Start the deception module"""
        logger.info("Starting Deception Module...")
        
        # Start adapter if available
        if self.adapter:
            try:
                self.adapter.start()
                self.honeypots = self.adapter.get_honeypots()
                logger.info(f"Adapter started with {len(self.honeypots)} honeypots")
            except Exception as e:
                logger.error(f"Failed to start adapter: {e}")
                self._create_default_honeypots()
        else:
            self._create_default_honeypots()
        
        self.running = True
        logger.info("Deception Module started")
        
        # Start monitoring
        self._start_monitoring()
    
    def _create_default_honeypots(self):
        """Create default honeypots if adapter fails"""
        default_configs = [
            {
                'name': 'ssh_honeypot',
                'type': 'ssh',
                'port': 2222,
                'banner': 'SSH-2.0-OpenSSH_7.9p1',
            },
            {
                'name': 'http_honeypot',
                'type': 'http',
                'port': 8081,
                'template': 'default_website',
            },
        ]
        
        # Merge with config
        config_honeypots = self.config.get('honeypots', [])
        all_configs = default_configs + [c for c in config_honeypots 
                                        if c not in default_configs]
        
        self.honeypots = []
        for hp_config in all_configs:
            self.honeypots.append({
                'id': hp_config.get('name', 'unknown').lower().replace(' ', '_'),
                'name': hp_config.get('name', 'Unnamed Honeypot'),
                'type': hp_config.get('type', 'unknown'),
                'port': hp_config.get('port', 0),
                'running': True,
                'config': hp_config,
            })
        
        logger.info(f"Created {len(self.honeypots)} default honeypots")
    
    def stop(self):
        """Stop the deception module"""
        logger.info("Stopping Deception Module...")
        
        # Stop adapter if running
        if self.adapter:
            try:
                self.adapter.stop()
            except Exception as e:
                logger.error(f"Error stopping adapter: {e}")
        
        self.running = False
        logger.info("Deception Module stopped")
    
    def attack_honeypot(self, honeypot_id: str, attack_type: str, 
                       parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Attack a honeypot (for simulations)"""
        if not self.running:
            return {'success': False, 'error': 'Module not running'}
        
        # Use adapter if available
        if self.adapter:
            return self.adapter.attack_honeypot(honeypot_id, attack_type, parameters)
        else:
            # Fallback simulation
            import random
            return {
                'success': random.random() > 0.3,
                'honeypot_id': honeypot_id,
                'attack_type': attack_type,
                'message': 'Simulated attack (adapter not available)',
            }
    
    def get_honeypots(self) -> List[Dict[str, Any]]:
        """Get all honeypots"""
        return self.honeypots
    
    def log_interaction(self, honeypot_id: str, interaction_data: Dict[str, Any]):
        """Log an interaction with a honeypot"""
        logger.info(f"Honeypot interaction: {honeypot_id} - {interaction_data}")
        
        # Forward to adapter if available
        if self.adapter and hasattr(self.adapter, '_log_attack'):
            honeypot = next((hp for hp in self.honeypots if hp['id'] == honeypot_id), None)
            if honeypot:
                self.adapter._log_attack(honeypot, 
                                       interaction_data.get('attack_type', 'unknown'),
                                       interaction_data)
        
        # Notify other modules
        if self.engine:
            self.engine.notify_modules('deception_event', {
                'honeypot_id': honeypot_id,
                'data': interaction_data
            })
    
    def _start_monitoring(self):
        """Start monitoring for deception events"""
        # This would set up monitoring threads
        pass
    
    def status(self) -> Dict[str, Any]:
        """Get detailed status"""
        base_status = super().status()
        base_status.update({
            "honeypots_count": len(self.honeypots),
            "traps_count": len(self.traps),
            "adapter_available": self.adapter is not None,
            "adapter_running": self.adapter.running if self.adapter else False,
            "active_honeypots": [hp['name'] for hp in self.honeypots if hp.get('running', False)],
        })
        
        # Add adapter status if available
        if self.adapter:
            adapter_status = self.adapter.status()
            base_status['adapter_details'] = adapter_status
        
        return base_status

# Need List type hint
from typing import List
