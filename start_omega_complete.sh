#!/bin/bash
# PROJECT OMEGA - COMPLETE LAUNCH SCRIPT
# All integrations, one command

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                🚀 PROJECT OMEGA - FULL SUITE                ║"
echo "║  Quantum-Resistant Cybersecurity Intelligence Platform       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    source omega_env/bin/activate 2>/dev/null || {
        echo "❌ Virtual environment not found."
        echo "   Run: source omega_env/bin/activate"
        exit 1
    }
fi

echo "📊 SELECT LAUNCH MODE:"
echo "1. Full Omega Core (Recommended)"
echo "2. Natural Language Interface"
echo "3. Security Tool Integration Test"
echo "4. Enhanced Cryptography Demo"
echo "5. Wireless Security Assessment"
echo "6. Exit"
echo ""
read -p "Choice (1-6): " choice

case $choice in
    1)
        echo "🚀 Launching Omega Core..."
        python3 omega_core.py
        ;;
    2)
        echo "🗣️  Launching Natural Language Interface..."
        python3 omega_nlp.py
        ;;
    3)
        echo "🔧 Testing Tool Integrations..."
        echo "--- Nmap Integration ---"
        python3 nmap_integration.py
        echo ""
        echo "--- Metasploit Integration ---"
        python3 metasploit_wrapper.py
        ;;
    4)
        echo "🔐 Enhanced Cryptography Demo..."
        python3 enhanced_crypto.py
        ;;
    5)
        echo "📶 Wireless Security Assessment..."
        python3 wifite_integration.py
        ;;
    6)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac

echo ""
echo "⭐ PROJECT OMEGA - MISSION ACCOMPLISHED ⭐"
