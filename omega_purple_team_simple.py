#!/usr/bin/env python3
"""
OMEGA Purple Team - Simple Working Version
"""

import json
import uuid
import random
from datetime import datetime
from typing import Dict, List

class PurpleTeamManager:
    def __init__(self):
        self.exercises = {}
        
    def create_exercise(self, name: str, scenario: str = "phishing"):
        ex_id = f"EX-{str(uuid.uuid4())[:8]}"
        exercise = {
            "id": ex_id,
            "name": name,
            "scenario": scenario,
            "created": datetime.now().isoformat(),
            "status": "planned",
            "red_actions": 0,
            "blue_actions": 0,
            "detections": 0
        }
        self.exercises[ex_id] = exercise
        print(f"✅ Created exercise: {name} ({scenario})")
        return exercise
        
    def run_simulation(self, exercise_id: str):
        if exercise_id not in self.exercises:
            return None
            
        ex = self.exercises[exercise_id]
        ex["status"] = "running"
        
        # Simulate actions
        ex["red_actions"] = random.randint(3, 8)
        ex["blue_actions"] = random.randint(5, 12)
        ex["detections"] = random.randint(2, ex["red_actions"])
        
        ex["detection_rate"] = round((ex["detections"] / ex["red_actions"]) * 100, 2)
        ex["status"] = "completed"
        ex["completed"] = datetime.now().isoformat()
        
        return ex

def test_purple_team():
    print("🧪 Testing Purple Team...")
    try:
        manager = PurpleTeamManager()
        exercise = manager.create_exercise("APT Simulation", "ransomware")
        results = manager.run_simulation(exercise["id"])
        
        print(f"   ✅ Exercise: {results['name']}")
        print(f"   🟥 Red actions: {results['red_actions']}")
        print(f"   🟦 Blue actions: {results['blue_actions']}")
        print(f"   🔍 Detections: {results['detections']}")
        print(f"   📊 Detection rate: {results['detection_rate']}%")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    if test_purple_team():
        print("\n✅ Purple Team test passed!")
    else:
        print("\n❌ Purple Team test failed!")
