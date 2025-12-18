#!/bin/bash
echo "🔍 Verifying JAIDA-Omega-SAIOS System"
echo "====================================="

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
fi

echo ""
echo "1. Checking Python dependencies..."
python3 -c "
import sys
deps = ['pandas', 'numpy', 'flask', 'yaml', 'prometheus_client', 'sqlite3']
for dep in deps:
    try:
        __import__(dep)
        print(f'   ✅ {dep}')
    except ImportError as e:
        print(f'   ❌ {dep} - not installed')
"

echo ""
echo "2. Checking system components..."
python3 -c "
import sys
sys.path.insert(0, '.')
components = [
    ('JAIDA Orchestrator', 'unified_orchestrator'),
    ('Real Data Adapter', 'real_data_adapter'),
    ('Omega Nexus', 'omega_nexus_enhanced'),
    ('Config Manager', 'config_manager'),
    ('Production Logger', 'production_logger'),
]

for name, module in components:
    try:
        __import__(module)
        print(f'   ✅ {name}')
    except ImportError as e:
        print(f'   ❌ {name} - file not found')
    except Exception as e:
        print(f'   ⚠️  {name} - error: {str(e)[:50]}')
"

echo ""
echo "3. Checking files and directories..."
echo "   Current directory: $(pwd)"
echo "   Files:"
ls -la | grep -E "\.(py|sh|db|yaml)$" | head -10
echo ""
echo "   Directories:"
ls -la | grep "^d" | head -10

echo ""
echo "4. Checking database..."
if [ -f "data/sovereign_data.db" ]; then
    echo "   ✅ Database exists at data/sovereign_data.db"
    python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    tables = cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\").fetchall()
    print(f'   📊 Tables: {len(tables)}')
    for table in tables[:3]:
        print(f'     - {table[0]}')
    conn.close()
except Exception as e:
    print(f'   ❌ Database error: {e}')
"
else
    echo "   ❌ Database not found"
    echo "   Looking for database files:"
    find . -name "*.db" -o -name "*.sqlite" 2>/dev/null | head -5
fi

echo ""
echo "====================================="
echo "📋 Summary: Run these commands to fix:"
echo "   1. cd ~/omega-platform/omega-platform"
echo "   2. source venv/bin/activate"
echo "   3. pip install flask pyyaml prometheus_client"
echo "   4. ./scripts/start_jaida.sh"
echo "====================================="
