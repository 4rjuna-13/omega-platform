#!/bin/bash
echo "======================================================================"
echo "   🚀 PROJECT OMEGA v4.0 - TUTORIAL EDITION LAUNCHER"
echo "======================================================================"
echo ""
echo "📊 Phase 2G: Interactive Learning & Safe Sandbox"
echo "   • 5 Progressive Tutorials"
echo "   • Safe Sandbox Mode"
echo "   • Achievement System"
echo "   • Training Scenarios"
echo ""
echo "🛑 Stopping any existing Omega servers..."
pkill -f "omega.*\.py" 2>/dev/null || true
sleep 2
echo ""
echo "🌐 Starting Omega v4.0 on http://localhost:8082"
echo "💡 Type 'tutorial start welcome' to begin!"
echo "======================================================================"
echo ""
python3 omega_v4_tutorial_working.py
