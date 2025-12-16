import platform  # Fixed: Added missing import
import json
import sys
from datetime import datetime

def test_omega_platform():
    """Test Project Omega platform components"""
    print(f"🧪 PROJECT OMEGA PLATFORM TEST - {datetime.now()}")
    print(f"✅ Python: {sys.version}")
    print(f"✅ Platform: {platform.system()} {platform.release()}")
    print(f"✅ Architecture: {platform.machine()}")
    
    # Test config
    try:
        with open('omega_config.json', 'r') as f:
            config = json.load(f)
        print(f"✅ Config loaded: {config['platform']['name']}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

if __name__ == "__main__":
    success = test_omega_platform()
    sys.exit(0 if success else 1)
