"""
Enhanced Scenario Manager that checks user directory
"""
import json
import os
from pathlib import Path

class ScenarioManagerEnhanced:
    def __init__(self):
        self.base_dir = Path("omega_platform/data/scenarios")
        self.user_dir = self.base_dir / "user"
        
        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.user_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sample scenario if none exist
        sample_path = self.base_dir / "sample.json"
        if not sample_path.exists():
            sample = {
                "id": "phishing_001",
                "name": "Basic Phishing Test",
                "description": "Test phishing scenario",
                "mitre_techniques": ["T1566"],
                "difficulty": "easy"
            }
            with open(sample_path, 'w') as f:
                json.dump(sample, f, indent=2)
    
    def list_scenarios(self):
        """Get ALL scenarios (base + user)"""
        scenarios = []
        
        # Check base directory
        for file in os.listdir(self.base_dir):
            if file.endswith('.json'):
                with open(self.base_dir / file, 'r') as f:
                    scenarios.append(json.load(f))
        
        # Check user directory
        if self.user_dir.exists():
            for file in os.listdir(self.user_dir):
                if file.endswith('.json'):
                    with open(self.user_dir / file, 'r') as f:
                        scenarios.append(json.load(f))
        
        return scenarios
    
    def count(self):
        return len(self.list_scenarios())
    
    def get_user_scenarios(self):
        """Get only user-imported scenarios"""
        scenarios = []
        if self.user_dir.exists():
            for file in os.listdir(self.user_dir):
                if file.endswith('.json'):
                    with open(self.user_dir / file, 'r') as f:
                        scenarios.append(json.load(f))
        return scenarios
    
    def get_base_scenarios(self):
        """Get only base scenarios"""
        scenarios = []
        for file in os.listdir(self.base_dir):
            if file.endswith('.json'):
                with open(self.base_dir / file, 'r') as f:
                    scenarios.append(json.load(f))
        return scenarios
