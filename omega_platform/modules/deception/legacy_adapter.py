"""
Adapter for legacy deception engine to work with new module system
"""

import sys
import os
import importlib.util
from omega_platform.modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class LegacyDeceptionAdapter(BaseModule):
    """Adapter to integrate legacy deception engine with new module system"""
    
    def __init__(self, config, engine):
        super().__init__(config, engine)
        self.legacy_engine = None
        
    def start(self):
        """Start the legacy deception engine"""
        logger.info("Starting legacy deception engine adapter...")
        
        try:
            # Dynamically load the legacy deception module
            legacy_path = os.path.join(os.path.dirname(__file__), 'legacy')
            
            # Look for Python files in the legacy directory
            python_files = [f for f in os.listdir(legacy_path) 
                           if f.endswith('.py') and not f.startswith('__')]
            
            if python_files:
                logger.info(f"Found legacy Python files: {python_files}")
                
                # Try to load the first Python file as a module
                first_module = python_files[0].replace('.py', '')
                module_path = os.path.join(legacy_path, python_files[0])
                
                # Load module dynamically
                spec = importlib.util.spec_from_file_location(first_module, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.legacy_engine = module
                    logger.info(f"Loaded legacy module: {first_module}")
                else:
                    logger.warning("Could not load legacy module")
            else:
                logger.warning("No Python files found in legacy directory")
            
            # Initialize with config
            port = self.config.get('port', 8080)
            logger.info(f"Legacy deception engine adapter configured for port {port}")
            
            # Mark as running
            self.running = True
            logger.info("Legacy deception engine adapter started")
            
        except Exception as e:
            logger.error(f"Failed to initialize legacy deception engine: {e}")
            # Don't raise - we want to continue even if legacy fails
            self.running = True  # Still mark as running for new features
    
    def stop(self):
        """Stop the legacy deception engine"""
        logger.info("Stopping legacy deception engine adapter...")
        self.running = False
        logger.info("Legacy deception engine adapter stopped")
    
    def status(self):
        """Get adapter status"""
        base_status = super().status()
        base_status.update({
            "adapter_type": "legacy_deception",
            "legacy_available": self.legacy_engine is not None,
        })
        return base_status
