#!/usr/bin/env python3
"""
OMEGA LotL Simulator - Simple Working Version
"""

import json
import uuid
import random
from datetime import datetime
from enum import Enum

class LotLTool(Enum):
    POWERSHELL = "powershell"
    CMD = "cmd"
    WMI = "wmi"
    BITSADMIN = "bitsadmin"

class LotLSimulator:
    def __init__(self):
        self.simulations = {}
        
    def create_simulation(self, name: str, os: str = "windows"):
        sim_id = f"LOTL-{str(uuid.uuid4())[:8]}"
        simulation = {
            "id": sim_id,
            "name": name,
            "os": os,
            "created": datetime.now().isoformat(),
            "tools_used": [],
            "detected": 0,
            "total": 0
        }
        self.simulations[sim_id] = simulation
        print(f"✅ Created LotL simulation: {name} ({os})")
        return simulation
        
    def execute_tool(self, sim_id: str, tool: LotLTool):
        if sim_id not in self.simulations:
            return False
            
        sim = self.simulations[sim_id]
        sim["total"] += 1
        
        # Simulate execution
        detected = random.choice([True, False, False])  # 33% detection rate
        
        tool_exec = {
            "tool": tool.value,
            "timestamp": datetime.now().isoformat(),
            "detected": detected
        }
        
        sim["tools_used"].append(tool_exec)
        if detected:
            sim["detected"] += 1
            
        return tool_exec
        
    def calculate_stealth_score(self, sim_id: str):
        if sim_id not in self.simulations:
            return 0
            
        sim = self.simulations[sim_id]
        if sim["total"] == 0:
            return 100
            
        detection_rate = (sim["detected"] / sim["total"]) * 100
        stealth_score = 100 - detection_rate
        return round(stealth_score, 2)

def test_lotl_simulator():
    print("🧪 Testing LotL Simulator...")
    try:
        simulator = LotLSimulator()
        sim = simulator.create_simulation("Windows Attack", "windows")
        
        # Execute tools
        simulator.execute_tool(sim["id"], LotLTool.POWERSHELL)
        simulator.execute_tool(sim["id"], LotLTool.CMD)
        simulator.execute_tool(sim["id"], LotLTool.WMI)
        simulator.execute_tool(sim["id"], LotLTool.BITSADMIN)
        
        score = simulator.calculate_stealth_score(sim["id"])
        print(f"   ✅ Simulation: {sim['name']}")
        print(f"   🛠️  Tools used: {len(sim['tools_used'])}")
        print(f"   🔍 Detected: {sim['detected']}/{sim['total']}")
        print(f"   🥷 Stealth score: {score}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_lotl_simulator():
        print("\n✅ LotL Simulator test passed!")
    else:
        print("\n❌ LotL Simulator test failed!")
