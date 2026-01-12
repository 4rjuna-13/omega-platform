#!/usr/bin/env python3
"""
Update the test_engine function in engine.py
"""
import re

with open('src/autonomous/engine.py', 'r') as f:
    content = f.read()

# Find and replace the test_engine function
new_test_function = '''def test_engine():
    """Test the autonomous engine"""
    print("Testing Autonomous Engine...")
    
    engine = AutonomousEngine()
    
    # Create test threat
    test_threat = ThreatIndicator(
        id="test_threat_001",
        source="test",
        indicator="test_malware",
        threat_type="malware",
        confidence=0.85,
        severity=ThreatLevel.CRITICAL,
        timestamp=datetime.now().isoformat(),
        context={"test": True}
    )
    
    # Make decisions
    decisions = engine.make_decision(test_threat)
    
    print(f"Generated {len(decisions)} decisions:")
    for decision in decisions:
        print(f"  • {decision.action.value} (confidence: {decision.confidence:.2%})")
    
    return decisions'''

# Replace the old function
pattern = r'def test_engine\(\):.*?(?=\n\n\S|\Z)'
content = re.sub(pattern, new_test_function, content, flags=re.DOTALL)

# Write back
with open('src/autonomous/engine.py', 'w') as f:
    f.write(content)

print("✅ Updated test_engine function")
