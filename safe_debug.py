print("🔍 Safe debug - checking file structure...")
import os
files = ['simple_threat_dashboard.py', 'test_all_components.py']
for f in files:
    if os.path.exists(f):
        print(f"✅ {f}: {os.path.getsize(f)} bytes")
    else:
        print(f"❌ {f}: NOT FOUND")
