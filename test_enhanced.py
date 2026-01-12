#!/usr/bin/env python3
"""
Test the enhanced Omega Platform
"""
import sys
sys.path.append('.')

# Test MITRE module
from omega_platform.modules.mitre_simple import MITRESimple
mitre = MITRESimple()
print("MITRE Techniques:", len(mitre.get_all()))

# Test scenario manager
from omega_platform.modules.scenario_simple import ScenarioManagerSimple
scenario_mgr = ScenarioManagerSimple()
scenarios = scenario_mgr.list_scenarios()
print("Scenarios found:", len(scenarios))

print("\n✅ Enhanced modules loaded successfully!")
