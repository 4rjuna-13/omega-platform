#!/bin/bash
echo "🚀 Starting JAIDA-Omega-SAIOS (Working Version)..."
echo "================================================="

# Activate virtual environment
source venv/bin/activate

# Ensure logs directory exists
mkdir -p logs

# Stop any existing processes
pkill -f "unified_orchestrator.py" 2>/dev/null || true
pkill -f "python.*production_logger" 2>/dev/null || true

# Start in autonomous mode with proper arguments
echo "Starting JAIDA in autonomous mode..."
python3 unified_orchestrator.py autonomous 2>&1 | tee logs/jaida_autonomous.log &
JAIDA_PID=$!
echo $JAIDA_PID > /tmp/jaida.pid

echo "✅ JAIDA started with PID: $JAIDA_PID"
echo ""
echo "📊 Monitoring:"
echo "   - Logs: tail -f logs/jaida_autonomous.log"
echo "   - Process ID: $JAIDA_PID"
echo "   - Mode: autonomous"
echo ""
echo "🛑 To stop: kill $JAIDA_PID or ./scripts/stop_jaida.sh"
echo "================================================="
