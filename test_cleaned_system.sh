#!/bin/bash
echo "🧪 Testing Cleaned JAIDA System"
echo "================================"

echo "1. Testing imports..."
python3 -c "
import sys
sys.path.insert(0, 'src')

modules = [
    ('core.jaida_core', 'Main system'),
    ('core.config_manager', 'Configuration'),
    ('adapters.real_data_adapter', 'Data adapter'),
    ('dashboard.jaida_dashboard', 'Dashboard'),
]

all_imports_ok = True
for module, desc in modules:
    try:
        __import__(module)
        print(f'  ✅ {module:25} - {desc}')
    except ImportError as e:
        print(f'  ❌ {module:25} - {desc}: {e}')
        all_imports_ok = False

if all_imports_ok:
    print('\\n✅ All imports successful!')
else:
    print('\\n⚠️  Some imports failed')
"

echo ""
echo "2. Testing main entry point..."
python3 jaida.py status

echo ""
echo "3. Testing database..."
python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
    tables = cursor.fetchall()
    
    print('  ✅ Database connected')
    print(f'  📋 {len(tables)} tables:')
    
    # Show row counts
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'    - {table[0]}: {count} rows')
    
    conn.close()
except Exception as e:
    print(f'  ❌ Database error: {e}')
"

echo ""
echo "4. Testing configuration..."
python3 -c "
import sys
sys.path.insert(0, 'src')
from core.config_manager import config

print(f'  ✅ Config loaded for {config.environment}')
print(f'  📁 Database path: {config.get(\"database.path\", \"Not set\")}')
print(f'  📡 Log level: {config.get(\"logging.level\", \"Not set\")}')
"

echo ""
echo "================================"
echo "🎯 System test completed!"
echo "🚀 Next: Run './scripts/jaida-manage start'"
