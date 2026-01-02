#!/bin/bash
# Health check script for JAIDA-Omega-SAIOS

echo "🏥 JAIDA-Omega-SAIOS Health Check"
echo "================================="

# Check if processes are running
check_process() {
    if pgrep -f "$1" > /dev/null; then
        echo "✅ $2 is running"
        return 0
    else
        echo "❌ $2 is not running"
        return 1
    fi
}

check_process "python.*unified_orchestrator" "JAIDA Orchestrator"
check_process "python.*real_data_adapter" "Data Adapter"

# Check virtual environment
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment missing"
fi

# Check database
if [ -f "data/sovereign_data.db" ]; then
    DB_SIZE=$(du -h "data/sovereign_data.db" | cut -f1)
    echo "✅ Database exists: $DB_SIZE"
else
    echo "❌ Database not found"
fi

# Check logs directory
if [ -d "logs" ]; then
    LOG_COUNT=$(find logs -name "*.log" | wc -l)
    echo "✅ Logs directory: $LOG_COUNT log files"
else
    echo "❌ Logs directory missing"
fi

# Check disk space
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}')
echo "💾 Disk usage: $DISK_USAGE"

# Check Python packages
echo "🐍 Python environment:"
source venv/bin/activate 2>/dev/null && {
    python3 -c "
import sys
print(f'  Python {sys.version.split()[0]}')
try:
    import pandas; print('  ✅ pandas')
except: print('  ❌ pandas')
try:
    import flask; print('  ✅ flask')
except: print('  ❌ flask')
try:
    import sqlite3; print('  ✅ sqlite3')
except: print('  ❌ sqlite3')
"
} || echo "  ⚠️  Could not activate virtual environment"

echo ""
echo "================================="
echo "Health check completed"
