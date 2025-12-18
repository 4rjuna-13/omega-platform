#!/bin/bash
# Omega Master Control - Unified control for JAIDA-OMEGA-SAIOS

VERSION="3.0.0"
SYSTEM_NAME="JAIDA-OMEGA-SAIOS"

print_header() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                $SYSTEM_NAME Control Panel                ║"
    echo "║                    Version $VERSION                       ║"
    echo "╚══════════════════════════════════════════════════════════╝"
}

print_saios_header() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                 SAIOS FOUNDATION LAYER                   ║"
    echo "║           Sovereign Authentic Intelligence OS            ║"
    echo "╚══════════════════════════════════════════════════════════╝"
}

print_omega_header() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                OMEGA OPERATIONAL LAYER                   ║"
    echo "║           Multi-faceted Enhanced Guardian Arch           ║"
    echo "╚══════════════════════════════════════════════════════════╝"
}

case "$1" in
    "start"|"demo")
        print_header
        echo ""
        echo "🚀 Starting Integrated Demo..."
        echo ""
        
        python3 integrated_demo.py
        
        echo ""
        echo "✅ System demo completed successfully!"
        echo ""
        echo "💡 Available commands:"
        echo "   ./omega_master_control.sh omega      - OMEGA operational demo"
        echo "   ./omega_master_control.sh saios      - SAIOS foundation demo"
        echo "   ./omega_master_control.sh status     - Check system status"
        echo "   ./omega_master_control.sh test       - Run all tests"
        echo "   ./omega_master_control.sh deploy     - Deploy new fleet"
        ;;
        
    "saios")
        print_saios_header
        echo ""
        echo "🚀 Starting SAIOS Foundation Demo..."
        echo ""
        
        python3 saios_integrated_demo.py
        
        echo ""
        echo "✅ SAIOS foundation demo completed!"
        echo ""
        echo "🔐 SOVEREIGN CAPABILITIES:"
        echo "   • JAI-LSD-25 Token Authentication"
        echo "   • Privilege-Based Command Execution"
        echo "   • GC Isolation Partitions"
        echo "   • Hardware-Level Execution"
        echo "   • Sovereign Mode (Unrestricted)"
        ;;
        
    "omega")
        print_omega_header
        echo ""
        echo "🚀 Starting OMEGA Operational Demo..."
        echo ""
        
        python3 omega_complete_demo.py
        
        echo ""
        echo "✅ OMEGA operational demo completed!"
        echo ""
        echo "🛡️ OMEGA COMPONENTS:"
        echo "   • Threat Modeler - Advanced threat modeling"
        echo "   • Purple Team - Red/Blue team simulation"
        echo "   • LotL Simulator - Living off the Land attacks"
        echo "   • SAIOS Integration - Automated response"
        ;;
        
    "status")
        print_header
        echo ""
        echo "📊 SYSTEM STATUS"
        echo "══════════════════════════════════════════════════════════"
        
        # Check all modules
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
        
        if python3 -c "from omega_threat_modeler import ThreatModeler" 2>/dev/null; then
            echo "   ✅ OMEGA Threat Modeler: Available"
        else
            echo "   ❌ OMEGA Threat Modeler: Missing"
        fi
        
        if python3 -c "from omega_purple_team import PurpleTeamManager" 2>/dev/null; then
            echo "   ✅ OMEGA Purple Team: Available"
        else
            echo "   ❌ OMEGA Purple Team: Missing"
        fi
        
        if python3 -c "from omega_lotl_simulator import LotLSimulator" 2>/dev/null; then
            echo "   ✅ OMEGA LotL Simulator: Available"
        else
            echo "   ❌ OMEGA LotL Simulator: Missing"
        fi
        
        # Test results
        echo ""
        echo "🧪 TEST RESULTS:"
        if ls omega_test_report_*.json 2>/dev/null | head -1 >/dev/null; then
            latest_report=$(ls -t omega_test_report_*.json | head -1)
            if [ -f "$latest_report" ]; then
                passed=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('passed_tests', 0))")
                total=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('total_tests', 0))")
                rate=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('success_rate', 0))")
                timestamp=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('timestamp', ''))")
                echo "   📅 Last test: $(echo $timestamp | cut -d'T' -f1)"
                echo "   ✅ Passed: $passed/$total tests ($(printf "%.1f" $rate)%)"
            fi
        else
            echo "   ⚠️ No test reports found"
        fi
        
        # SAIOS status
        echo ""
        echo "🔐 SAIOS FOUNDATION STATUS:"
        python3 -c "
