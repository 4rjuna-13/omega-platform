print("🔍 Debugging SimpleDashboard...")

try:
    from simple_threat_dashboard import SimpleDashboard
    print("✅ Imported SimpleDashboard")
    
    dashboard = SimpleDashboard()
    print("✅ Created dashboard instance")
    
    # Try add_sample_data
    print("\nTesting add_sample_data()...")
    try:
        dashboard.add_sample_data()
        print("✅ add_sample_data() succeeded")
    except Exception as e:
        print(f"❌ add_sample_data() failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    # Try generate_report
    print("\nTesting generate_report()...")
    try:
        report = dashboard.generate_report()
        print(f"✅ generate_report() succeeded")
        print(f"   Report has keys: {list(report.keys())}")
        if 'summary' in report:
            print(f"   Summary: {report['summary']}")
    except Exception as e:
        print(f"❌ generate_report() failed: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
