#!/bin/bash

echo "🚀 Starting Project Omega v2.0 with Deception Engine..."
echo "📁 Directory: $(pwd)"

# Kill any existing Omega processes
pkill -f "python3 omega_final_v2e.py" 2>/dev/null
sleep 1

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "omega_env" ]; then
        echo "🔧 Activating virtual environment..."
        source omega_env/bin/activate
    else
        echo "⚠️  Virtual environment not found. Creating one..."
        python3 -m venv omega_env
        source omega_env/bin/activate
        pip install flask flask-socketio numpy scikit-learn psutil
    fi
fi

# Check if deception engine files exist
if [ ! -f "deception_engine.py" ]; then
    echo "❌ Deception engine files not found!"
    exit 1
fi

# Start the server
echo "🌐 Starting Omega Server on port 8081..."
echo "💡 Access at: http://localhost:8081"
echo "🕵️  Deception Engine: ACTIVE"
echo ""
echo "📋 Available honeypots:"
echo "   • SSH Honeypot: port 2222"
echo "   • Web Honeypot: port 8088"
echo "   • MySQL Honeypot: port 3307"
echo ""
echo "📝 Commands to test deception:"
echo "   • 'deception start medium'"
echo "   • 'deception status'"
echo "   • 'deploy honeypot fake_ssh'"
echo ""
echo "======================================================================"

python3 omega_final_v2e.py