try:
    from saios_foundation import SAIOS_Core
    saios = SAIOS_Core()
    status = saios.get_system_status()
    print(f'   ✅ SAIOS: {status[\"status\"]}')
    print(f'   🔑 Active tokens: {status[\"active_tokens\"]}')
    print(f'   🔒 Active partitions: {status[\"active_partitions\"]}')
    print(f'   📝 Command history: {status[\"command_history_entries\"]}')
except Exception as e:
    print(f'   ❌ SAIOS error: {e}')
"
        
        # OMEGA status
        echo ""
        echo "🛡️ OMEGA OPERATIONAL STATUS:"
        python3 -c "
try:
    components = []
    
    # Threat Modeler
    try:
        from omega_threat_modeler import ThreatModeler
        tm = ThreatModeler()
        components.append(f'Threat Modeler: {len(tm.models)} models')
    except:
        components.append('Threat Modeler: Not available')
    
    # Purple Team
    try:
        from omega_purple_team import PurpleTeamManager
        pt = PurpleTeamManager()
        components.append(f'Purple Team: {len(pt.exercises)} exercises')
    except:
        components.append('Purple Team: Not available')
    
    # LotL Simulator
    try:
        from omega_lotl_simulator import LotLSimulator
        ls = LotLSimulator()
        components.append(f'LotL Simulator: {len(ls.simulations)} simulations')
    except:
        components.append('LotL Simulator: Not available')
    
    for comp in components:
        print(f'   • {comp}')
        
except Exception as e:
    print(f'   ❌ OMEGA error: {e}')
"
        
        # Context status
        echo ""
        echo "📋 CONTEXT SYSTEM:"
        if [ -f JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md ]; then
            LINES=$(wc -l < JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md)
            AGE=$(stat -c %y JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md 2>/dev/null | cut -d' ' -f1)
            CONTEXT_ID=$(grep -m1 "CONTEXT ID:" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md | cut -d: -f2- | tr -d ' ')
            echo "   ✅ Context file: $LINES lines"
            echo "   📅 Last updated: $AGE"
            echo "   🆔 Context ID: $CONTEXT_ID"
        else
            echo "   ❌ Context file missing"
        fi
        ;;
        
    "test")
        print_header
        echo ""
        echo "🧪 RUNNING COMPREHENSIVE TESTS..."
        echo ""
        
        python3 test_all_components.py
        
        # Update context after tests
        echo ""
        echo "🔄 Updating context with test results..."
        ./JAIDA_CONTEXT_SYSTEM.sh update
        ;;
        
    "context")
        case "$2" in
            "update")
                echo "🔄 Updating context..."
                ./JAIDA_CONTEXT_SYSTEM.sh update
                ;;
            "recall")
                echo "📋 Recalling context..."
                ./JAIDA_CONTEXT_SYSTEM.sh recall
                ;;
            *)
                echo "Context Management:"
                echo "  ./omega_master_control.sh context update  - Update context"
                echo "  ./omega_master_control.sh context recall  - Display context"
                ;;
        esac
        ;;
        
    "deploy")
        FLEET_NAME="${2:-'Quick Response Fleet'}"
        WORKERS="${3:-3}"
        
        print_header
        echo ""
        echo "🤖 DEPLOYING NEW BOT FLEET..."
        echo ""
        
        python3 -c "
