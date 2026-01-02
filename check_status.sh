#!/bin/bash
echo "📊 JAIDA-Omega-SAIOS Status Check"
echo "================================="

# Check if processes are running
echo "1. Running Processes:"
if pgrep -f "unified_orchestrator.py" > /dev/null; then
    echo "   ✅ JAIDA Orchestrator is running"
    ps aux | grep "unified_orchestrator.py" | grep -v grep
else
    echo "   ❌ JAIDA Orchestrator is NOT running"
fi

if pgrep -f "jaida_simple_working.py" > /dev/null; then
    echo "   ✅ Simple JAIDA is running"
    ps aux | grep "jaida_simple_working.py" | grep -v grep
fi

# Check database
echo ""
echo "2. Database Status:"
if [ -f "data/sovereign_data.db" ]; then
    size=$(du -h "data/sovereign_data.db" | cut -f1)
    echo "   ✅ Database exists: $size"
    
    python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    
    # Check all tables
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
    tables = cursor.fetchall()
    
    print(f'   📋 Tables: {len(tables)}')
    for table in tables:
        cursor.execute(f\"SELECT COUNT(*) FROM {table[0]};\")
        count = cursor.fetchone()[0]
        print(f'     - {table[0]}: {count} rows')
    
    conn.close()
except Exception as e:
    print(f'   ❌ Error: {e}')
"
else
    echo "   ❌ Database not found"
fi

# Check logs
echo ""
echo "3. Log Files:"
if [ -d "logs" ]; then
    echo "   ✅ Logs directory exists"
    ls -la logs/*.log 2>/dev/null | head -5
else
    echo "   ❌ Logs directory missing"
fi

echo ""
echo "================================="
echo "🚀 Quick Start: ./jaida_simple_working.py"
echo "🛑 Stop All: ./scripts/stop_jaida.sh"
