#!/bin/bash
# Simple Master Control for JAIDA-OMEGA-SAIOS

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           JAIDA-OMEGA-SAIOS Control Panel               ║"
echo "║                    Version 3.0.0                         ║"
echo "╚══════════════════════════════════════════════════════════╝"

case "$1" in
    "status")
        echo ""
        echo "📊 SYSTEM STATUS"
        echo "══════════════════════════════════════════════════════════"
        
        echo ""
        echo "🔍 MODULE STATUS:"
        
        if python3 -c "from simple_threat_dashboard import SimpleDashboard" 2>/dev/null; then
            echo "   ✅ Threat Dashboard: Available"
        else
            echo "   ❌ Threat Dashboard: Missing"
        fi
        
        if python3 -c "from enterprise_platform_simple import SimpleOrchestrator" 2>/dev/null; then
            echo "   ✅ Enterprise Integration: Available"
        else
            echo "   ❌ Enterprise Integration: Missing"
        fi
        
        if python3 -c "from sovereign_hierarchy import BotFather" 2>/dev/null; then
            echo "   ✅ Sovereign Hierarchy: Available"
        else
            echo "   ❌ Sovereign Hierarchy: Missing"
        fi
        
        if python3 -c "from saios_foundation import SAIOS_Core" 2>/dev/null; then
            echo "   ✅ SAIOS Foundation: Available"
        else
            echo "   ❌ SAIOS Foundation: Missing"
        fi
        
        if python3 -c "from omega_threat_modeler_simple import ThreatModeler" 2>/dev/null; then
            echo "   ✅ OMEGA Threat Modeler: Available"
        else
            echo "   ❌ OMEGA Threat Modeler: Missing"
        fi
        
        if python3 -c "from omega_purple_team_simple import PurpleTeamManager" 2>/dev/null; then
            echo "   ✅ OMEGA Purple Team: Available"
        else
            echo "   ❌ OMEGA Purple Team: Missing"
        fi
        
        if python3 -c "from omega_lotl_simulator_simple import LotLSimulator" 2>/dev/null; then
            echo "   ✅ OMEGA LotL Simulator: Available"
        else
            echo "   ❌ OMEGA LotL Simulator: Missing"
        fi
        
        echo ""
        echo "🧪 LATEST TEST RESULTS:"
        if ls omega_test_report_*.json 2>/dev/null | head -1 >/dev/null; then
            latest_report=$(ls -t omega_test_report_*.json | head -1)
            if [ -f "$latest_report" ]; then
                passed=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('passed_tests', 0))")
                total=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('total_tests', 0))")
                rate=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('success_rate', 0))")
                echo "   ✅ Passed: $passed/$total tests ($(printf "%.1f" $rate)%)"
            fi
        else
            echo "   ⚠️ No test reports found"
        fi
        ;;
        
    "test")
        echo ""
        echo "🧪 RUNNING COMPREHENSIVE TESTS..."
        echo ""
        python3 test_all_components.py
        ;;
        
    "threat-model")
        echo ""
        echo "🎯 RUNNING THREAT MODELER..."
        python3 omega_threat_modeler_simple.py
        ;;
        
    "purple-team")
        echo ""
        echo "🟣🟦 RUNNING PURPLE TEAM..."
        python3 omega_purple_team_simple.py
        ;;
        
    "lotl")
        echo ""
        echo "🛠️ RUNNING LOTL SIMULATOR..."
        python3 omega_lotl_simulator_simple.py
        ;;
        
    "deploy")
        FLEET_NAME="${2:-'Quick Response Fleet'}"
        WORKERS="${3:-3}"
        
        echo ""
        echo "🤖 DEPLOYING BOT FLEET..."
        python3 -c "
from sovereign_hierarchy import BotFather
bf = BotFather()
fleet = bf.deploy_fleet('$FLEET_NAME', num_workers=$WORKERS)
print(f'✅ Fleet deployed: {fleet[\"gc_name\"]}')
print(f'   ID: {fleet[\"fleet_id\"]}')
print(f'   Workers: {fleet[\"worker_count\"]}')
"
        ;;
        
    "context")
        echo ""
        echo "📋 GETTING CONTEXT FOR NEW CONVERSATION..."
        echo ""
        echo "Copy everything below this line:"
        echo "══════════════════════════════════════════════════════════"
        ./JAIDA_CONTEXT_SYSTEM.sh recall | sed -n '/^# 🏛️ JAIDA-OMEGA-SAIOS/,/^## 🚨 FOR NEW CONVERSATIONS:/p'
        echo "══════════════════════════════════════════════════════════"
        ;;
        
    "update")
        echo ""
        echo "🔄 UPDATING CONTEXT..."
        ./JAIDA_CONTEXT_SYSTEM.sh update
        ;;
        
    "help"|*)
        echo ""
        echo "🛠️ AVAILABLE COMMANDS:"
        echo ""
        echo "  ./omega_master_control_simple.sh status      - Check system status"
        echo "  ./omega_master_control_simple.sh test        - Run all tests"
        echo "  ./omega_master_control_simple.sh threat-model - Run threat modeler"
        echo "  ./omega_master_control_simple.sh purple-team - Run purple team"
        echo "  ./omega_master_control_simple.sh lotl        - Run LotL simulator"
        echo "  ./omega_master_control_simple.sh deploy [name] [workers]"
        echo "                                        - Deploy bot fleet"
        echo "  ./omega_master_control_simple.sh context     - Get context for new conversation"
        echo "  ./omega_master_control_simple.sh update      - Update context"
        echo "  ./omega_master_control_simple.sh help        - Show this help"
        echo ""
        echo "💡 QUICK START:"
        echo "  1. Run tests: ./omega_master_control_simple.sh test"
        echo "  2. Check status: ./omega_master_control_simple.sh status"
        echo "  3. Get context: ./omega_master_control_simple.sh context"
        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║        JAIDA-OMEGA-SAIOS: Complete Sovereign AI         ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        ;;
esac