from sovereign_hierarchy import BotFather
bf = BotFather()
fleet = bf.deploy_fleet('$FLEET_NAME', num_workers=$WORKERS)
status = bf.get_system_status()
print(f'🚀 Fleet Deployment Complete!')
print(f'')
print(f'📋 Fleet Details:')
print(f'   Name: {fleet[\"gc_name\"]}')
print(f'   ID: {fleet[\"fleet_id\"]}')
print(f'   Worker Drones: {fleet[\"worker_count\"]}')
print(f'   GC Bot ID: {fleet[\"gc_id\"]}')
print(f'')
print(f'📊 Updated System Status:')
print(f'   Total Bots: {status[\"total_bots\"]}')
print(f'   Active Fleets: {status[\"fleet_count\"]}')
print(f'   Worker Drones: {status[\"worker_drones\"]}')
print(f'   General Contractors: {status[\"general_contractors\"]}')
"
        
        # Update context
        echo ""
        echo "🔄 Updating context with new fleet..."
        ./JAIDA_CONTEXT_SYSTEM.sh update
        ;;
        
    "threat-model")
        print_omega_header
        echo ""
        echo "🎯 CREATING THREAT MODEL..."
        echo ""
        
        MODEL_NAME="${2:-'Security Assessment'}"
        
        python3 -c "
from omega_threat_modeler import ThreatModeler
tm = ThreatModeler()
model = tm.create_model('$MODEL_NAME', template='web_application')
analysis = tm.analyze_model(model.model_id)
report = analysis['report']

print(f'✅ Threat Model Created!')
print(f'')
print(f'📋 Model Details:')
print(f'   Name: {model.name}')
print(f'   ID: {model.model_id}')
print(f'   Assets: {report[\"attack_surface\"][\"total_assets\"]}')
print(f'   Threats: {report[\"attack_surface\"][\"total_threats\"]}')
print(f'   Overall Risk: {report[\"summary\"][\"overall_risk\"]}')
print(f'   Risk Level: {report[\"summary\"][\"risk_level\"]}')
print(f'')
print(f'🎯 Top Recommendations:')
for i, rec in enumerate(report['summary']['recommendations'][:3], 1):
    print(f'   {i}. {rec}')
"
        ;;
        
    "purple-exercise")
        print_omega_header
        echo ""
        echo "🟣🟦 RUNNING PURPLE TEAM EXERCISE..."
        echo ""
        
        EXERCISE_NAME="${2:-'Security Exercise'}"
        SCENARIO="${3:-'phishing_campaign'}"
        
        python3 -c "
from omega_purple_team import PurpleTeamManager
pt = PurpleTeamManager()
exercise = pt.create_exercise('$EXERCISE_NAME', scenario_key='$SCENARIO')
simulation = pt.run_exercise_simulation(exercise.exercise_id)
report = simulation['report']

print(f'✅ Purple Team Exercise Complete!')
print(f'')
print(f'📋 Exercise Details:')
print(f'   Name: {exercise.name}')
print(f'   Duration: {report[\"duration_hours\"]} hours')
print(f'   Red Team Actions: {report[\"metrics\"][\"team_metrics\"][\"red_team_actions\"]}')
print(f'   Blue Team Actions: {report[\"metrics\"][\"team_metrics\"][\"blue_team_actions\"]}')
print(f'   Detection Rate: {report[\"metrics\"][\"defense_metrics\"][\"detection_rate_percent\"]}%')
print(f'   Findings: {report[\"metrics\"][\"findings_metrics\"][\"total_findings\"]}')
print(f'')
print(f'🎯 Lessons Learned:')
for i, lesson in enumerate(report['lessons_learned'][:3], 1):
    print(f'   {i}. {lesson}')
"
        ;;
        
    "lotl-sim")
        print_omega_header
        echo ""
        echo "🛠️ RUNNING LOTL SIMULATION..."
        echo ""
        
        SIM_NAME="${2:-'LotL Attack Test'}"
        
        python3 -c "
from omega_lotl_simulator import LotLSimulator
ls = LotLSimulator()
sim = ls.create_simulation('$SIM_NAME', target_os='windows')
results = ls.run_standard_simulation(sim.simulation_id)
report = results['report']

print(f'✅ LotL Simulation Complete!')
print(f'')
print(f'📋 Simulation Details:')
print(f'   Name: {sim.name}')
print(f'   OS: {sim.target_os}')
print(f'   Total Commands: {report[\"metrics\"][\"total_commands\"]}')
print(f'   Successful: {report[\"metrics\"][\"successful_commands\"]}')
print(f'   Detected: {report[\"metrics\"][\"detected_commands\"]}')
print(f'   Stealth Score: {report[\"metrics\"][\"stealth_score\"]}')
print(f'   Stealth Level: {report[\"stealth_assessment\"][\"level\"]}')
print(f'')
print(f'🎯 Recommendations:')
for i, rec in enumerate(report['recommendations'][:3], 1):
    print(f'   {i}. {rec}')
