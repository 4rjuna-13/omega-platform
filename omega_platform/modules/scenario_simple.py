"""
Simple scenario manager
"""
import json
import os

class ScenarioManagerSimple:
    def __init__(self):
        self.scenarios_dir = "omega_platform/data/scenarios"
        os.makedirs(self.scenarios_dir, exist_ok=True)
        
        # Create sample scenario if none exist
        sample_file = f"{self.scenarios_dir}/sample_phishing.json"
        if not os.path.exists(sample_file):
            sample = {
                "id": "phishing_001",
                "name": "Basic Phishing Test",
                "description": "Test phishing scenario",
                "mitre_techniques": ["T1566"],
                "difficulty": "easy"
            }
            with open(sample_file, 'w') as f:
                json.dump(sample, f, indent=2)
    
    def list_scenarios(self):
        scenarios = []
        for file in os.listdir(self.scenarios_dir):
            if file.endswith('.json'):
                with open(f"{self.scenarios_dir}/{file}", 'r') as f:
                    scenarios.append(json.load(f))
        return scenarios
