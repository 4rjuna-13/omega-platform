#!/bin/bash
# JAIDA-Omega-SAIOS Management Script

case "$1" in
    "start")
        echo "🚀 Starting JAIDA Enhanced (Fixed)..."
        pkill -f "jaida_enhanced" 2>/dev/null
        python3 jaida_enhanced_fixed.py 2>&1 | tee logs/jaida_current.log &
        echo $! > /tmp/jaida.pid
        echo "✅ Started (PID: $(cat /tmp/jaida.pid))"
        echo "📝 Logs: tail -f logs/jaida_current.log"
        ;;
    
    "stop")
        echo "🛑 Stopping JAIDA..."
        if [ -f "/tmp/jaida.pid" ]; then
            kill $(cat /tmp/jaida.pid) 2>/dev/null
            rm /tmp/jaida.pid
        fi
        pkill -f "jaida_enhanced" 2>/dev/null
        pkill -f "jaida_simple" 2>/dev/null
        echo "✅ All JAIDA processes stopped"
        ;;
    
    "status")
        echo "📊 JAIDA Status:"
        if [ -f "/tmp/jaida.pid" ] && kill -0 $(cat /tmp/jaida.pid) 2>/dev/null; then
            echo "   ✅ Running (PID: $(cat /tmp/jaida.pid))"
        else
            echo "   ❌ Not running"
        fi
        
        echo ""
        echo "📈 Database Stats:"
        python3 -c "
import sqlite3
conn = sqlite3.connect('data/sovereign_data.db')
cursor = conn.cursor()

tables = ['simple_alerts', 'enhanced_alerts', 'alerts']
for table in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f'   {table}: {count} rows')
    except:
        pass

conn.close()
"
        ;;
    
    "dashboard")
        echo "📊 Starting Dashboard..."
        python3 jaida_dashboard.py &
        echo "✅ Dashboard started"
        echo "   Press Ctrl+C in dashboard window to stop"
        ;;
    
    "logs")
        echo "📝 Showing recent logs:"
        tail -20 logs/jaida_current.log 2>/dev/null || echo "No log file found"
        ;;
    
    *)
        echo "JAIDA-Omega-SAIOS Management"
        echo "Usage: $0 {start|stop|status|dashboard|logs}"
        echo ""
        echo "Commands:"
        echo "  start     - Start enhanced JAIDA system"
        echo "  stop      - Stop all JAIDA processes"
        echo "  status    - Check system status"
        echo "  dashboard - Start real-time dashboard"
        echo "  logs      - Show recent logs"
        ;;
esac
