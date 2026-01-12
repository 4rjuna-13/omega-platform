#!/bin/bash
# Simple Core System Management

case "$1" in
    "start")
        echo "🚀 Starting JAIDA Core..."
        
        # Kill any existing core
        pkill -f "run_jaida.py" 2>/dev/null
        
        # Start core
        python3 run_jaida.py 2>&1 | tee logs/core.log &
        echo $! > /tmp/core.pid
        
        echo "✅ Core started (PID: $(cat /tmp/core.pid))"
        echo "📝 Logs: tail -f logs/core.log"
        ;;
    
    "stop")
        echo "🛑 Stopping JAIDA Core..."
        
        if [ -f "/tmp/core.pid" ]; then
            kill $(cat /tmp/core.pid) 2>/dev/null && echo "✅ Stopped core"
            rm -f /tmp/core.pid
        else
            pkill -f "run_jaida.py" 2>/dev/null && echo "✅ Stopped core" || echo "✅ No core running"
        fi
        ;;
    
    "status")
        echo "📊 Core System Status"
        echo "===================="
        
        if [ -f "/tmp/core.pid" ] && kill -0 $(cat /tmp/core.pid) 2>/dev/null; then
            echo "✅ Running (PID: $(cat /tmp/core.pid))"
            echo ""
            echo "📈 Database Stats:"
            python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
    tables = cursor.fetchall()
    print(f'  Tables: {len(tables)}')
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'  - {table[0]}: {count} rows')
    conn.close()
except Exception as e:
    print(f'  ❌ Error: {e}')
"
        else
            echo "❌ Not running"
        fi
        ;;
    
    "logs")
        echo "📝 Core System Logs:"
        tail -20 logs/core.log 2>/dev/null || echo "No log file found"
        ;;
    
    *)
        echo "🤖 JAIDA Core Management"
        echo ""
        echo "Usage: $0 {start|stop|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start core system"
        echo "  stop    - Stop core system"
        echo "  status  - Check core status"
        echo "  logs    - Show core logs"
        ;;
esac
