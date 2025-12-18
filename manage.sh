#!/bin/bash
# JAIDA Complete System Management

JAIDA_PID_FILE="/tmp/jaida.pid"
JAIDA_LOG="logs/jaida_system.log"

case "$1" in
    "start")
        echo "🚀 Starting JAIDA System..."
        
        # Stop if already running
        if [ -f "$JAIDA_PID_FILE" ]; then
            PID=$(cat "$JAIDA_PID_FILE")
            kill "$PID" 2>/dev/null && echo "Stopped previous instance"
        fi
        
        # Ensure directories exist
        mkdir -p logs data
        
        # Start core system
        python3 run_jaida.py 2>&1 | tee "$JAIDA_LOG" &
        echo $! > "$JAIDA_PID_FILE"
        
        echo "✅ JAIDA core started (PID: $(cat "$JAIDA_PID_FILE"))"
        echo "📝 Logs: tail -f $JAIDA_LOG"
        echo ""
        echo "💡 To start web dashboard: ./scripts/dashboard-manage start"
        ;;
    
    "stop")
        echo "🛑 Stopping JAIDA System..."
        
        # Stop core
        if [ -f "$JAIDA_PID_FILE" ]; then
            PID=$(cat "$JAIDA_PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                echo "✅ Stopped JAIDA core (PID: $PID)"
            else
                echo "⚠️  JAIDA core not running"
            fi
            rm -f "$JAIDA_PID_FILE"
        else
            pkill -f "run_jaida.py" 2>/dev/null && echo "✅ Stopped JAIDA core" || echo "✅ No JAIDA core running"
        fi
        
        # Stop dashboard
        ./scripts/dashboard-manage stop 2>/dev/null || true
        ;;
    
    "status")
        echo "📊 JAIDA System Status"
        echo "======================"
        
        # Core status
        echo "Core System:"
        if [ -f "$JAIDA_PID_FILE" ] && kill -0 $(cat "$JAIDA_PID_FILE") 2>/dev/null; then
            echo "  ✅ Running (PID: $(cat "$JAIDA_PID_FILE"))"
        else
            echo "  ❌ Not running"
        fi
        
        # Dashboard status
        echo ""
        echo "Web Dashboard:"
        ./scripts/dashboard-manage status 2>/dev/null | sed 's/^/  /'
        
        # Database stats
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
    for table in tables[:3]:
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'  - {table[0]}: {count} rows')
    conn.close()
except Exception as e:
    print(f'  ❌ Error: {e}')
"
        ;;
    
    "dashboard")
        echo "🌐 Managing Web Dashboard..."
        if [ -z "$2" ]; then
            ./scripts/dashboard-manage status
        else
            ./scripts/dashboard-manage "$2"
        fi
        ;;
    
    "logs")
        echo "📝 JAIDA System Logs:"
        if [ -f "$JAIDA_LOG" ]; then
            tail -20 "$JAIDA_LOG"
        else
            echo "No system log file found"
        fi
        ;;
    
    "all")
        echo "🎯 Starting Complete JAIDA System..."
        ./manage.sh stop 2>/dev/null
        sleep 2
        ./manage.sh start
        sleep 3
        ./scripts/dashboard-manage start
        echo ""
        echo "✅ Complete system started!"
        echo "🌐 Dashboard: http://localhost:8080"
        echo "📊 Check status: ./manage.sh status"
        ;;
    
    "clean")
        echo "🧹 Cleaning up..."
        ./manage.sh stop
        rm -rf __pycache__ src/__pycache__ src/*/__pycache__
        rm -f logs/*.log 2>/dev/null
        echo "✅ Cleanup complete"
        ;;
    
    "test")
        echo "🧪 Testing JAIDA..."
        python3 run_jaida.py test
        ;;
    
    "reset")
        echo "🔄 Resetting JAIDA..."
        ./manage.sh stop
        python3 run_jaida.py clean 2>/dev/null || true
        rm -f data/sovereign_data.db 2>/dev/null
        echo "✅ Reset complete"
        ;;
    
    *)
        echo "🏛️ JAIDA-OMEGA-SAIOS Complete Management"
        echo ""
        echo "Usage: $0 {start|stop|status|dashboard|logs|all|clean|test|reset}"
        echo ""
        echo "Commands:"
        echo "  start     - Start JAIDA core system"
        echo "  stop      - Stop all JAIDA components"
        echo "  status    - Show system status"
        echo "  dashboard - Manage web dashboard (start/stop/status/logs)"
        echo "  logs      - Show system logs"
        echo "  all       - Start complete system (core + dashboard)"
        echo "  clean     - Clean cache and logs"
        echo "  test      - Run system test"
        echo "  reset     - Full system reset"
        echo ""
        echo "Examples:"
        echo "  ./manage.sh all           # Start everything"
        echo "  ./manage.sh status        # Check status"
        echo "  ./manage.sh dashboard start  # Start only dashboard"
        echo "  ./manage.sh stop          # Stop everything"
        ;;
esac
