"""
Advanced Threat Simulation Module
Simulates realistic attack scenarios to test security controls
"""

import random
import time
import threading
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from omega_platform.modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class SimulationModule(BaseModule):
    """Advanced threat simulation engine"""
    
    def __init__(self, config: Dict[str, Any], engine):
        super().__init__(config, engine)
        self.scenarios = []
        self.agents = []
        self.active_simulations = []
        self.results = []
        self.scenario_loader = ScenarioLoader()
        self.agent_manager = AgentManager()
        
    def start(self):
        """Start the simulation module"""
        logger.info("Starting Advanced Threat Simulation Module...")
        
        # Load scenarios from configured path
        scenarios_path = self.config.get('scenarios_path', './data/scenarios/')
        self.scenarios = self.scenario_loader.load_scenarios(scenarios_path)
        
        logger.info(f"Loaded {len(self.scenarios)} simulation scenarios")
        
        # Initialize agent manager
        self.agent_manager.initialize(self.config.get('agents', {}))
        
        self.running = True
        logger.info("Advanced Threat Simulation Module started")
        
        # Start background simulation scheduler
        self._start_scheduler()
    
    def stop(self):
        """Stop the simulation module"""
        logger.info("Stopping Advanced Threat Simulation Module...")
        
        # Stop all active simulations
        for sim in self.active_simulations:
            sim.stop()
        
        # Stop all agents
        self.agent_manager.stop_all()
        
        self.running = False
        logger.info("Advanced Threat Simulation Module stopped")
    
    def _start_scheduler(self):
        """Start the simulation scheduler"""
        if self.config.get('auto_schedule', False):
            interval = self.config.get('schedule_interval', 3600)  # Default: 1 hour
            self.scheduler_thread = threading.Thread(
                target=self._run_scheduler,
                args=(interval,),
                daemon=True
            )
            self.scheduler_thread.start()
            logger.info(f"Simulation scheduler started (interval: {interval}s)")
    
    def _run_scheduler(self, interval: int):
        """Run scheduled simulations"""
        while self.running:
            time.sleep(interval)
            if self.running:
                self.run_scheduled_simulation()
    
    def run_scheduled_simulation(self):
        """Run a randomly selected simulation"""
        if not self.scenarios:
            logger.warning("No scenarios available for scheduling")
            return
        
        # Select random scenario
        scenario = random.choice(self.scenarios)
        
        # Run simulation
        logger.info(f"Running scheduled simulation: {scenario.name}")
        result = self.run_scenario(scenario.id)
        
        if result:
            logger.info(f"Scheduled simulation completed: {result['id']}")
    
    def run_scenario(self, scenario_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Run a specific simulation scenario"""
        logger.info(f"Running simulation scenario: {scenario_id}")
        
        # Find scenario
        scenario = next((s for s in self.scenarios if s.id == scenario_id), None)
        if not scenario:
            logger.error(f"Scenario not found: {scenario_id}")
            return None
        
        # Create simulation instance
        simulation = Simulation(scenario, self.engine, **kwargs)
        self.active_simulations.append(simulation)
        
        # Run simulation
        try:
            result = simulation.run()
            self.results.append(result)
            
            # Notify other modules
            self._notify_simulation_result(result)
            
            # Remove from active
            self.active_simulations.remove(simulation)
            
            return result
            
        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            return None
    
    def _notify_simulation_result(self, result: Dict[str, Any]):
        """Notify other modules about simulation results"""
        if self.engine:
            self.engine.notify_modules('simulation_complete', {
                'result': result,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    def list_scenarios(self) -> List[Dict[str, Any]]:
        """List all available scenarios"""
        return [s.to_dict() for s in self.scenarios]
    
    def get_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent simulation results"""
        return self.results[-limit:] if self.results else []
    
    def create_custom_scenario(self, name: str, steps: List[Dict[str, Any]], 
                              **kwargs) -> Dict[str, Any]:
        """Create a custom simulation scenario"""
        scenario = {
            'id': f"custom_{int(time.time())}",
            'name': name,
            'steps': steps,
            'created': datetime.utcnow().isoformat(),
            **kwargs
        }
        
        # Add to scenarios
        self.scenarios.append(Scenario.from_dict(scenario))
        
        # Save to disk if configured
        if self.config.get('save_custom_scenarios', True):
            self._save_custom_scenario(scenario)
        
        return scenario
    
    def _save_custom_scenario(self, scenario: Dict[str, Any]):
        """Save custom scenario to disk"""
        try:
            scenarios_path = self.config.get('scenarios_path', './data/scenarios/')
            os.makedirs(scenarios_path, exist_ok=True)
            
            filename = f"{scenario['id']}.json"
            filepath = os.path.join(scenarios_path, filename)
            
            with open(filepath, 'w') as f:
                json.dump(scenario, f, indent=2)
            
            logger.info(f"Saved custom scenario: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to save custom scenario: {e}")
    
    def status(self) -> Dict[str, Any]:
        """Get detailed status"""
        base_status = super().status()
        base_status.update({
            "scenarios_loaded": len(self.scenarios),
            "active_simulations": len(self.active_simulations),
            "total_results": len(self.results),
            "agent_count": self.agent_manager.count(),
            "scheduler_running": hasattr(self, 'scheduler_thread') 
                               and self.scheduler_thread.is_alive(),
        })
        return base_status

# Supporting classes
class Scenario:
    """Simulation scenario definition"""
    
    def __init__(self, scenario_id: str, name: str, description: str = "", 
                 steps: List[Dict[str, Any]] = None, tags: List[str] = None,
                 difficulty: str = "medium", estimated_time: int = 300):
        self.id = scenario_id
        self.name = name
        self.description = description
        self.steps = steps or []
        self.tags = tags or []
        self.difficulty = difficulty
        self.estimated_time = estimated_time  # in seconds
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'steps': self.steps,
            'tags': self.tags,
            'difficulty': self.difficulty,
            'estimated_time': self.estimated_time,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scenario':
        return cls(
            scenario_id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            steps=data.get('steps', []),
            tags=data.get('tags', []),
            difficulty=data.get('difficulty', 'medium'),
            estimated_time=data.get('estimated_time', 300),
        )

class ScenarioLoader:
    """Loads simulation scenarios from disk"""
    
    def load_scenarios(self, path: str) -> List[Scenario]:
        """Load all scenarios from a directory"""
        scenarios = []
        
        try:
            if not os.path.exists(path):
                logger.warning(f"Scenarios path does not exist: {path}")
                return scenarios
            
            # Load built-in scenarios first
            scenarios.extend(self._load_builtin_scenarios())
            
            # Load from files
            for filename in os.listdir(path):
                if filename.endswith('.json'):
                    filepath = os.path.join(path, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            scenario = Scenario.from_dict(data)
                            scenarios.append(scenario)
                            logger.debug(f"Loaded scenario: {scenario.name}")
                    except Exception as e:
                        logger.error(f"Failed to load scenario {filename}: {e}")
            
        except Exception as e:
            logger.error(f"Failed to load scenarios: {e}")
        
        return scenarios
    
    def _load_builtin_scenarios(self) -> List[Scenario]:
        """Load built-in simulation scenarios"""
        builtin_scenarios = [
            Scenario(
                scenario_id="apt_simulation_1",
                name="APT Campaign Simulation",
                description="Simulates an Advanced Persistent Threat campaign",
                steps=[
                    {"type": "reconnaissance", "target": "network_scan", "duration": 60},
                    {"type": "initial_access", "method": "phishing", "targets": 5},
                    {"type": "lateral_movement", "technique": "pass_the_hash"},
                    {"type": "data_exfiltration", "data_size": "100MB"},
                ],
                tags=["apt", "campaign", "enterprise"],
                difficulty="hard",
                estimated_time=1800,
            ),
            Scenario(
                scenario_id="ransomware_1",
                name="Ransomware Attack",
                description="Simulates a ransomware infection and encryption",
                steps=[
                    {"type": "initial_infection", "vector": "malicious_email"},
                    {"type": "propagation", "method": "network_shares"},
                    {"type": "encryption", "targets": ["documents", "databases"]},
                    {"type": "ransom_note", "message": "Your files are encrypted!"},
                ],
                tags=["ransomware", "encryption", "crypto"],
                difficulty="medium",
                estimated_time=600,
            ),
            Scenario(
                scenario_id="insider_threat_1",
                name="Insider Threat",
                description="Simulates malicious activity from an internal user",
                steps=[
                    {"type": "credential_theft", "method": "shoulder_surfing"},
                    {"type": "data_access", "sensitive_data": True},
                    {"type": "data_exfiltration", "method": "usb_drive"},
                ],
                tags=["insider", "data_theft", "internal"],
                difficulty="easy",
                estimated_time=300,
            ),
        ]
        
        return builtin_scenarios

class AgentManager:
    """Manages simulation agents"""
    
    def __init__(self):
        self.agents = {}
    
    def initialize(self, agent_configs: Dict[str, Any]):
        """Initialize agents from configuration"""
        # This would create agent instances based on config
        # For now, just a placeholder
        self.agents = {}
    
    def stop_all(self):
        """Stop all agents"""
        for agent_id, agent in self.agents.items():
            try:
                agent.stop()
            except Exception as e:
                logger.error(f"Failed to stop agent {agent_id}: {e}")
    
    def count(self) -> int:
        """Get number of agents"""
        return len(self.agents)

class Simulation:
    """Individual simulation instance"""
    
    def __init__(self, scenario: Scenario, engine, **kwargs):
        self.scenario = scenario
        self.engine = engine
        self.kwargs = kwargs
        self.running = False
        self.start_time = None
        self.end_time = None
        self.result = None
        
    def run(self) -> Dict[str, Any]:
        """Run the simulation"""
        self.running = True
        self.start_time = datetime.utcnow()
        
        logger.info(f"Starting simulation: {self.scenario.name}")
        
        results = {
            'id': f"sim_{int(time.time())}_{self.scenario.id}",
            'scenario_id': self.scenario.id,
            'scenario_name': self.scenario.name,
            'start_time': self.start_time.isoformat(),
            'steps': [],
            'success': True,
            'errors': [],
        }
        
        # Execute each step
        for i, step in enumerate(self.scenario.steps):
            step_result = self._execute_step(i, step, results)
            results['steps'].append(step_result)
            
            # Check if step failed
            if not step_result.get('success', True):
                results['success'] = False
                results['errors'].append(step_result.get('error', 'Unknown error'))
        
        self.end_time = datetime.utcnow()
        results['end_time'] = self.end_time.isoformat()
        results['duration'] = (self.end_time - self.start_time).total_seconds()
        
        self.result = results
        self.running = False
        
        logger.info(f"Simulation completed: {results['id']} (success: {results['success']})")
        
        return results
    
    def _execute_step(self, step_index: int, step: Dict[str, Any], 
                     results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a simulation step"""
        step_result = {
            'step_index': step_index,
            'step_type': step.get('type', 'unknown'),
            'start_time': datetime.utcnow().isoformat(),
            'success': True,
        }
        
        try:
            # Execute based on step type
            step_type = step.get('type', 'unknown')
            
            if step_type == 'reconnaissance':
                self._execute_reconnaissance(step, step_result)
            elif step_type == 'initial_access':
                self._execute_initial_access(step, step_result)
            elif step_type == 'lateral_movement':
                self._execute_lateral_movement(step, step_result)
            elif step_type == 'data_exfiltration':
                self._execute_data_exfiltration(step, step_result)
            elif step_type == 'encryption':
                self._execute_encryption(step, step_result)
            else:
                # Generic step execution
                step_result['message'] = f"Executed step: {step_type}"
                time.sleep(step.get('duration', 1))  # Simulate work
            
            # Notify engine about step execution
            if self.engine:
                self.engine.notify_modules('simulation_step', {
                    'step': step,
                    'result': step_result,
                    'scenario': self.scenario.name,
                })
            
        except Exception as e:
            step_result['success'] = False
            step_result['error'] = str(e)
            logger.error(f"Step {step_index} failed: {e}")
        
        step_result['end_time'] = datetime.utcnow().isoformat()
        
        return step_result
    
    def _execute_reconnaissance(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Execute reconnaissance step"""
        target = step.get('target', 'network')
        duration = step.get('duration', 30)
        
        result['details'] = {
            'target': target,
            'duration': duration,
            'techniques': ['port_scan', 'service_discovery', 'os_fingerprinting']
        }
        
        # Simulate reconnaissance
        time.sleep(min(duration, 5))  # Cap at 5 seconds for simulation
        
        # If engine has deception module, check if detected
        if self.engine and 'deception' in self.engine.modules:
            deception_module = self.engine.modules['deception']
            result['deception_detected'] = True  # Would actually check
        
        result['message'] = f"Reconnaissance completed on {target}"
    
    def _execute_initial_access(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Execute initial access step"""
        method = step.get('method', 'phishing')
        targets = step.get('targets', 1)
        
        result['details'] = {
            'method': method,
            'targets': targets,
            'success_rate': random.uniform(0.1, 0.5),  # Simulated success rate
        }
        
        time.sleep(2)
        result['message'] = f"Initial access attempted via {method}"
    
    def _execute_lateral_movement(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Execute lateral movement step"""
        technique = step.get('technique', 'pass_the_hash')
        
        result['details'] = {
            'technique': technique,
            'systems_compromised': random.randint(1, 5),
        }
        
        time.sleep(3)
        result['message'] = f"Lateral movement using {technique}"
    
    def _execute_data_exfiltration(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Execute data exfiltration step"""
        data_size = step.get('data_size', '10MB')
        method = step.get('method', 'https')
        
        result['details'] = {
            'data_size': data_size,
            'method': method,
            'destination': 'external_server',
        }
        
        time.sleep(2)
        result['message'] = f"Data exfiltration simulated: {data_size} via {method}"
    
    def _execute_encryption(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Execute encryption step"""
        targets = step.get('targets', ['files'])
        
        result['details'] = {
            'targets': targets,
            'files_encrypted': random.randint(100, 1000),
            'ransom_amount': random.uniform(0.1, 10),  # In Bitcoin for simulation
        }
        
        time.sleep(2)
        result['message'] = f"Encryption simulation on {len(targets)} target types"
    
    def stop(self):
        """Stop the simulation"""
        self.running = False
        logger.info(f"Simulation stopped: {self.scenario.name}")

# Need to import os for the module
import os

# Add at the top of the file, after other imports
from .deception_integration import DeceptionTargetManager

# Update the SimulationModule class __init__ method:
# Add this line after self.agent_manager = AgentManager()
#         self.target_manager = DeceptionTargetManager(engine)

# Update the Simulation class _execute_reconnaissance method to use real targets:
# Replace the current _execute_reconnaissance with:

    def _execute_reconnaissance(self, step: Dict[str, Any], result: Dict[str, Any]):
        """Execute reconnaissance step using deception targets"""
        target = step.get('target', 'network')
        duration = step.get('duration', 30)
        
        # Use target manager if available
        targets_found = []
        if hasattr(self, 'simulation_module') and hasattr(self.simulation_module, 'target_manager'):
            targets = self.simulation_module.target_manager.scan_for_targets()
            targets_found = [t['name'] for t in targets]
        
        result['details'] = {
            'target': target,
            'duration': duration,
            'targets_found': targets_found,
            'techniques': ['port_scan', 'service_discovery', 'os_fingerprinting']
        }
        
        # Simulate reconnaissance
        time.sleep(min(duration, 5))
        
        # If we have targets, simulate scanning them
        if targets_found and hasattr(self, 'simulation_module') and hasattr(self.simulation_module, 'target_manager'):
            for target in self.simulation_module.target_manager.available_targets[:3]:  # Scan first 3
                scan_result = self.simulation_module.target_manager.attack_target(
                    target['id'], 'port_scan', {}
                )
                if scan_result.get('success'):
                    result['details']['scan_results'] = result['details'].get('scan_results', [])
                    result['details']['scan_results'].append({
                        'target': target['name'],
                        'ports': scan_result.get('ports_found', []),
                    })
        
        result['message'] = f"Reconnaissance completed, found {len(targets_found)} targets"
