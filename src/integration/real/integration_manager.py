#!/usr/bin/env python3
"""
Simplified Real Integration Manager for JAIDA-OMEGA-SAIOS
"""

import time
import threading
import json
import yaml
import logging
from datetime import datetime
from typing import Dict

from .alert_processor import RealAlertProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("IntegrationManager")

class RealIntegrationManager:
    """Manages real integration pipeline"""
    
    def __init__(self, config_path: str = "config/integration.yaml"):
        """Initialize integration manager"""
        self.config_path = config_path
        self.alert_processor = None
        self.running = False
        
        logger.info("Real Integration Manager initialized")
    
    def start(self) -> bool:
        """Start the integration pipeline"""
        if self.running:
            logger.warning("Integration manager already running")
            return False
        
        try:
            logger.info("🚀 Starting JAIDA-OMEGA-SAIOS Real Integration Pipeline")
            
            # Start alert processor
            self.alert_processor = RealAlertProcessor(self.config_path)
            self.alert_processor.start()
            
            self.running = True
            logger.info("✅ Integration pipeline started successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start integration pipeline: {e}")
            self.stop()
            return False
    
    def stop(self) -> bool:
        """Stop the integration pipeline"""
        logger.info("🛑 Stopping integration pipeline...")
        
        self.running = False
        
        # Stop components
        if self.alert_processor:
            self.alert_processor.stop()
        
        logger.info("Integration pipeline stopped")
        return True
    
    def get_status(self) -> Dict:
        """Get integration status"""
        if not self.alert_processor:
            return {"status": "not_running"}
        
        stats = self.alert_processor.get_statistics()
        
        return {
            "status": "running" if self.running else "stopped",
            "components": {
                "alert_processor": stats['processor_status']
            },
            "statistics": stats['statistics'],
            "config_sources": stats['config_sources']
        }

# Test function
def test_integration_manager():
    """Test the integration manager"""
    print("🧪 Testing Real Integration Manager...")
    
    manager = RealIntegrationManager()
    
    try:
        # Test start
        if manager.start():
            print("✅ Integration manager started")
            
            # Let it run for a bit
            time.sleep(10)
            
            # Get status
            status = manager.get_status()
            print(f"📊 Status: {status}")
            
            # Stop
            manager.stop()
            print("✅ Integration manager stopped")
        else:
            print("❌ Failed to start integration manager")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        manager.stop()

if __name__ == "__main__":
    test_integration_manager()
