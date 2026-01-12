"""
Scenario Marketplace for Omega Platform
"""
import json
import os
from datetime import datetime

class ScenarioMarketplace:
    def __init__(self):
        self.marketplace_dir = "omega_platform/data/marketplace"
        os.makedirs(self.marketplace_dir, exist_ok=True)
        
        # Initialize with sample marketplace scenarios
        self._initialize_marketplace()
    
    def _initialize_marketplace(self):
        """Create sample marketplace scenarios if none exist"""
        sample_file = f"{self.marketplace_dir}/marketplace_scenarios.json"
        
        if not os.path.exists(sample_file):
            sample_scenarios = [
                {
                    "id": "market_001",
                    "name": "Advanced Spear Phishing",
                    "description": "Advanced phishing with attachment and tracking",
                    "author": "Security Team",
                    "difficulty": "medium",
                    "mitre_techniques": ["T1566", "T1566.001"],
                    "downloads": 42,
                    "rating": 4.5,
                    "category": "phishing"
                },
                {
                    "id": "market_002", 
                    "name": "Ransomware Impact Simulation",
                    "description": "Simulate ransomware encryption and impact",
                    "author": "Red Team",
                    "difficulty": "hard",
                    "mitre_techniques": ["T1486", "T1490"],
                    "downloads": 28,
                    "rating": 4.2,
                    "category": "ransomware"
                },
                {
                    "id": "market_003",
                    "name": "Web Application Exploit",
                    "description": "Simulate web app vulnerability exploitation",
                    "author": "PenTest Team",
                    "difficulty": "medium",
                    "mitre_techniques": ["T1190", "T1210"],
                    "downloads": 35,
                    "rating": 4.0,
                    "category": "web"
                }
            ]
            
            with open(sample_file, 'w') as f:
                json.dump(sample_scenarios, f, indent=2)
    
    def get_marketplace_scenarios(self):
        """Get all marketplace scenarios"""
        marketplace_file = f"{self.marketplace_dir}/marketplace_scenarios.json"
        
        if not os.path.exists(marketplace_file):
            return []
        
        with open(marketplace_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    
    def import_scenario(self, scenario_id):
        """Import a scenario from marketplace to user library"""
        marketplace = self.get_marketplace_scenarios()
        scenario = next((s for s in marketplace if s["id"] == scenario_id), None)
        
        if not scenario:
            return {"success": False, "error": "Scenario not found"}
        
        # Create user scenarios directory
        user_dir = "omega_platform/data/scenarios/user"
        os.makedirs(user_dir, exist_ok=True)
        
        # Save to user library
        user_scenario = scenario.copy()
        user_scenario["imported_at"] = datetime.now().isoformat()
        user_scenario["source"] = "marketplace"
        
        user_file = f"{user_dir}/{scenario_id}.json"
        with open(user_file, 'w') as f:
            json.dump(user_scenario, f, indent=2)
        
        # Update download count
        self._increment_download_count(scenario_id)
        
        return {
            "success": True,
            "message": f"Scenario '{scenario['name']}' imported successfully",
            "scenario": user_scenario
        }
    
    def _increment_download_count(self, scenario_id):
        """Increment download count for a scenario"""
        marketplace_file = f"{self.marketplace_dir}/marketplace_scenarios.json"
        
        if not os.path.exists(marketplace_file):
            return
        
        with open(marketplace_file, 'r') as f:
            scenarios = json.load(f)
        
        for scenario in scenarios:
            if scenario["id"] == scenario_id:
                scenario["downloads"] = scenario.get("downloads", 0) + 1
                break
        
        with open(marketplace_file, 'w') as f:
            json.dump(scenarios, f, indent=2)
    
    def get_stats(self):
        """Get marketplace statistics"""
        scenarios = self.get_marketplace_scenarios()
        
        if not scenarios:
            return {"total": 0}
        
        categories = {}
        total_downloads = 0
        
        for scenario in scenarios:
            category = scenario.get("category", "uncategorized")
            categories[category] = categories.get(category, 0) + 1
            total_downloads += scenario.get("downloads", 0)
        
        return {
            "total_scenarios": len(scenarios),
            "total_downloads": total_downloads,
            "categories": categories,
            "average_rating": sum(s.get("rating", 0) for s in scenarios) / len(scenarios) if scenarios else 0
        }