"
        ;;
        
    "help"|"")
        print_header
        echo ""
        echo "🛠️ AVAILABLE COMMANDS:"
        echo ""
        echo "🚀 SYSTEM CONTROL:"
        echo "  ./omega_master_control.sh start      - Start integrated demo"
        echo "  ./omega_master_control.sh saios      - SAIOS foundation demo"
        echo "  ./omega_master_control.sh omega      - OMEGA operational demo"
        echo "  ./omega_master_control.sh status     - Check system status"
        echo "  ./omega_master_control.sh test       - Run comprehensive tests"
        echo ""
        echo "🤖 BOT MANAGEMENT:"
        echo "  ./omega_master_control.sh deploy [name] [workers]"
        echo "                                  - Deploy new bot fleet"
        echo ""
        echo "🛡️ OMEGA OPERATIONS:"
        echo "  ./omega_master_control.sh threat-model [name]"
        echo "                                  - Create threat model"
        echo "  ./omega_master_control.sh purple-exercise [name] [scenario]"
        echo "                                  - Run purple team exercise"
        echo "  ./omega_master_control.sh lotl-sim [name]"
        echo "                                  - Run LotL simulation"
        echo ""
        echo "🔐 SAIOS FOUNDATION:"
       
cat > omega_master_control.sh << 'EOF'
#!/bin/bash
# Omega Master Control - Unified control for JAIDA-OMEGA-SAIOS

VERSION="3.0.0"
SYSTEM_NAME="JAIDA-OMEGA-SAIOS"

print_header() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                $SYSTEM_NAME Control Panel                ║"
    echo "║                    Version $VERSION                       ║"
    echo "╚══════════════════════════════════════════════════════════╝"
}

print_saios_header() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                 SAIOS FOUNDATION LAYER                   ║"
    echo "║           Sovereign Authentic Intelligence OS            ║"
    echo "╚══════════════════════════════════════════════════════════╝"
}

print_omega_header() {
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                OMEGA OPERATIONAL LAYER                   ║"
    echo "║           Multi-faceted Enhanced Guardian Arch           ║"
    echo "╚══════════════════════════════════════════════════════════╝"
}

