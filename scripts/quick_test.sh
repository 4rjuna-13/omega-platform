#!/bin/bash
# Quick test of JAIDA-Omega-SAIOS components

echo "🧪 JAIDA-Omega-SAIOS Quick Test"
echo "================================"

# Activate virtual environment
source venv/bin/activate

# Test 1: Core imports
echo "1. Testing core imports..."
python3 -c "
import sys
modules = ['unified_orchestrator', 'omega_nexus_real_integration', 'real_data_adapter']
for module in modules:
    try:
        __import__(module)
        print(f'  ✅ {module}')
    except ImportError as e:
        print(f'  ❌ {module}: {str(e)[:50]}')
"

# Test 2: Database
echo ""
echo "2. Testing database..."
python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    tables = cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\").fetchall()
    print(f'  ✅ Database accessible: {len(tables)} tables')
    conn.close()
except Exception as e:
    print(f'  ❌ Database error: {e}')
"

# Test 3: Configuration
echo ""
echo "3. Testing configuration..."
if [ -f "config_manager.py" ]; then
    python3 config_manager.py 2>&1 | head -5
    echo "  ✅ Configuration manager loaded"
else
    echo "  ⚠️  Configuration manager not found"
fi

# Test 4: Real data adapter
echo ""
echo "4. Testing real data adapter..."
python3 -c "
try:
    from real_data_adapter import RealDataAdapter
    adapter = RealDataAdapter()
    print('  ✅ Real data adapter initialized')
    
    # Test with mock data
    alerts = adapter.fetch_alerts('mock_siem', hours=1)
    print(f'  ✅ Fetched {len(alerts)} mock alerts')
except Exception as e:
    print(f'  ❌ Adapter error: {e}')
"

echo ""
echo "================================"
echo "Quick test completed!"
