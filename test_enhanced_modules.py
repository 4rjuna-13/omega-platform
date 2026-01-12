#!/usr/bin/env python3
"""
Test the enhanced Omega Platform modules
"""
import sys
sys.path.insert(0, '.')

print("Testing Enhanced Omega Platform Modules...")

# Test MITRE Module
from omega_platform.modules.mitre_module import MITREModule
mitre = MITREModule()
print(f"✅ MITRE Module: {len(mitre.get_all())} techniques")

# Test Scenario Manager
from omega_platform.modules.scenario_manager import ScenarioManager
scenarios = ScenarioManager()
print(f"✅ Scenario Manager: {scenarios.count()} scenarios")

# Test Data Lake
from omega_platform.modules.data_lake import SecurityDataLake
data_lake = SecurityDataLake()
events = data_lake.get_all_events()
print(f"✅ Data Lake: {len(events)} events")

# Test stats
stats = data_lake.get_stats()
print(f"✅ Data Lake Stats: {stats['total_events']} total events")

print("\n🎉 All enhanced modules loaded successfully!")
print("Ready to start enhanced web app.")
