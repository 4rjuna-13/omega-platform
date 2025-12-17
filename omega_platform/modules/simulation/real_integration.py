"""
Real integration between Simulation and Deception modules
Uses the actual deception module instead of mock targets
"""

import logging
from typing import Dict, Any, List, Optional
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class RealDeceptionIntegration:
    """Real integration with deception module"""
    
    def __init__(self, engine):
        self.engine = engine
        self.deception_module = None
        self.attack_history = []
        
        # Try to get deception module from engine
        if engine and hasattr(engine, 'modules'):
            self.deception_module = engine.modules.get('deception')
            if self.deception_module:
                logger.info("Connected to real deception module")
            else:
                logger.warning("Deception module not found in engine")
    
    def get_targets(self) -> List[Dict[str, Any]]:
        """Get real honeypots from deception module"""
        targets = []
        
        if self.deception_module and hasattr(self.deception_module, 'get_honeypots'):
            try:
                honeypots = self.deception_module.get_honeypots()
                for honeypot in honeypots:
                    target = {
                        'id': honeypot.get('id', 'unknown'),
                        'type': 'real_honeypot',
                        'name': honeypot.get('name', 'Unnamed Honeypot'),
                        'service': honeypot.get('type', 'unknown'),
                        'port': honeypot.get('port', 0),
                        'realism_score': 95,  # Real honeypots are highly realistic
                        'interaction_logging': True,
                        'honeypot_data': honeypot,
                    }
                    targets.append(target)
                
                logger.info(f"Got {len(targets)} real honeypot targets")
                
            except Exception as e:
                logger.error(f"Failed to get honeypots: {e}")
                targets = self._get_fallback_targets()
        
        else:
            logger.warning("Deception module doesn't have get_honeypots method")
            targets = self._get_fallback_targets()
        
        return targets
    
    def _get_fallback_targets(self) -> List[Dict[str, Any]]:
        """Get fallback targets if deception module not available"""
        logger.warning("Using fallback simulation targets")
        return [
            {
                'id': 'sim_target_1',
                'type': 'simulated',
                'name': 'Simulated SSH Server',
                'service': 'ssh',
                'port': 22,
                'realism_score': 60,
                'interaction_logging': True,
            },
            {
                'id': 'sim_target_2',
                'type': 'simulated',
                'name': 'Simulated Web Server',
                'service': 'http',
                'port': 80,
                'realism_score': 65,
                'interaction_logging': True,
            }
        ]
    
    def attack_target(self, target_id: str, attack_type: str,
                     parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Attack a real honeypot target"""
        parameters = parameters or {}
        
        logger.info(f"Attacking target {target_id} with {attack_type}")
        
        # Check if we have a real deception module
        if self.deception_module and hasattr(self.deception_module, 'attack_honeypot'):
            try:
                # Attack the real honeypot
                result = self.deception_module.attack_honeypot(target_id, attack_type, parameters)
                
                # Add metadata
                result['target_type'] = 'real_honeypot'
                result['integration'] = 'real'
                result['timestamp'] = datetime.utcnow().isoformat()
                
                # Log the attack
                self._log_attack(target_id, attack_type, result, real=True)
                
                return result
                
            except Exception as e:
                logger.error(f"Real honeypot attack failed: {e}")
                # Fall back to simulation
        
        # Simulated attack fallback
        result = self._simulate_attack(target_id, attack_type, parameters)
        result['target_type'] = 'simulated'
        result['integration'] = 'simulated_fallback'
        
        self._log_attack(target_id, attack_type, result, real=False)
        
        return result
    
    def _simulate_attack(self, target_id: str, attack_type: str,
                        parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate an attack"""
        # Simple simulation
        import time
        time.sleep(0.2)
        
        result = {
            'success': random.random() > 0.3,
            'target_id': target_id,
            'attack_type': attack_type,
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        # Add type-specific details
        if attack_type == 'port_scan':
            result['ports_found'] = [22, 80, 443, 8080, 8443]
            result['services'] = ['ssh', 'http', 'https']
        elif attack_type == 'brute_force':
            result['attempts'] = parameters.get('attempts', 100)
            if random.random() > 0.7:
                result['credentials_found'] = ['admin:password123']
        
        return result
    
    def _log_attack(self, target_id: str, attack_type: str,
                   result: Dict[str, Any], real: bool):
        """Log attack to history"""
        attack_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'target_id': target_id,
            'attack_type': attack_type,
            'result': result,
            'real_honeypot': real,
            'success': result.get('success', False),
        }
        
        self.attack_history.append(attack_record)
        
        # Keep only last 100 records
        if len(self.attack_history) > 100:
            self.attack_history = self.attack_history[-100:]
        
        logger.info(f"Attack logged: {attack_type} on {target_id} "
                   f"(real: {real}, success: {result.get('success', False)})")
    
    def get_attack_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent attack history"""
        return self.attack_history[-limit:] if self.attack_history else []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        total = len(self.attack_history)
        if total == 0:
            return {'total_attacks': 0}
        
        real_attacks = [a for a in self.attack_history if a['real_honeypot']]
        successful = [a for a in self.attack_history if a['success']]
        
        return {
            'total_attacks': total,
            'real_honeypot_attacks': len(real_attacks),
            'simulated_attacks': total - len(real_attacks),
            'successful_attacks': len(successful),
            'success_rate': len(successful) / total if total > 0 else 0,
        }
