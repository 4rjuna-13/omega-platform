#!/usr/bin/env python3
"""
Simple Enterprise Platform for Omega testing
"""

from enum import Enum
from typing import List, Dict, Any, Optional

class IntegrationType(Enum):
    SIEM = "siem"
    EDR = "edr"
    NETWORK = "network"
    CLOUD = "cloud"
    THREAT_INTEL = "threat_intel"

class SimpleIntegration:
    """Simple integration for testing"""
    def __init__(self, name: str, integration_type: IntegrationType):
        self.name = name
        self.type = integration_type
        self.connected = False
        self.data_received = 0
    
    def connect(self) -> Dict[str, Any]:
        """Connect the integration"""
        self.connected = True
        return {
            "status": "connected",
            "integration": self.name,
            "type": self.type.value
        }
    
    def disconnect(self) -> Dict[str, Any]:
        """Disconnect the integration"""
        self.connected = False
        return {"status": "disconnected", "integration": self.name}
    
    def send_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send an alert through the integration"""
        if not self.connected:
            return {"status": "error", "message": "Not connected"}
        
        self.data_received += 1
        return {
            "status": "sent",
            "integration": self.name,
            "alert_id": f"alert_{self.data_received:06d}",
            "data": alert_data
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return {
            "name": self.name,
            "type": self.type.value,
            "connected": self.connected,
            "data_received": self.data_received
        }

class SimpleOrchestrator:
    """Simple orchestrator for testing"""
    def __init__(self):
        self.name = "Omega Enterprise Orchestrator"
        self.version = "1.0.0"
        self.integrations: List[SimpleIntegration] = []
    
    def add_integration(self, integration: SimpleIntegration) -> Dict[str, Any]:
        """Add an integration to the orchestrator"""
        self.integrations.append(integration)
        return {
            "action": "integration_added",
            "name": integration.name,
            "total_integrations": len(self.integrations)
        }
    
    def remove_integration(self, integration_name: str) -> Dict[str, Any]:
        """Remove an integration by name"""
        for i, integ in enumerate(self.integrations):
            if integ.name == integration_name:
                del self.integrations[i]
                return {
                    "action": "integration_removed",
                    "name": integration_name,
                    "total_integrations": len(self.integrations)
                }
        return {"action": "not_found", "name": integration_name}
    
    def connect_all(self) -> List[Dict[str, Any]]:
        """Connect all integrations"""
        results = []
        for integ in self.integrations:
            results.append(integ.connect())
        return results
    
    def broadcast_alert(self, alert_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Send alert to all connected integrations"""
        results = []
        for integ in self.integrations:
            if integ.connected:
                results.append(integ.send_alert(alert_data))
        return results
    
    def get_all_status(self) -> List[Dict[str, Any]]:
        """Get status of all integrations"""
        return [integ.get_status() for integ in self.integrations]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get orchestrator summary"""
        connected = sum(1 for integ in self.integrations if integ.connected)
        total_data = sum(integ.data_received for integ in self.integrations)
        
        return {
            "name": self.name,
            "version": self.version,
            "total_integrations": len(self.integrations),
            "connected_integrations": connected,
            "total_data_received": total_data,
            "integrations": [integ.name for integ in self.integrations]
        }

# Test function for the test suite
def test_integration() -> bool:
    """Test function for test_all_components.py"""
    try:
        orchestrator = SimpleOrchestrator()
        integration = SimpleIntegration("Test SIEM", IntegrationType.SIEM)
        
        orchestrator.add_integration(integration)
        integration.connect()
        
        # Verify we have at least one integration
        return len(orchestrator.integrations) == 1
    except Exception as e:
        print(f"Integration test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing enterprise_platform_simple.py")
    
    # Run a quick test
    orchestrator = SimpleOrchestrator()
    
    # Add some integrations
    siem = SimpleIntegration("Splunk SIEM", IntegrationType.SIEM)
    edr = SimpleIntegration("CrowdStrike EDR", IntegrationType.EDR)
    
    orchestrator.add_integration(siem)
    orchestrator.add_integration(edr)
    
    # Connect them
    orchestrator.connect_all()
    
    # Send a test alert
    test_alert = {
        "severity": "high",
        "title": "Test Threat Alert",
        "source": "Omega Platform",
        "timestamp": "2025-12-17T18:30:00Z"
    }
    
    results = orchestrator.broadcast_alert(test_alert)
    
    # Print results
    print(f"✅ {orchestrator.name} v{orchestrator.version}")
    print(f"📊 Integrations: {len(orchestrator.integrations)}")
    print(f"📨 Alerts sent: {len(results)}")
    print(f"📋 Status: {orchestrator.get_summary()}")
    
    print("🎯 Enterprise module ready!")
