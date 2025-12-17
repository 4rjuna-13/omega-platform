"""
import os
Omega Engine - Core orchestration engine
"""

import time
import threading
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OmegaEngine:
    """Main Omega Platform engine"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.modules = {}
        self.running = False
        self.start_time = None
        self._load_modules()
        
    def _load_modules(self):
        """Dynamically load configured modules"""
        logger.info("Loading Omega modules...")
        
        # Load core modules from config
        module_configs = self.config.get('modules', {})
        
        for module_name, module_config in module_configs.items():
            if module_config.get('enabled', False):
                try:
                    # Dynamic import based on module name
                    import importlib
                    module_path = f"omega_platform.modules.{module_name}"
                    module_class = getattr(
                        importlib.import_module(module_path),
                        f"{module_name.capitalize()}Module"
                    )
                    
                    # Initialize module
                    self.modules[module_name] = module_class(
                        config=module_config,
                        engine=self
                    )
                    logger.info(f"Loaded module: {module_name}")
                    
                except Exception as e:
                    logger.error(f"Failed to load module {module_name}: {e}")
    
    def start(self):
        """Start the Omega engine and all modules"""
        if self.running:
            logger.warning("Engine is already running")
            return
        
        logger.info("Starting Omega Engine...")
        self.start_time = time.time()
        self.running = True
        
        # Start all modules
        for name, module in self.modules.items():
            try:
                module.start()
                logger.info(f"Started module: {name}")
            except Exception as e:
                logger.error(f"Failed to start module {name}: {e}")
        
        logger.info(f"Omega Engine started successfully (PID: {os.getpid()})")
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
                self._check_modules()
        except KeyboardInterrupt:
            logger.info("Shutdown signal received")
            self.stop()
    
    def stop(self):
        """Stop the Omega engine and all modules"""
        logger.info("Stopping Omega Engine...")
        self.running = False
        
        # Stop all modules in reverse order
        for name, module in reversed(list(self.modules.items())):
            try:
                module.stop()
                logger.info(f"Stopped module: {name}")
            except Exception as e:
                logger.error(f"Failed to stop module {name}: {e}")
        
        logger.info("Omega Engine stopped")
    
    def status(self):
        """Get engine status"""
        uptime = time.time() - self.start_time if self.start_time else 0
        
        status = {
            "running": self.running,
            "uptime": uptime,
            "modules": {},
            "version": self.get_version()
        }
        
        for name, module in self.modules.items():
            status["modules"][name] = module.status()
        
        # Pretty print status
        print(f"Omega Platform Status:")
        print(f"  Version: {status['version']}")
        print(f"  Running: {status['running']}")
        print(f"  Uptime: {uptime:.2f} seconds")
        print(f"  Modules ({len(status['modules'])}):")
        
        for name, module_status in status["modules"].items():
            print(f"    - {name}: {module_status}")
    
    def get_version(self):
        """Get Omega Platform version"""
        return "3.0.0"  # Should come from package metadata
    
    def _check_modules(self):
        """Periodic health check of all modules"""
        for name, module in self.modules.items():
            if hasattr(module, 'health_check'):
                try:
                    health = module.health_check()
                    if not health.get('healthy', True):
                        logger.warning(f"Module {name} unhealthy: {health.get('message', 'Unknown')}")
                except Exception as e:
                    logger.error(f"Health check failed for module {name}: {e}")
    
    def run_tests(self):
        """Run platform tests"""
        logger.info("Running platform tests...")
        # This would trigger the test suite
        # For now, just a placeholder
        print("Test functionality to be implemented")
