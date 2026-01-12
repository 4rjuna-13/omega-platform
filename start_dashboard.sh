#!/bin/bash
# Omega Platform Simulation Dashboard Startup Script

echo "🚀 Starting Omega Platform Simulation Dashboard..."
echo "=============================================="

# Check if we're in the right directory
if [ ! -d "omega_platform" ]; then
    echo "❌ Error: omega_platform directory not found!"
    echo "   Please run this script from the project root directory."
    exit 1
fi

# Check Python dependencies
echo "📦 Checking Python dependencies..."
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip install -r requirements.txt 2>/dev/null || echo "⚠️  Could not install dependencies automatically"
fi

# Check if Omega Platform is available
echo "🔍 Checking Omega Platform availability..."
python -c "import omega_platform" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Omega Platform package found"
    PLATFORM_MODE="integrated"
else
    echo "⚠️  Omega Platform package not found, running in demo mode"
    PLATFORM_MODE="demo"
fi

# Create necessary directories
mkdir -p omega_platform/web/static/css
mkdir -p omega_platform/web/static/js
mkdir -p omega_platform/web/templates/dashboard

# Start the dashboard
echo "🌐 Starting simulation dashboard on http://localhost:5000"
echo ""
echo "   Dashboard URL:  http://localhost:5000"
echo "   API Status:     http://localhost:5000/api/status"
echo "   Mode:           $PLATFORM_MODE"
echo ""
echo "📊 Press Ctrl+C to stop the dashboard"
echo "=============================================="

cd omega_platform/web/dashboard
python simulation_app.py
