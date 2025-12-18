#!/usr/bin/env python3
"""
OMEGA Threat Modeler - Simple Working Version
"""

import json
import uuid
import random
from datetime import datetime
from enum import Enum
from typing import Dict, List

class ThreatCategory(Enum):
    RECONNAISSANCE = "TA0043"
    INITIAL_ACCESS = "TA0001"
    EXECUTION = "TA0002"
    PERSISTENCE = "TA0003"

class Asset:
    def __init__(self, asset_id: str, name: str, asset_type: str, value: int):
        self.asset_id = asset_id
        self.name = name
        self.asset_type = asset_type
        self.value = value
        self.threats = []
        
    def add_threat(self, name: str, category: ThreatCategory):
        threat = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "category": category.value,
            "timestamp": datetime.now().isoformat()
        }
        self.threats.append(threat)
        return threat
        
    def get_risk_score(self):
        base_risk = min(self.value / 10, 10)
        threat_risk = len(self.threats) * 0.5
        return round(base_risk + threat_risk, 2)

class ThreatModeler:
    def __init__(self):
        self.models = {}
        
    def create_model(self, name: str):
        model_id = f"TM-{str(uuid.uuid4())[:8]}"
        model = {
            "id": model_id,
            "name": name,
            "assets": [],
            "created": datetime.now().isoformat()
        }
        self.models[model_id] = model
        print(f"✅ Created threat model: {name}")
        return model
        
    def add_asset(self, model_id: str, asset: Asset):
        if model_id in self.models:
            asset_data = {
                "id": asset.asset_id,
                "name": asset.name,
                "type": asset.asset_type,
                "risk_score": asset.get_risk_score(),
                "threats": asset.threats
            }
            self.models[model_id]["assets"].append(asset_data)
            return True
        return False
        
    def analyze_model(self, model_id: str):
        if model_id not in self.models:
            return None
            
        model = self.models[model_id]
        total_risk = sum(asset["risk_score"] for asset in model["assets"])
        avg_risk = total_risk / len(model["assets"]) if model["assets"] else 0
        
        return {
            "model_id": model_id,
            "name": model["name"],
            "total_assets": len(model["assets"]),
            "average_risk": round(avg_risk, 2),
            "risk_level": self._get_risk_level(avg_risk)
        }
        
    def _get_risk_level(self, score: float) -> str:
        if score >= 7.5: return "CRITICAL"
        elif score >= 5.0: return "HIGH"
        elif score >= 2.5: return "MEDIUM"
        else: return "LOW"

def test_threat_modeler():
    print("🧪 Testing Threat Modeler...")
    try:
        modeler = ThreatModeler()
        model = modeler.create_model("Test Web App")
        
        web_server = Asset("ASSET-001", "Web Server", "server", 8)
        web_server.add_threat("SQL Injection", ThreatCategory.INITIAL_ACCESS)
        web_server.add_threat("XSS", ThreatCategory.EXECUTION)
        
        database = Asset("ASSET-002", "Database", "database", 9)
        database.add_threat("Credential Theft", ThreatCategory.PERSISTENCE)
        
        modeler.add_asset(model["id"], web_server)
        modeler.add_asset(model["id"], database)
        
        analysis = modeler.analyze_model(model["id"])
        print(f"   ✅ Model analysis: {analysis['risk_level']} risk")
        print(f"   📊 Assets: {analysis['total_assets']}, Avg Risk: {analysis['average_risk']}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_threat_modeler():
        print("\n✅ Threat Modeler test passed!")
    else:
        print("\n❌ Threat Modeler test failed!")
