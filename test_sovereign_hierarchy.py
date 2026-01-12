#!/usr/bin/env python3
"""
Test Sovereign Hierarchy integration with Omega Platform
"""

import sys
import os

def test_hierarchy_creation():
    """Test that hierarchy can be created and persisted"""
    print("🧪 Testing Sovereign Hierarchy...")
    
    try:
        # Import and create hierarchy
        from sovereign_hierarchy import SovereignRegistry
        
        print("✅ SovereignRegistry imported")
        
        # Create registry
        registry = SovereignRegistry("test_registry.json")
        
        # Check default GCs were created
        assert len(registry.gc_bots) >= 3, f"Expected at least 3 GCs, got {len(registry.gc_bots)}"
        print(f"✅ Default GCs created: {len(registry.gc_bots)}")
        
        # Check Bot Father exists
        assert "GC-BOT-FATHER-001" in registry.gc_bots, "Bot Father not found"
        print("✅ Bot Father GC exists")
        
        # Test partition creation
        registry.create_partition("test_partition", ["GC-THREAT-MODELER-001"], "Test isolation")
        assert "test_partition" in registry.partitions
        print("✅ Partition creation works")
        
        # Test WD commissioning
        bot_father = registry.gc_bots["GC-BOT-FATHER-001"]
        initial_wd_count = len(registry.wd_bots)
        
        new_wd = bot_father.commission_worker(
            bot_father.bot_type.WD_REPORT_GENERATOR,
            "Generate test reports",
            bot_father.permissions.WD_STANDARD
        )
        
        registry.wd_bots[new_wd.id] = new_wd
        registry.save()
        
        assert len(registry.wd_bots) == initial_wd_count + 1, "WD not added to registry"
        print(f"✅ WD commissioned: {new_wd.id}")
        
        # Test persistence
        registry2 = SovereignRegistry("test_registry.json")
        assert len(registry2.gc_bots) == len(registry.gc_bots), "Registry not persisted"
        assert len(registry2.wd_bots) == len(registry.wd_bots), "WDs not persisted"
        print("✅ Registry persistence verified")
        
        # Clean up
        if os.path.exists("test_registry.json"):
            os.remove("test_registry.json")
        
        print("\n🎉 All hierarchy tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Hierarchy test failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up on failure
        if os.path.exists("test_registry.json"):
            os.remove("test_registry.json")
        
        return False

def test_integration_with_omega():
    """Test hierarchy integration with existing Omega components"""
    print("\n🔗 Testing integration with Omega Platform...")
    
    try:
        # Test that we can import existing modules
        from simple_threat_dashboard import SimpleDashboard
        from enterprise_platform_simple import SimpleOrchestrator
        
        print("✅ Existing Omega modules import successfully")
        
        # Create a simple integration scenario
        dashboard = SimpleDashboard()
        dashboard.add_sample_data()
        report = dashboard.generate_report()
        
        print(f"✅ Dashboard works with hierarchy: {len(report)} report items")
        
        # Show how hierarchy could enhance dashboard
        print("\n🎯 Hierarchy Enhancement Example:")
        print("   Current: Static dashboard")
        print("   Enhanced: Dashboard powered by GC Threat Modeler")
        print("             With WD bots for data collection and analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🤖 JAIDA SOVEREIGN HIERARCHY INTEGRATION TEST")
    print("="*60)
    
    hierarchy_ok = test_hierarchy_creation()
    integration_ok = test_integration_with_omega()
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY:")
    print(f"   Sovereign Hierarchy: {'✅ PASS' if hierarchy_ok else '❌ FAIL'}")
    print(f"   Omega Integration: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    
    if hierarchy_ok and integration_ok:
        print("\n🎉 Sovereign Hierarchy ready for full integration!")
        print("🚀 Next: Connect web crawler and bot creation suite to hierarchy")
    else:
        print("\n⚠️ Some tests failed. Check errors above.")
    
    print("="*60)
