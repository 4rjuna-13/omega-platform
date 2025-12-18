#!/bin/bash
# Stop Everything

echo "🛑 Stopping Complete JAIDA System"
echo "================================"

./core.sh stop
./dashboard.sh stop

echo "✅ All components stopped"
