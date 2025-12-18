#!/bin/bash
# Simple Dashboard Management

case "$1" in
    "start")
        echo "🌐 Starting Dashboard..."
        
        # Kill any existing dashboard
        pkill -f "simple_app.py" 2>/dev/null
        
        # Start dashboard
        python3 src/dashboard/simple_app.py 2>&1 | tee logs/dashboard.log &
        echo $! > /tmp/dashboard.pid
        
        echo "✅ Dashboard started (PID: $(cat /tmp/dashboard.pid))"
        echo "🌐 Open: http://localhost:8080"
        echo "📝 Logs: tail -f logs/dashboard.log"
        ;;
    
    "stop")
        echo "🛑 Stopping Dashboard..."
        
        if [ -f "/tmp/dashboard.pid" ]; then
            kill $(cat /tmp/dashboard.pid) 2>/dev/null && echo "✅ Stopped dashboard"
            rm -f /tmp/dashboard.pid
        else
            pkill -f "simple_app.py" 2>/dev/null && echo "✅ Stopped dashboard" || echo "✅ No dashboard running"
        fi
        ;;
    
    "status")
        echo "📊 Dashboard Status"
        echo "=================="
        
        if [ -f "/tmp/dashboard.pid" ] && kill -0 $(cat /tmp/dashboard.pid) 2>/dev/null; then
            echo "✅ Running (PID: $(cat /tmp/dashboard.pid))"
            echo "🌐 URL: http://localhost:8080"
        else
            echo "❌ Not running"
            echo ""
            echo "To start: ./dashboard.sh start"
        fi
        ;;
    
    "logs")
        echo "📝 Dashboard Logs:"
        tail -20 logs/dashboard.log 2>/dev/null || echo "No log file found"
        ;;
    
    *)
        echo "🌐 JAIDA Dashboard Management"
        echo ""
        echo "Usage: $0 {start|stop|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start web dashboard"
        echo "  stop    - Stop web dashboard"
        echo "  status  - Check dashboard status"
        echo "  logs    - Show dashboard logs"
        ;;
esac
