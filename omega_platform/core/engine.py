"""
Omega Engine - Core orchestration engine
"""
import os
import sys
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from omega_platform.core.config_loader import ConfigLoader
from omega_platform.core.logging_setup import setup_logging

class OmegaEngine:
    """Main engine orchestrating all platform components."""
    
    def __init__(self, env: str = "development"):
        """Initialize Omega Engine with environment."""
        self.env = env
        self.config_loader = ConfigLoader(env)
        self.config = self.config_loader.load_config()
        
        # Setup logging
        self.logger = setup_logging(
            name="OmegaEngine",
            level=self.config.get("logging", {}).get("level", "INFO"),
            log_file=self.config.get("logging", {}).get("file", "omega_platform.log")
        )
        
        # Initialize modules
        self.modules: Dict[str, Any] = {}
        self._is_running = False
        
        self.logger.info(f"Omega Engine initialized for environment: {env}")
    
    def load_module(self, module_name: str) -> bool:
        """Dynamically load a module."""
        try:
            module_path = f"omega_platform.modules.{module_name}"
            __import__(module_path)
            module_class = getattr(sys.modules[module_path], f"{module_name.capitalize()}Module")
            
            module_config = self.config.get("modules", {}).get(module_name, {})
            module_instance = module_class(module_config)
            
            self.modules[module_name] = module_instance
            self.logger.info(f"✅ Module loaded: {module_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load module {module_name}: {e}")
            return False
    
    def load_all_modules(self) -> Dict[str, bool]:
        """Load all configured modules."""
        module_results = {}
        modules_to_load = self.config.get("modules", {}).keys()
        
        self.logger.info(f"Loading modules: {list(modules_to_load)}")
        
        for module_name in modules_to_load:
            success = self.load_module(module_name)
            module_results[module_name] = success
        
        return module_results
    
    def start(self) -> bool:
        """Start the Omega Engine and all modules."""
        try:
            self.logger.info("🚀 Starting Omega Engine...")
            
            # Load all modules
            module_results = self.load_all_modules()
            
            # Start all successfully loaded modules
            for module_name, module_instance in self.modules.items():
                try:
                    if hasattr(module_instance, 'start'):
                        module_instance.start()
                        self.logger.info(f"✅ Module started: {module_name}")
                except Exception as e:
                    self.logger.error(f"❌ Failed to start module {module_name}: {e}")
            
            self._is_running = True
            self.logger.info(f"✅ Omega Engine started successfully (PID: {os.getpid()})")
            self.logger.info(f"📊 Loaded {len(self.modules)} modules")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start Omega Engine: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop the Omega Engine and all modules."""
        try:
            self.logger.info("🛑 Stopping Omega Engine...")
            
            # Stop all modules
            for module_name, module_instance in self.modules.items():
                try:
                    if hasattr(module_instance, 'stop'):
                        module_instance.stop()
                        self.logger.info(f"✅ Module stopped: {module_name}")
                except Exception as e:
                    self.logger.warning(f"⚠️ Error stopping module {module_name}: {e}")
            
            self._is_running = False
            self.logger.info("✅ Omega Engine stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping Omega Engine: {e}")
            return False
    
    def status(self) -> Dict[str, Any]:
        """Get engine status."""
        module_statuses = {}
        for module_name, module_instance in self.modules.items():
            if hasattr(module_instance, 'status'):
                module_statuses[module_name] = module_instance.status()
            else:
                module_statuses[module_name] = {"status": "unknown"}
        
        return {
            "engine": {
                "status": "running" if self._is_running else "stopped",
                "environment": self.env,
                "pid": os.getpid(),
                "start_time": datetime.now().isoformat(),
                "modules_loaded": list(self.modules.keys())
            },
            "modules": module_statuses,
            "config": {
                "environment": self.env,
                "config_file": self.config_loader.config_path
            }
        }
    
    def run_simulation(self, scenario: str, intensity: str = "medium") -> Dict[str, Any]:
        """Run a simulation scenario."""
        if "simulation" not in self.modules:
            return {"error": "Simulation module not loaded"}
        
        try:
            self.logger.info(f"🏃 Starting simulation: {scenario} ({intensity})")
            result = self.modules["simulation"].run_scenario(scenario, intensity)
            self.logger.info(f"✅ Simulation completed: {scenario}")
            return result
        except Exception as e:
            self.logger.error(f"❌ Simulation failed: {scenario} - {e}")
            return {"error": str(e)}
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics."""
        metrics = {
            "engine": {
                "status": "running" if self._is_running else "stopped",
                "modules_count": len(self.modules),
                "uptime": "N/A",  # Would track in production
            },
            "modules": {},
            "system": {
                "memory_usage": "N/A",
                "cpu_usage": "N/A",
                "disk_usage": "N/A"
            }
        }
        
        # Add module-specific metrics
        for module_name, module_instance in self.modules.items():
            if hasattr(module_instance, 'get_metrics'):
                metrics["modules"][module_name] = module_instance.get_metrics()
        
        return metrics

def create_engine(env: str = "development") -> OmegaEngine:
    """Factory function to create Omega Engine instance."""
    return OmegaEngine(env)
