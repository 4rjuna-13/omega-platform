#!/bin/bash

echo "🤖 TESTING INTEGRATED OMEGA v3.0"
echo "================================"

cd ~/omega-platform

# Start server
echo "🚀 Starting Omega v3.0..."
pkill -f "python3 omega_" 2>/dev/null
python3 omega_v3_integrated.py &
SERVER_PID=$!
sleep 5

echo ""
echo "1. SYSTEM STATUS"
curl -s http://localhost:8081/api/status | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'   Status: {data[\"status\"]}')
print(f'   Version: {data[\"version\"]}')
print(f'   Deception: {data[\"deception\"]}')
print(f'   Response: {data[\"response\"]}')
"

echo ""
echo "2. ACTIVATE AUTONOMOUS RESPONSE"
curl -s -X POST http://localhost:8081/api/response/activate \
  -H "Content-Type: application/json" \
  -d '{"level": "MODERATE"}' | python3 -m json.tool

sleep 2

echo ""
echo "3. TEST RESPONSE SYSTEM"
curl -s -X POST http://localhost:8081/api/response/test \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

sleep 2

echo ""
echo "4. RESPONSE STATUS"
curl -s http://localhost:8081/api/response/status | python3 -m json.tool

echo ""
echo "5. START DECEPTION (if available)"
curl -s -X POST http://localhost:8081/api/deception/start \
  -H "Content-Type: application/json" \
  -d '{"level": "MEDIUM"}' 2>/dev/null | python3 -m json.tool || echo "   Deception not available"

echo ""
echo "🌐 Open browser to: http://localhost:8081"
echo ""
echo "🎮 Test the complete loop:"
echo "   1. Activate response: 'response activate aggressive'"
echo "   2. Start deception: 'deception start medium'"
echo "   3. Test honeypot: curl http://localhost:8088/"
echo "   4. Check response logs in web interface"
echo "================================"

# Keep server running
echo "Server running (PID: $SERVER_PID)"
echo "Press Ctrl+C to stop"
wait $SERVER_PID

