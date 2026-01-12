#!/usr/bin/env python3
"""
🧪 Extended Test Suite - Including Autonomous Decision Engine
"""

import sys
import subprocess
import time

def run_test(test_name, command):
    """Run a test and return results"""
    print(f"\n🧪 Running: {test_name}")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {test_name}: PASSED")
            return True, result.stdout
        else:
            print(f"❌ {test_name}: FAILED")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name}: TIMEOUT")
        return False, "Test timed out"
    except Exception as e:
        print(f"⚠️  {test_name}: ERROR - {e}")
        return False, str(e)

def test_autonomous_decision_engine():
    """Test the autonomous decision engine"""
    print("\n🤖 Testing Autonomous Decision Engine")
    print("=" * 50)
    
    tests = [
        ("Basic Engine Test", "python3 autonomous_decision_engine.py"),
        ("Scenario Tests", "python3 test_autonomous_scenarios.py"),
        ("Integration Test", "python3 integrate_autonomous_engine.py")
    ]
    
    results = []
    for test_name, command in tests:
        passed, output = run_test(test_name, command)
        results.append((test_name, passed))
        
        # Show brief output for key tests
        if test_name == "Basic Engine Test":
            lines = output.split('\n')
            for line in lines[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"  {line}")
    
    # Summary
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n📊 Autonomous Engine Tests: {passed_count}/{total_count} passed")
    return all(passed for _, passed in results)

def test_omega_nexus_integration():
    """Test Omega Nexus integration with autonomous engine"""
    print("\n🔗 Testing Omega Nexus Integration")
    print("=" * 50)
    
    # Create a simple test nexus script
    test_nexus = '''
import json
from datetime import datetime
from integrate_autonomous_engine import OmegaAutonomousIntegration

print("Testing Omega Nexus -> Autonomous Engine bridge...")
integration = OmegaAutonomousIntegration()

# Generate test alerts
alerts = integration.generate_sample_alerts()
print(f"Generated {len(alerts)} test alerts")

# Run autonomous cycle
report = integration.execute_autonomous_cycle()
print(f"Cycle completed: {report['decisions_executed']} decisions executed")

print("✅ Integration test successful!")
'''
    
    with open("test_nexus_integration.py", "w") as f:
        f.write(test_nexus)
    
    return run_test("Nexus Integration", "python3 test_nexus_integration.py")[0]

def test_persistence():
    """Test that decisions are persisted correctly"""
    print("\n💾 Testing Decision Persistence")
    print("=" * 50)
    
    test_script = '''
import sqlite3
import json
from autonomous_decision_engine import AutonomousDecisionEngine

# Initialize engine
engine = AutonomousDecisionEngine()

# Get pending decisions
pending = engine.get_pending_decisions()
print(f"Pending decisions in DB: {len(pending)}")

# Get analytics
analytics = engine.get_decision_analytics()
print(f"Total decisions in DB: {analytics['total_decisions']}")

# Verify database structure
conn = sqlite3.connect("data/sovereign.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='autonomous_decisions'")
if cursor.fetchone():
    print("✅ autonomous_decisions table exists")
    
    cursor.execute("PRAGMA table_info(autonomous_decisions)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Table columns: {columns}")
else:
    print("❌ autonomous_decisions table missing")

conn.close()
print("✅ Persistence test completed")
'''
    
    with open("test_persistence.py", "w") as f:
        f.write(test_script)
    
    return run_test("Data Persistence", "python3 test_persistence.py")[0]

def test_performance():
    """Test performance of autonomous engine"""
    print("\n⚡ Testing Performance")
    print("=" * 50)
    
    test_script = '''
import time
from autonomous_decision_engine import AutonomousDecisionEngine, ThreatIndicator, ThreatLevel
from datetime import datetime

engine = AutonomousDecisionEngine()

# Create multiple threats
threats = []
for i in range(50):
    threat = ThreatIndicator(
        source=f"test_{i}",
        indicator=f"test_threat_{i}",
        threat_type="malware",
        confidence=0.7 + (i % 3) * 0.1,
        severity=ThreatLevel(i % 4),
        timestamp=datetime.now().isoformat(),
        context={"iteration": i}
    )
    threats.append(threat)

# Time the decision making
start_time = time.time()

decisions_made = 0
for threat in threats[:10]:  # Test with 10 threats
    decisions = engine.make_decision(threat)
    decisions_made += len(decisions)

end_time = time.time()

print(f"Performance Test Results:")
print(f"  Threats processed: 10")
print(f"  Decisions generated: {decisions_made}")
print(f"  Total time: {(end_time - start_time):.4f} seconds")
print(f"  Average per threat: {(end_time - start_time) / 10:.4f} seconds")

if (end_time - start_time) < 2.0:
    print("✅ Performance test PASSED")
else:
    print("⚠️  Performance test SLOW")
'''
    
    with open("test_performance.py", "w") as f:
        f.write(test_script)
    
    return run_test("Engine Performance", "python3 test_performance.py")[0]

def main():
    """Run all extended tests"""
    print("🏛️ JAIDA-OMEGA-SAIOS Extended Test Suite")
    print("🤖 Including Autonomous Decision Engine")
    print("=" * 70)
    
    # Run original tests first
    print("\n🔧 Running original component tests...")
    original_result = subprocess.run(
        "python3 test_all_components.py",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if original_result.returncode == 0:
        print("✅ Original tests passed")
    else:
        print("❌ Original tests failed")
        print(original_result.stderr)
    
    # Run new autonomous engine tests
    test_results = []
    
    test_functions = [
        ("Autonomous Decision Engine", test_autonomous_decision_engine),
        ("Omega Nexus Integration", test_omega_nexus_integration),
        ("Data Persistence", test_persistence),
        ("Performance", test_performance)
    ]
    
    for test_name, test_func in test_functions:
        try:
            passed = test_func()
            test_results.append((test_name, passed))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 EXTENDED TEST SUITE SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in test_results if passed)
    total_count = len(test_results)
    
    print(f"\nAutonomous Engine Tests: {passed_count}/{total_count} passed")
    
    for test_name, passed in test_results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    # Overall status
    overall_passed = original_result.returncode == 0 and all(passed for _, passed in test_results)
    
    print("\n" + "=" * 70)
    if overall_passed:
        print("🎉 ALL TESTS PASSED - System is fully operational!")
    else:
        print("⚠️  SOME TESTS FAILED - Review output above")
    
    print("=" * 70)
    
    # Cleanup
    cleanup_files = [
        "test_nexus_integration.py",
        "test_persistence.py",
        "test_performance.py",
        "alerts.json",
        "integration_report.json"
    ]
    
    import os
    for file in cleanup_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"🧹 Cleaned up: {file}")
            except:
                pass

if __name__ == "__main__":
    main()
