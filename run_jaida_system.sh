#!/bin/bash
# Run Complete JAIDA-Omega-SAIOS System

echo "🚀 Starting Complete JAIDA-Omega-SAIOS System"
echo "============================================="

# Stop any existing processes
./scripts/stop_jaida.sh 2>/dev/null

# Create necessary directories
mkdir -p logs data backups

# Start enhanced JAIDA system
echo "Starting Enhanced JAIDA with AI detection..."
python3 jaida_enhanced.py 2>&1 | tee logs/enhanced_jaida.log &
ENHANCED_PID=$!
echo $ENHANCED_PID > /tmp/jaida_enhanced.pid
echo "✅ Enhanced JAIDA started (PID: $ENHANCED_PID)"

# Wait a moment, then start dashboard
sleep 3
echo ""
echo "Starting Real-time Dashboard..."
echo "Open a new terminal and run: python3 jaida_dashboard.py"
echo "Or check logs at: tail -f logs/enhanced_jaida.log"
echo ""
echo "📊 Access Points:"
echo "   - Enhanced JAIDA: PID $ENHANCED_PID"
echo "   - Logs: tail -f logs/enhanced_jaida.log"
echo "   - Dashboard: python3 jaida_dashboard.py"
echo "   - Database: data/sovereign_data.db"
echo ""
echo "🛑 To stop: kill $ENHANCED_PID"
echo "============================================="