case "$1" in
    "start"|"demo")
        print_header
        echo ""
        echo "🚀 Starting Integrated Demo..."
        echo ""
        
        python3 integrated_demo.py
        
        echo ""
        echo "✅ System demo completed successfully!"
        echo ""
        echo "💡 Available commands:"
        echo "   ./omega_master_control.sh omega      - OMEGA operational demo"
        echo "   ./omega_master_control.sh saios      - SAIOS foundation demo"
        echo "   ./omega_master_control.sh status     - Check system status"
        echo "   ./omega_master_control.sh test       - Run all tests"
        echo "   ./omega_master_control.sh deploy     - Deploy new fleet"
        ;;
        
    "saios")
        print_saios_header
        echo ""
        echo "🚀 Starting SAIOS Foundation Demo..."
        echo ""
        
        python3 saios_integrated_demo.py
        
        echo ""
        echo "✅ SAIOS foundation demo completed!"
        echo ""
        echo "🔐 SOVEREIGN CAPABILITIES:"
        echo "   • JAI-LSD-25 Token Authentication"
        echo "   • Privilege-Based Command Execution"
        echo "   • GC Isolation Partitions"
        echo "   • Hardware-Level Execution"
        echo "   • Sovereign Mode (Unrestricted)"
        ;;
        
    "omega")
        print_omega_header
        echo ""
        echo "🚀 Starting OMEGA Operational Demo..."
        echo ""
        
        python3 omega_complete_demo.py
        
        echo ""
        echo "✅ OMEGA operational demo completed!"
        echo ""
        echo "🛡️ OMEGA COMPONENTS:"
        echo "   • Threat Modeler - Advanced threat modeling"
        echo "   • Purple Team - Red/Blue team simulation"
        echo "   • LotL Simulator - Living off the Land attacks"
        echo "   • SAIOS Integration - Automated response"
        ;;
        
    "status")
        print_header
        echo ""
        echo "📊 SYSTEM STATUS"
        echo "══════════════════════════════════════════════════════════"
        
        # Check all modules
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
        
        if python3 -c "from omega_threat_modeler import ThreatModeler" 2>/dev/null; then
            echo "   ✅ OMEGA Threat Modeler: Available"
        else
            echo "   ❌ OMEGA Threat Modeler: Missing"
        fi
        
        if python3 -c "from omega_purple_team import PurpleTeamManager" 2>/dev/null; then
            echo "   ✅ OMEGA Purple Team: Available"
        else
            echo "   ❌ OMEGA Purple Team: Missing"
        fi
        
        if python3 -c "from omega_lotl_simulator import LotLSimulator" 2>/dev/null; then
            echo "   ✅ OMEGA LotL Simulator: Available"
        else
            echo "   ❌ OMEGA LotL Simulator: Missing"
        fi
        
        # Test results
        echo ""
        echo "🧪 TEST RESULTS:"
        if ls omega_test_report_*.json 2>/dev/null | head -1 >/dev/null; then
            latest_report=$(ls -t omega_test_report_*.json | head -1)
            if [ -f "$latest_report" ]; then
                passed=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('passed_tests', 0))")
                total=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('total_tests', 0))")
                rate=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('success_rate', 0))")
                timestamp=$(python3 -c "import json; data=json.load(open('$latest_report')); print(data.get('timestamp', ''))")
                echo "   📅 Last test: $(echo $timestamp | cut -d'T' -f1)"
                echo "   ✅ Passed: $passed/$total tests ($(printf "%.1f" $rate)%)"
            fi
        else
            echo "   ⚠️ No test reports found"
        fi
        
        # SAIOS status
        echo ""
        echo "🔐 SAIOS FOUNDATION STATUS:"
        python3 -c "
try:
    from saios_foundation import SAIOS_Core
    saios = SAIOS_Core()
    status = saios.get_system_status()
    print(f'   ✅ SAIOS: {status[\"status\"]}')
    print(f'   🔑 Active tokens: {status[\"active_tokens\"]}')
    print(f'   🔒 Active partitions: {status[\"active_partitions\"]}')
    print(f'   📝 Command history: {status[\"command_history_entries\"]}')
except Exception as e:
    print(f'   ❌ SAIOS error: {e}')
"
        
        # OMEGA status
        echo ""
        echo "🛡️ OMEGA OPERATIONAL STATUS:"
        python3 -c "
try:
    components = []
    
    # Threat Modeler
    try:
        from omega_threat_modeler import ThreatModeler
        tm = ThreatModeler()
        components.append(f'Threat Modeler: {len(tm.models)} models')
    except:
        components.append('Threat Modeler: Not available')
    
    # Purple Team
    try:
        from omega_purple_team import PurpleTeamManager
        pt = PurpleTeamManager()
        components.append(f'Purple Team: {len(pt.exercises)} exercises')
    except:
        components.append('Purple Team: Not available')
    
    # LotL Simulator
    try:
        from omega_lotl_simulator import LotLSimulator
        ls = LotLSimulator()
        components.append(f'LotL Simulator: {len(ls.simulations)} simulations')
    except:
        components.append('LotL Simulator: Not available')
    
    for comp in components:
        print(f'   • {comp}')
        
except Exception as e:
    print(f'   ❌ OMEGA error: {e}')
