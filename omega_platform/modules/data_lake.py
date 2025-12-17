"""
Security Data Lake for Omega Platform v4.5
"""
import json
import os
from datetime import datetime
from pathlib import Path

class SecurityDataLake:
    def __init__(self):
        self.data_dir = Path("omega_platform/data/data_lake")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.events_file = self.data_dir / "security_events.json"
        
        # Initialize with sample event if empty
        if not self.events_file.exists() or os.path.getsize(self.events_file) == 0:
            self._create_sample_events()
    
    def _create_sample_events(self):
        """Create sample security events"""
        sample_events = [
            {
                "event_id": "event_001",
                "timestamp": datetime.now().isoformat() + "Z",
                "event_type": "simulation_start",
                "scenario_id": "phishing_001",
                "scenario_name": "Basic Phishing Test",
                "threat_level": "medium",
                "mitre_techniques": ["T1566"],
                "details": {"status": "completed", "user": "test_user"}
            },
            {
                "event_id": "event_002",
                "timestamp": datetime.now().isoformat() + "Z",
                "event_type": "threat_detected",
                "scenario_id": "phish_001",
                "scenario_name": "Basic Phishing",
                "threat_level": "high",
                "mitre_techniques": ["T1566"],
                "details": {"confidence": 0.85, "source_ip": "192.168.1.100"}
            }
        ]
        
        with open(self.events_file, 'w') as f:
            json.dump(sample_events, f, indent=2)
    
    def store_event(self, event_data):
        """Store a new security event"""
        events = self.get_all_events()
        event_data["event_id"] = f"event_{len(events) + 1:03d}"
        event_data["timestamp"] = datetime.now().isoformat() + "Z"
        
        events.append(event_data)
        
        with open(self.events_file, 'w') as f:
            json.dump(events, f, indent=2)
        
        return event_data["event_id"]
    
    def get_all_events(self):
        """Get all security events"""
        if not self.events_file.exists():
            return []
        
        with open(self.events_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    
    def get_recent_events(self, limit=10):
        """Get recent events"""
        events = self.get_all_events()
        return events[-limit:] if events else []
    
    def get_events_by_scenario(self, scenario_id):
        """Get events for a specific scenario"""
        events = self.get_all_events()
        return [e for e in events if e.get("scenario_id") == scenario_id]
    
    def get_stats(self):
        """Get data lake statistics"""
        events = self.get_all_events()
        
        if not events:
            return {
                "total_events": 0,
                "event_types": {},
                "threat_levels": {},
                "scenarios": {}
            }
        
        # Calculate statistics
        event_types = {}
        threat_levels = {}
        scenarios = {}
        
        for event in events:
            # Count event types
            etype = event.get("event_type", "unknown")
            event_types[etype] = event_types.get(etype, 0) + 1
            
            # Count threat levels
            level = event.get("threat_level", "unknown")
            threat_levels[level] = threat_levels.get(level, 0) + 1
            
            # Count scenarios
            scenario = event.get("scenario_name", "unknown")
            scenarios[scenario] = scenarios.get(scenario, 0) + 1
        
        return {
            "total_events": len(events),
            "event_types": event_types,
            "threat_levels": threat_levels,
            "scenarios": scenarios,
            "latest_event": events[-1] if events else None
        }
    
    def cleanup_old_events(self, days_old=30):
        """Cleanup events older than specified days (placeholder)"""
        # Implementation would filter by timestamp
        # For now, just return current count
        events = self.get_all_events()
        return {"message": f"Would cleanup events older than {days_old} days", "current_count": len(events)}
