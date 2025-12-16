#!/bin/bash
echo "🚀 Testing Project Omega Fixed Version..."
echo "=========================================="

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    source omega_env/bin/activate
fi

# Test the fixed version
echo "🔄 Starting Omega Command Center (Fixed)..."
python3 omega_complete_fixed.py &
SERVER_PID=$!

# Give server time to start
sleep 3

echo "✅ Server started with PID: $SERVER_PID"
echo "🌐 Access at: http://localhost:8081"
echo ""
echo "📋 Quick commands:"
echo "   • View logs: tail -f omega_log.txt"
echo "   • Check status: curl http://localhost:8081/api/status"
echo "   • Stop server: kill $SERVER_PID"
echo ""
echo "Press Ctrl+C to stop this script (server will continue running)"
echo "=========================================="

# Keep script running
wait $SERVER_PID