"
        
        # Context status
        echo ""
        echo "📋 CONTEXT SYSTEM:"
        if [ -f JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md ]; then
            LINES=$(wc -l < JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md)
            AGE=$(stat -c %y JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md 2>/dev/null | cut -d' ' -f1)
            CONTEXT_ID=$(grep -m1 "CONTEXT ID:" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md | cut -d: -f2- | tr -d ' ')
            echo "   ✅ Context file: $LINES lines"
            echo "   📅 Last updated: $AGE"
            echo "   🆔 Context ID: $CONTEXT_ID"
        else
            echo "   ❌ Context file missing"
        fi
        ;;
        
    "test")
        print_header
        echo ""
        echo "🧪 RUNNING COMPREHENSIVE TESTS..."
        echo ""
        
        python3 test_all_components.py
        
        # Update context after tests
        echo ""
        echo "🔄 Updating context with test results..."
        ./JAIDA_CONTEXT_SYSTEM.sh update
        ;;
        
    "context")
        case "$2" in
            "update")
                echo "🔄 Updating context..."
                ./JAIDA_CONTEXT_SYSTEM.sh update
                ;;
            "recall")
                echo "📋 Recalling context..."
                ./JAIDA_CONTEXT_SYSTEM.sh recall
                ;;
            *)
                echo "Context Management:"
                echo "  ./omega_master_control.sh context update  - Update context"
                echo "  ./omega_master_control.sh context recall  - Display context"
                ;;
        esac
        ;;
        
    "deploy")
        FLEET_NAME="${2:-'Quick Response Fleet'}"
        WORKERS="${3:-3}"
        
        print_header
        echo ""
        echo "🤖 DEPLOYING NEW BOT FLEET..."
        echo ""
        
        python3 -c "
from sovereign_hierarchy import BotFather
bf = BotFather()
fleet = bf.deploy_fleet('$FLEET_NAME', num_workers=$WORKERS)
status = bf.get_system_status()
print(f'🚀 Fleet Deployment Complete!')
print(f'')
print(f'📋 Fleet Details:')
print(f'   Name: {fleet[\"gc_name\"]}')
print(f'   ID: {fleet[\"fleet_id\"]}')
print(f'   Worker Drones: {fleet[\"worker_count\"]}')
print(f'   GC Bot ID: {fleet[\"gc_id\"]}')
print(f'')
print(f'📊 Updated System Status:')
print(f'   Total Bots: {status[\"total_bots\"]}')
print(f'   Active Fleets: {status[\"fleet_count\"]}')
print(f'   Worker Drones: {status[\"worker_drones\"]}')
print(f'   General Contractors: {status[\"general_contractors\"]}')
"
        
        # Update context
        echo ""
        echo "🔄 Updating context with new fleet..."
        ./JAIDA_CONTEXT_SYSTEM.sh update
        ;;
        
    "threat-model")
        print_omega_header
        echo ""
        echo "🎯 CREATING THREAT MODEL..."
        echo ""
        
        MODEL_NAME="${2:-'Security Assessment'}"
        
        python3 -c "
from omega_threat_modeler import ThreatModeler
tm = ThreatModeler()
model = tm.create_model('$MODEL_NAME', template='web_application')
analysis = tm.analyze_model(model.model_id)
report = analysis['report']

print(f'✅ Threat Model Created!')
print(f'')
print(f'📋 Model Details:')
print(f'   Name: {model.name}')
print(f'   ID: {model.model_id}')
print(f'   Assets: {report[\"attack_surface\"][\"total_assets\"]}')
print(f'   Threats: {report[\"attack_surface\"][\"total_threats\"]}')
print(f'   Overall Risk: {report[\"summary\"][\"overall_risk\"]}')
print(f'   Risk Level: {report[\"summary\"][\"risk_level\"]}')
print(f'')
print(f'🎯 Top Recommendations:')
for i, rec in enumerate(report['summary']['recommendations'][:3], 1):
    print(f'   {i}. {rec}')
"
        ;;
        
    "purple-exercise")
        print_omega_header
        echo ""
        echo "🟣🟦 RUNNING PURPLE TEAM EXERCISE..."
        echo ""
        
        EXERCISE_NAME="${2:-'Security Exercise'}"
        SCENARIO="${3:-'phishing_campaign'}"
        
        python3 -c "
from omega_purple_team import PurpleTeamManager
pt = PurpleTeamManager()
exercise = pt.create_exercise('$EXERCISE_NAME', scenario_key='$SCENARIO')
simulation = pt.run_exercise_simulation(exercise.exercise_id)
report = simulation['report']

