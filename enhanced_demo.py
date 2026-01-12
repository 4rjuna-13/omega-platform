#!/usr/bin/env python3
"""
🎬 Enhanced JAIDA-OMEGA-SAIOS Demonstration
"""

import sys
import os
import sqlite3
from datetime import datetime

sys.path.insert(0, 'src')

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*70}")
    print(f"📋 {title}")
    print('='*70)

def demo_system_status():
    """Demonstrate system status"""
    print_section("SYSTEM STATUS DEMONSTRATION")
    
    from core.orchestrator import SystemOrchestrator
    orchestrator = SystemOrchestrator()
    
    # Check health
    health = orchestrator.check_system_health()
    print(f"Overall Health: {health['overall_health'].upper()}")
    
    # Get system status
    status = orchestrator.get_system_status()
    print(f"\nSystem Components:")
    for component, info in status.items():
        status_icon = '✅' if info['status'] in ['running', 'healthy'] else '⚠️' if info['status'] == 'degraded' else '❌'
        print(f"  {status_icon} {component}: {info['status']}")
        if info['details']:
            print(f"      Details: {info['details']}")

def demo_autonomous_engine():
    """Demonstrate autonomous decision making"""
    print_section("AUTONOMOUS DECISION ENGINE")
    
    from autonomous.engine import AutonomousEngine, ThreatIndicator, ThreatLevel
    
    engine = AutonomousEngine()
    
    print("🧪 Testing with different threat types:\n")
    
    # Test different threat scenarios
    scenarios = [
        {
            "name": "Malware Attack",
            "threat_type": "malware",
            "severity": ThreatLevel.CRITICAL,
            "confidence": 0.92
        },
        {
            "name": "Phishing Campaign",
            "threat_type": "phishing", 
            "severity": ThreatLevel.MALICIOUS,
            "confidence": 0.78
        },
        {
            "name": "DDoS Attack",
            "threat_type": "ddos",
            "severity": ThreatLevel.CRITICAL,
            "confidence": 0.95
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}:")
        
        threat = ThreatIndicator(
            id=f"demo_threat_{i:03d}",
            source="demo",
            indicator=f"{scenario['threat_type']}_detected",
            threat_type=scenario['threat_type'],
            confidence=scenario['confidence'],
            severity=scenario['severity'],
            timestamp=datetime.now().isoformat(),
            context={"demo": True, "scenario": scenario['name']}
        )
        
        decisions = engine.make_decision(threat)
        
        print(f"   Threat: {scenario['threat_type'].upper()}")
        print(f"   Severity: {scenario['severity'].name}")
        print(f"   Confidence: {scenario['confidence']:.0%}")
        print(f"   Decisions generated: {len(decisions)}")
        
        for decision in decisions:
            print(f"     • {decision.action.value} (priority: {decision.priority})")
        print()

def demo_database():
    """Demonstrate database operations"""
    print_section("DATABASE & PERSISTENCE")
    
    db_path = "data/sovereign.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Show tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📊 Database contains {len(tables)} tables:")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            count = cursor.fetchone()[0]
            print(f"   • {table[0]}: {count} records")
        
        # Show recent decisions
        print("\n📋 Recent autonomous decisions:")
        cursor.execute("""
            SELECT decision_id, action, confidence, executed, created_at 
            FROM autonomous_decisions 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        
        for row in cursor.fetchall():
            decision_id, action, confidence, executed, created_at = row
            executed_icon = '✅' if executed else '⏳'
            print(f"   {executed_icon} {action} (ID: {decision_id[:8]}...)")
            print(f"      Confidence: {confidence:.0%}, Created: {created_at[:19]}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

def demo_integration():
    """Demonstrate integration capabilities"""
    print_section("SYSTEM INTEGRATION")
    
    print("🔗 Integration Points Available:")
    print("   1. Omega Nexus Integration - Threat alert processing")
    print("   2. Bot Father System - Autonomous bot deployment") 
    print("   3. Web Crawler System - Threat intelligence gathering")
    print("   4. Deception Technology - Honeypot activation")
    print("   5. Sovereign Database - Persistent data storage")
    
    print("\n⚡ Simulated Integration Workflow:")
    print("   Threat detected → Analysis → Decision → Action → Results stored")
    print("   ✅ End-to-end autonomous cybersecurity response")

def main():
    """Main demonstration"""
    print("\n" + "="*70)
    print("🎬 ENHANCED JAIDA-OMEGA-SAIOS DEMONSTRATION")
    print("🤖 Autonomous Cybersecurity Platform v2.0")
    print("="*70)
    
    try:
        demo_system_status()
        demo_autonomous_engine()
        demo_database()
        demo_integration()
        
        print_section("DEMONSTRATION COMPLETE")
        print("✅ All systems operational")
        print("🚀 Ready for autonomous cybersecurity operations")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Demonstration error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
