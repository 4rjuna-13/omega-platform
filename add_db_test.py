#!/usr/bin/env python3
"""
Add SovereignDB test to test suite
"""

with open('test_all_components.py', 'r') as f:
    content = f.read()

# Find where tests are added and insert ours
if 'def test_deception_integration' in content:
    # Insert after deception integration test
    insert_point = content.find('def test_deception_integration')
    # Find the end of that function
    end_func = content.find('def ', insert_point + 1)
    
    new_test = '''
def test_sovereign_db():
    """Test the persistent data layer"""
    print("💾 Testing SovereignDB...")
    try:
        from sovereign_db import SovereignDB
        db = SovereignDB()
        
        # Test basic functionality
        db.register_bot(
            bot_id="TEST-PERSISTENCE-001",
            bot_class="WD",
            bot_type="wd_threat_detector",
            capabilities=["persistence_test"]
        )
        
        db.store_ioc(
            ioc_type="test_domain",
            ioc_value="test-malicious.com",
            source_layer="test",
            confidence=0.9
        )
        
        metrics = db.get_metrics()
        
        print(f"  ✅ Bot registered")
        print(f"  ✅ IOC stored")
        print(f"  ✅ Metrics: {metrics['threats']['total']} threats")
        return True
    except Exception as e:
        print(f"  ❌ SovereignDB test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
'''

    # Also need to add this test to the test execution
    # Find where tests are called
    if 'tester.test_component("Deception Integration"' in content:
        content = content.replace(
            'tester.test_component("Deception Integration"',
            'tester.test_component("Sovereign DB", test_sovereign_db)\n    tester.test_component("Deception Integration"'
        )
    
    # Insert the function
    content = content[:end_func] + new_test + content[end_func:]

with open('test_all_components_fixed.py', 'w') as f:
    f.write(content)

print("✅ Updated test suite created")