print(f'✅ Purple Team Exercise Complete!')
print(f'')
print(f'📋 Exercise Details:')
print(f'   Name: {exercise.name}')
print(f'   Duration: {report[\"duration_hours\"]} hours')
print(f'   Red Team Actions: {report[\"metrics\"][\"team_metrics\"][\"red_team_actions\"]}')
print(f'   Blue Team Actions: {report[\"metrics\"][\"team_metrics\"][\"blue_team_actions\"]}')
print(f'   Detection Rate: {report[\"metrics\"][\"defense_metrics\"][\"detection_rate_percent\"]}%')
print(f'   Findings: {report[\"metrics\"][\"findings_metrics\"][\"total_findings\"]}')
print(f'')
print(f'🎯 Lessons Learned:')
for i, lesson in enumerate(report['lessons_learned'][:3], 1):
    print(f'   {i}. {lesson}')
"
        ;;
        
    "lotl-sim")
        print_omega_header
        echo ""
        echo "🛠️ RUNNING LOTL SIMULATION..."
        echo ""
        
        SIM_NAME="${2:-'LotL Attack Test'}"
        
        python3 -c "
from omega_lotl_simulator import LotLSimulator
ls = LotLSimulator()
sim = ls.create_simulation('$SIM_NAME', target_os='windows')
results = ls.run_standard_simulation(sim.simulation_id)
report = results['report']

print(f'✅ LotL Simulation Complete!')
print(f'')
print(f'📋 Simulation Details:')
print(f'   Name: {sim.name}')
print(f'   OS: {sim.target_os}')
print(f'   Total Commands: {report[\"metrics\"][\"total_commands\"]}')
print(f'   Successful: {report[\"metrics\"][\"successful_commands\"]}')
print(f'   Detected: {report[\"metrics\"][\"detected_commands\"]}')
print(f'   Stealth Score: {report[\"metrics\"][\"stealth_score\"]}')
print(f'   Stealth Level: {report[\"stealth_assessment\"][\"level\"]}')
print(f'')
print(f'🎯 Recommendations:')
for i, rec in enumerate(report['recommendations'][:3], 1):
    print(f'   {i}. {rec}')
"
        ;;
        
    "help"|"")
        print_header
        echo ""
        echo "🛠️ AVAILABLE COMMANDS:"
        echo ""
        echo "🚀 SYSTEM CONTROL:"
        echo "  ./omega_master_control.sh start      - Start integrated demo"
        echo "  ./omega_master_control.sh saios      - SAIOS foundation demo"
        echo "  ./omega_master_control.sh omega      - OMEGA operational demo"
        echo "  ./omega_master_control.sh status     - Check system status"
        echo "  ./omega_master_control.sh test       - Run comprehensive tests"
        echo ""
        echo "🤖 BOT MANAGEMENT:"
        echo "  ./omega_master_control.sh deploy [name] [workers]"
        echo "                                  - Deploy new bot fleet"
        echo ""
        echo "🛡️ OMEGA OPERATIONS:"
        echo "  ./omega_master_control.sh threat-model [name]"
        echo "                                  - Create threat model"
        echo "  ./omega_master_control.sh purple-exercise [name] [scenario]"
        echo "                                  - Run purple team exercise"
        echo "  ./omega_master_control.sh lotl-sim [name]"
        echo "                                  - Run LotL simulation"
        echo ""
        echo "🔐 SAIOS FOUNDATION:"
        echo "  ./omega_master_control.sh context update  - Update context"
        echo "  ./omega_master_control.sh context recall  - Display context"
        echo ""
        echo "🔧 MAINTENANCE:"
        echo "  ./omega_master_control.sh help       - Show this help"
        echo ""
        echo "📚 QUICK EXAMPLES:"
        echo "  Run complete OMEGA demo:"
        echo "    ./omega_master_control.sh omega"
        echo ""
        echo "  Create threat model:"
        echo "    ./omega_master_control.sh threat-model \"Web App Security\""
        echo ""
        echo "  Run purple team exercise:"
        echo "    ./omega_master_control.sh purple-exercise \"APT Simulation\" ransomware_attack"
        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║        JAIDA-OMEGA-SAIOS: Complete Sovereign AI         ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        ;;
        
    *)
        echo "❌ Unknown command: $1"
        echo "💡 Try: ./omega_master_control.sh help"
        ;;
esac
