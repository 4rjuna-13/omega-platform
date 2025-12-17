"""
Integrated Simulation Module with deception targeting
"""

# This would be a refactored version combining everything
# For now, let's create a simple test to verify integration works

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def test_integration():
    """Test that simulation can integrate with deception"""
    print("Testing Simulation-Deception Integration...")
    
    try:
        from omega_platform.modules.simulation.deception_integration import DeceptionTargetManager
        print("✅ DeceptionTargetManager can be imported")
        
        # Create a mock engine
        class MockEngine:
            modules = {}
        
        engine = MockEngine()
        manager = DeceptionTargetManager(engine)
        
        # Test target scanning
        targets = manager.scan_for_targets()
        print(f"✅ Target scanning works: found {len(targets)} targets")
        
        if targets:
            # Test attacking a target
            target_id = targets[0]['id']
            result = manager.attack_target(target_id, 'port_scan', {})
            print(f"✅ Attack simulation works: {result.get('success', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import os
    test_integration()
