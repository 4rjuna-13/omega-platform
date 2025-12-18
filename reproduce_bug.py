import sys
sys.path.insert(0, '.')

try:
    from simple_threat_dashboard import ThreatDashboard
    print("✅ Dashboard imported successfully")
    
    # Create instance
    dashboard = ThreatDashboard()
    print("✅ Dashboard instance created")
    
    # Try common methods that might cause the error
    methods_to_test = ['get_summary', 'get_threat_indicators', 'generate_report']
    
    for method in methods_to_test:
        if hasattr(dashboard, method):
            try:
                result = getattr(dashboard, method)()
                print(f"✅ {method}(): returned type: {type(result)}")
                if hasattr(result, '__len__'):
                    print(f"   Length: {len(result)}")
            except Exception as e:
                print(f"❌ {method}(): ERROR - {type(e).__name__}: {e}")
        else:
            print(f"⚠️ {method}: Method not found")
            
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
