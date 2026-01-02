#!/bin/bash
# Start JAIDA-Omega-SAIOS system

set -e

echo "🚀 Starting JAIDA-Omega-SAIOS..."
echo "================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./deploy_production_fixed.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check for required files
if [ ! -f "unified_orchestrator.py" ]; then
    echo "❌ Main orchestrator file not found"
    exit 1
fi

# Create necessary directories
mkdir -p data logs backups

# Start the orchestrator
echo "Starting JAIDA orchestrator..."
python3 unified_orchestrator.py &
JAIDA_PID=$!
echo $JAIDA_PID > /tmp/jaida.pid
echo "✅ JAIDA orchestrator started (PID: $JAIDA_PID)"

# Start monitoring if available
if [ -f "production_logger.py" ]; then
    echo "Starting monitoring..."
    python3 -c "from production_logger import metrics; print('📊 Metrics server running')" &
    echo "✅ Monitoring started"
fi

echo ""
echo "✅ JAIDA-Omega-SAIOS started successfully!"
echo ""
echo "📊 Access points:"
echo "   - Logs: tail -f logs/jaida.log"
echo "   - Metrics: http://localhost:9090 (if monitoring enabled)"
echo ""
echo "🛑 To stop: ./scripts/stop_jaida.sh"
echo ""
echo "========================================"
