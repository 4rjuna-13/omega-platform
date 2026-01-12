#!/bin/bash

echo "🔍 Verifying JAIDA-OMEGA-SAIOS Real Integration"
echo "=============================================="

echo "1. Checking file structure..."
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ $1"
    fi
}

check_file "src/integration/real/alert_processor.py"
check_file "src/integration/real/integration_manager.py"
check_file "omega_nexus_real_integration.py"
check_file "config/integration.yaml"
check_file "test_real_integration.py"
check_file "setup_real_integration.sh"

echo ""
echo "2. Testing Python imports..."
python3 << 'PYTHON_EOF'
import sys
sys.path.insert(0, 'src')

modules_to_test = [
    ('integration.real.alert_processor', 'RealAlertProcessor'),
    ('integration.real.integration_manager', 'RealIntegrationManager'),
]

for module_name, class_name in modules_to_test:
    try:
        module = __import__(module_name, fromlist=[class_name])
        cls = getattr(module, class_name)
        print(f"✅ {module_name}.{class_name}")
    except ImportError as e:
        print(f"❌ {module_name}.{class_name}: {e}")
    except AttributeError as e:
        print(f"❌ {module_name}.{class_name}: {e}")
PYTHON_EOF

echo ""
echo "3. Testing database..."
if [ -f "data/sovereign.db" ]; then
    python3 << 'DB_TEST_EOF'
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign.db')
    cursor = conn.cursor()
    
    # Check for real_alerts table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='real_alerts'")
    if cursor.fetchone():
        print("✅ real_alerts table exists")
    else:
        print("⚠️ real_alerts table not found")
    
    # Check for autonomous_decisions table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='autonomous_decisions'")
    if cursor.fetchone():
        cursor.execute("SELECT COUNT(*) FROM autonomous_decisions")
        count = cursor.fetchone()[0]
        print(f"✅ autonomous_decisions table exists with {count} records")
    else:
        print("⚠️ autonomous_decisions table not found")
    
    conn.close()
except Exception as e:
    print(f"❌ Database test failed: {e}")
DB_TEST_EOF
else
    echo "⚠️ Database not found at data/sovereign.db"
fi

echo ""
echo "4. Quick functionality test..."
python3 << 'FUNC_TEST_EOF'
import sys
sys.path.insert(0, 'src')

try:
    from integration.real.alert_processor import RealAlertProcessor
    
    # Create processor
    processor = RealAlertProcessor()
    print("✅ Alert processor created")
    
    # Get statistics
    stats = processor.get_statistics()
    print(f"✅ Processor status: {stats['processor_status']}")
    
    # Test alert conversion
    test_alert = {
        'alert_id': 'TEST-001',
        'alert_type': 'test',
        'severity': 8,
        'confidence': 0.9,
        'description': 'Test'
    }
    
    threat_indicator = processor._convert_alert_to_threat_indicator(test_alert)
    print(f"✅ Alert conversion works: {threat_indicator['indicator_id']}")
    
    print("\n✅ All functionality tests passed!")
    
except Exception as e:
    print(f"❌ Functionality test failed: {e}")
    import traceback
    traceback.print_exc()
FUNC_TEST_EOF

echo ""
echo "=============================================="
echo "🎯 QUICK START:"
echo "   python3 omega_nexus_real_integration.py demo --duration 60"
echo ""
echo "🚀 START INTEGRATION:"
echo "   python3 omega_nexus_real_integration.py start"
echo ""
echo "📊 CHECK STATUS:"
echo "   python3 omega_nexus_real_integration.py status"
echo ""
echo "🧪 RUN TESTS:"
echo "   python3 test_real_integration.py"
echo "=============================================="
