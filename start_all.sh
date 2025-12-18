#!/bin/bash
# Start Everything

echo "🎯 Starting Complete JAIDA System"
echo "================================"

# Stop everything first
./core.sh stop
./dashboard.sh stop
sleep 2

# Create directories
mkdir -p logs data

# Start core
echo ""
echo "🚀 Starting core system..."
./core.sh start
sleep 3

# Start dashboard
echo ""
echo "🌐 Starting dashboard..."
./dashboard.sh start

echo ""
echo "================================"
echo "✅ System started successfully!"
echo ""
echo "📊 Core system: ./core.sh status"
echo "🌐 Dashboard: http://localhost:8080"
echo "🛑 To stop: ./stop_all.sh"
