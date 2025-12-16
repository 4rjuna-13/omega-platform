#!/bin/bash
echo "=============================================="
echo "   🧪 OMEGA v4.0 TUTORIAL EDITION - TEST"
echo "=============================================="
echo ""
echo "1. Testing API status..."
curl -s http://localhost:8082/api/status
echo ""
echo ""
echo "2. Testing help endpoint..."
curl -s http://localhost:8082/api/command/help
echo ""
echo ""
echo "3. Testing tutorial list API..."
curl -s http://localhost:8082/api/tutorial/list
echo ""
echo "=============================================="
echo "✅ If you see JSON responses above, Omega v4.0"
echo "   with Tutorial Engine is WORKING!"
echo ""
echo "🌐 Open in browser: http://localhost:8082"
echo "💡 Type 'tutorial start welcome' to begin!"
echo "=============================================="
