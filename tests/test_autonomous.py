#!/usr/bin/env python3
"""
🧪 Test Autonomous Engine
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.autonomous.engine import AutonomousEngine, ThreatIndicator, ThreatLevel
from src.autonomous.executor import DecisionExecutor
from datetime import datetime

def test_threat_analysis():
    """Test threat analysis functionality"""
    print("Testing threat analysis...")
    
    engine = AutonomousEngine()
    
    # Create test threat
    threat = ThreatIndicator(
        source="test",
        indicator="malware.exe",
        threat_type="malware",
        confidence=0.9,
        severity=ThreatLevel.CRITICAL,
        timestamp=datetime.now().isoformat(),
        context={"file": "malware.exe", "signature": "Trojan"}
    )
    
    # Analyze threat
    analysis = engine.analyze_threat(threat)
    
    assert "threat_score" in analysis
    assert "response_level" in analysis
    assert analysis["threat_score"] > 0
    
    print(f"  ✓ Threat score: {analysis['threat_score']}")
    print(f"  ✓ Response level: {analysis['response_level']}")
    return True

def test_decision_making():
    """Test decision making functionality"""
    print("Testing decision making...")
    
    engine = AutonomousEngine()
    
    # Create test threat
    threat = ThreatIndicator(
        source="test",
        indicator="phishing_email",
        threat_type="phishing",
        confidence=0.8,
        severity=ThreatLevel.MALICIOUS,
        timestamp=datetime.now().isoformat(),
        context={"subject": "Urgent: Password Reset Required"}
    )
    
    # Make decisions
    decisions = engine.make_decision(threat)
    
    assert len(decisions) > 0
    
    print(f"  ✓ Generated {len(decisions)} decisions")
    for decision in decisions:
        print(f"    • {decision.action.value} (priority: {decision.priority})")
    
    return True

def test_decision_execution():
    """Test decision execution"""
    print("Testing decision execution...")
    
    engine = AutonomousEngine()
    executor = DecisionExecutor(engine)
    
    # Create test decision
    test_decision = {
        "decision_id": "test_exec_001",
        "action": "deploy_bots",
        "reason": "Test execution",
        "confidence": 0.9,
        "priority": 1,
        "parameters": {"bot_count": 3, "bot_type": "monitor"},
        "expected_outcome": "Test",
        "timestamp": datetime.now().isoformat()
    }
    
    # Execute decision
    result = executor.execute_decision(test_decision)
    
    assert "decision_id" in result
    assert result["decision_id"] == "test_exec_001"
    
    print(f"  ✓ Executed decision: {result['result']['message']}")
    return True

def test_persistence():
    """Test data persistence"""
    print("Testing data persistence...")
    
    engine = AutonomousEngine()
    
    # Create test threat
    threat = ThreatIndicator(
        source="persistence_test",
        indicator="test_persistence",
        threat_type="malware",
        confidence=0.7,
        severity=ThreatLevel.SUSPICIOUS,
        timestamp=datetime.now().isoformat(),
        context={"test": "persistence"}
    )
    
    # Make decisions (these get stored in DB)
    decisions = engine.make_decision(threat)
    
    # Get pending decisions from DB
    pending = engine.get_pending_decisions()
    
    assert len(pending) >= len(decisions)
    
    print(f"  ✓ Decisions stored: {len(pending)}")
    return True

def run_all_tests():
    """Run all tests"""
    print("🧪 Running Autonomous Engine Tests")
    print("="*50)
    
    tests = [
        ("Threat Analysis", test_threat_analysis),
        ("Decision Making", test_decision_making),
        ("Decision Execution", test_decision_execution),
        ("Data Persistence", test_persistence)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{test_name}...")
            result = test_func()
            if result:
                print(f"✅ {test_name}: PASSED")
                results.append(True)
            else:
                print(f"❌ {test_name}: FAILED")
                results.append(False)
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n" + "="*50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    return all(results)

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
