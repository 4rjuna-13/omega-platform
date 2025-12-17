"""
Simple Scenario Manager
"""
import json
import os

class ScenarioManager:
    def __init__(self):
        self.data_dir = "omega_platform/data/scenarios"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Create sample scenario
        sample_path = f"{self.data_dir}/sample.json"
        if not os.path.exists(sample_path):
            sample = {
                "id": "phish_001",
                "name": "Basic Phishing",
                "mitre_techniques": ["T1566"],
                "difficulty": "easy"
            }
            with open(sample_path, 'w') as f:
                json.dump(sample, f, indent=2)
    
    def list_scenarios(self):
        scenarios = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.json'):
                with open(f"{self.data_dir}/{file}", 'r') as f:
                    scenarios.append(json.load(f))
        return scenarios
    
    def count(self):
        return len(self.list_scenarios())
