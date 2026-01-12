#!/bin/bash
# Stop JAIDA-Omega-SAIOS system

echo "🛑 Stopping JAIDA-Omega-SAIOS..."
echo "================================"

# Stop by PID if exists
if [ -f "/tmp/jaida.pid" ]; then
    JAIDA_PID=$(cat /tmp/jaida.pid)
    if kill -0 $JAIDA_PID 2>/dev/null; then
        kill $JAIDA_PID
        echo "✅ Stopped JAIDA orchestrator (PID: $JAIDA_PID)"
        rm /tmp/jaida.pid
    else
        echo "⚠️  JAIDA process not running"
        rm /tmp/jaida.pid
    fi
else
    echo "⚠️  No PID file found, attempting to find and stop processes..."
    
    # Find and stop Python processes
    PIDS=$(pgrep -f "python.*(unified_orchestrator|jaida)" || true)
    if [ ! -z "$PIDS" ]; then
        echo "Found processes: $PIDS"
        kill $PIDS 2>/dev/null || true
        echo "✅ Stopped JAIDA processes"
    else
        echo "✅ No JAIDA processes found"
    fi
fi

# Stop monitoring processes
MONITOR_PIDS=$(pgrep -f "production_logger" || true)
if [ ! -z "$MONITOR_PIDS" ]; then
    kill $MONITOR_PIDS 2>/dev/null || true
    echo "✅ Stopped monitoring processes"
fi

echo ""
echo "✅ JAIDA-Omega-SAIOS stopped successfully!"
echo "========================================"
