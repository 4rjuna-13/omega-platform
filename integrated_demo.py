#!/usr/bin/env python3
"""
Integrated Demo - JAIDA-OMEGA-SAIOS Full System
Shows how all components work together
"""

import json
from datetime import datetime

print("="*60)
print("🤖 JAIDA-OMEGA-SAIOS INTEGRATED DEMO")
print("="*60)

print("\n1. 📊 INITIALIZING THREAT INTELLIGENCE DASHBOARD...")
from simple_threat_dashboard import SimpleDashboard, DataSource, ThreatSeverity

dashboard = SimpleDashboard("Integrated Demo Dashboard")
dashboard.add_sample_data()

# Add more threats
dashboard.add_indicator(
    "Lateral Movement",
    ThreatSeverity.HIGH,
    DataSource.PURPLE_TEAM,
    "Suspicious lateral movement detected",
    ["source_ip_10.0.0.5", "destination_ip_10.0.0.12"]
)

report = dashboard.generate_report()
print(f"   ✅ Dashboard operational")
print(f"   - Active threats: {report['summary']['active_indicators']}")
print(f"   - Total indicators: {report['summary']['total_indicators']}")

print("\n2. 🏢 INITIALIZING ENTERPRISE INTEGRATION...")
from enterprise_platform_simple import SimpleOrchestrator, SimpleIntegration, IntegrationType

orchestrator = SimpleOrchestrator("Demo Orchestrator")
siem = SimpleIntegration("Demo SIEM", IntegrationType.SIEM)
soar = SimpleIntegration("Demo SOAR", IntegrationType.SOAR)

siem.connect()
soar.connect()

orchestrator.add_integration(siem)
orchestrator.add_integration(soar)

print(f"   ✅ Enterprise integration operational")
print(f"   - Connected systems: {orchestrator.get_status()['connected_integrations']}")

print("\n3. 🤖 DEPLOYING SOVEREIGN HIERARCHY...")
from sovereign_hierarchy import BotFather, TaskPriority

bot_father = BotFather()

# Deploy multiple fleets for different purposes
threat_fleet = bot_father.deploy_fleet(
    "Threat Analysis Fleet",
    num_workers=3,
    worker_capabilities=[
        ["network_scan", "vulnerability_detection"],
        ["malware_analysis", "threat_hunting"],
        ["incident_response", "forensics"]
    ]
)

response_fleet = bot_father.deploy_fleet(
    "Incident Response Fleet", 
    num_workers=2,
    worker_capabilities=[
        ["containment", "eradication"],
        ["recovery", "lessons_learned"]
    ]
)

print(f"   ✅ Sovereign hierarchy deployed")
print(f"   - Total bots: {bot_father.get_system_status()['total_bots']}")
print(f"   - Fleets active: {bot_father.get_system_status()['fleet_count']}")

print("\n4. 🎯 EXECUTING INTEGRATED OPERATION...")
# Get the threat analysis GC
threat_gc = bot_father.get_bot(threat_fleet['gc_id'])

# Create tasks based on dashboard threats
for i, threat in enumerate(report['recent_indicators'][:2]):
    task = threat_gc.create_task(
        f"Analyze: {threat['type']}",
        "threat_analysis",
        TaskPriority.HIGH if threat['severity'] >= 3 else TaskPriority.MEDIUM,
        {
            "threat_type": threat['type'],
            "severity": threat['severity_label'],
            "description": threat['description'],
            "iocs": threat.get('iocs', [])
        }
    )
    print(f"   📋 Task created: {task['name']}")

# Deploy a comprehensive strategy
strategy = threat_gc.deploy_strategy(
    "Full Spectrum Threat Response",
    [
        "Collect threat intelligence from dashboard",
        "Analyze threats using specialized workers",
        "Coordinate with enterprise systems",
        "Execute containment if needed",
        "Generate comprehensive report"
    ]
)

print(f"   🎯 Strategy deployed: {strategy['name']}")
print(f"   - Objectives: {len(strategy['objectives'])}")

print("\n5. 📈 GENERATING INTEGRATED REPORT...")
final_report = {
    "timestamp": datetime.now().isoformat(),
    "system": "JAIDA-OMEGA-SAIOS Integrated Demo",
    "components": {
        "threat_dashboard": {
            "status": "operational",
            "indicators": report['summary']['total_indicators'],
            "active_threats": report['summary']['active_indicators']
        },
        "enterprise_integration": {
            "status": "operational",
            "integrations": orchestrator.get_status()['total_integrations'],
            "connected": orchestrator.get_status()['connected_integrations']
        },
        "sovereign_hierarchy": {
            "status": "operational",
            "total_bots": bot_father.get_system_status()['total_bots'],
            "worker_drones": bot_father.get_system_status()['worker_drones'],
            "general_contractors": bot_father.get_system_status()['general_contractors'],
            "active_strategies": 1
        }
    },
    "operation": {
        "tasks_created": threat_gc.task_queue.qsize(),
        "strategy": strategy['name'],
        "objectives": strategy['objectives']
    }
}

print(f"   ✅ Integrated report generated")
print(f"   - Total system components: 3")
print(f"   - Active bots: {final_report['components']['sovereign_hierarchy']['total_bots']}")
print(f"   - Pending tasks: {final_report['operation']['tasks_created']}")

print("\n" + "="*60)
print("🎉 INTEGRATED DEMO COMPLETE")
print("="*60)
print("\n🏛️ JAIDA-OMEGA-SAIOS Architecture:")
print("   📊 Threat Dashboard → 🏢 Enterprise Integration → 🤖 Sovereign Hierarchy")
print("\n🚀 System is ready for autonomous operations")
print("💡 Each component can now work together seamlessly")

# Save the report
filename = f"integrated_demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, 'w') as f:
    json.dump(final_report, f, indent=2)

print(f"\n💾 Full report saved to: {filename}")
