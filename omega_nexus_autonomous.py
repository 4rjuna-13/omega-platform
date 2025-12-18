#!/usr/bin/env python3
"""
🏛️ OMEGA NEXUS AUTONOMOUS EDITION
Central orchestrator with integrated autonomous decision engine
"""

import sys
import json
import argparse
import logging
from datetime import datetime
from integrate_autonomous_engine import OmegaAutonomousIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OmegaNexusAutonomous:
    """Omega Nexus with autonomous capabilities"""
    
    def __init__(self):
        self.integration = OmegaAutonomousIntegration()
        self.system_status = self._load_system_status()
        logger.info("🚀 Omega Nexus Autonomous Edition initialized")
    
    def _load_system_status(self):
        """Load current system status"""
        return {
            "version": "2.1-autonomous",
            "status": "operational",
            "last_updated": datetime.now().isoformat(),
            "components": {
                "autonomous_engine": "active",
                "decision_executor": "active",
                "integration_layer": "active"
            }
        }
    
    def status(self):
        """Display system status"""
        status = self.integration.get_system_status()
        
        print("\n" + "=" * 70)
        print("🏛️ OMEGA NEXUS AUTONOMOUS EDITION - SYSTEM STATUS")
        print("=" * 70)
        
        print(f"\n📊 Autonomous Engine Status:")
        print(f"  Status: {status['autonomous_engine']}")
        print(f"  Pending Decisions: {status['pending_decisions']}")
        print(f"  Total Decisions: {status['total_decisions']}")
        print(f"  Success Rate: {status['success_rate']}%")
        print(f"  Average Confidence: {status['average_confidence']}%")
        
        if status['last_cycle']:
            print(f"\n🔄 Last Autonomous Cycle:")
            print(f"  Cycle ID: {status['last_cycle']['cycle_id']}")
            print(f"  Duration: {status['last_cycle']['duration_seconds']:.2f}s")
            print(f"  Decisions Executed: {status['last_cycle']['decisions_executed']}")
        
        print(f"\n🤖 System Components:")
        for component, state in self.system_status['components'].items():
            print(f"  • {component}: {state}")
        
        print(f"\n⏰ Last Updated: {self.system_status['last_updated']}")
        print("=" * 70)
        
        return status
    
    def autonomous(self, cycles: int = 1):
        """Run autonomous decision cycles"""
        print(f"\n🔄 Running {cycles} autonomous cycle(s)...")
        
        reports = []
        for i in range(cycles):
            print(f"\nCycle {i+1}/{cycles}:")
            report = self.integration.execute_autonomous_cycle()
            reports.append(report)
            
            print(f"  ✓ Generated: {report['decisions_generated']} decisions")
            print(f"  ✓ Executed: {report['decisions_executed']} actions")
            print(f"  ✓ Duration: {report['duration_seconds']:.2f}s")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 AUTONOMOUS CYCLES SUMMARY")
        print("=" * 70)
        
        total_decisions = sum(r['decisions_executed'] for r in reports)
        total_duration = sum(r['duration_seconds'] for r in reports)
        
        print(f"\nTotal Cycles: {len(reports)}")
        print(f"Total Decisions Executed: {total_decisions}")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"Average per Cycle: {total_duration/len(reports):.2f}s")
        
        # Save report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "cycles": cycles,
            "reports": reports,
            "summary": {
                "total_decisions": total_decisions,
                "total_duration": total_duration
            }
        }
        
        with open("autonomous_cycles_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Report saved: autonomous_cycles_report.json")
        print("=" * 70)
        
        return reports
    
    def analyze(self, threat_data: dict):
        """Analyze threat data and show what decisions would be made"""
        print("\n🔍 Threat Analysis Mode")
        print("=" * 70)
        
        try:
            # Convert threat data
            from autonomous_decision_engine import ThreatIndicator, ThreatLevel
            
            # Map severity string to enum
            severity_map = {
                "low": ThreatLevel.SUSPICIOUS,
                "medium": ThreatLevel.MALICIOUS,
                "high": ThreatLevel.CRITICAL,
                "critical": ThreatLevel.CRITICAL
            }
            
            threat = ThreatIndicator(
                id=threat_data.get('id', ''),
                source=threat_data.get('source', 'manual'),
                indicator=threat_data.get('indicator', 'unknown'),
                threat_type=threat_data.get('threat_type', 'unknown'),
                confidence=threat_data.get('confidence', 0.5),
                severity=severity_map.get(threat_data.get('severity', 'medium'), ThreatLevel.MALICIOUS),
                timestamp=threat_data.get('timestamp', datetime.now().isoformat()),
                context=threat_data.get('context', {})
            )
            
            # Analyze
            engine = self.integration.engine
            analysis = engine.analyze_threat(threat)
            
            print(f"\n📊 Threat Analysis Results:")
            print(f"  Threat Score: {analysis['threat_score']}/100")
            print(f"  Response Level: {analysis['response_level']}")
            print(f"  Confidence: {analysis['confidence']:.2%}")
            
            # Show what decisions would be made
            decisions = engine.make_decision(threat)
            
            print(f"\n🤖 Autonomous Decisions that would be made:")
            for i, decision in enumerate(decisions, 1):
                print(f"\n  {i}. {decision.action.value}")
                print(f"     Priority: {decision.priority}")
                print(f"     Reason: {decision.reason}")
                print(f"     Confidence: {decision.confidence:.2%}")
                print(f"     Expected: {decision.expected_outcome}")
                
                if decision.parameters:
                    print(f"     Parameters: {json.dumps(decision.parameters, indent=4)}")
            
            print("\n" + "=" * 70)
            
            return {
                "analysis": analysis,
                "decisions": [d.to_dict() for d in decisions]
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return {"error": str(e)}
    
    def monitor(self, interval: int = 60):
        """Continuous monitoring with autonomous response"""
        import time
        
        print(f"\n👁️  Starting Autonomous Monitor (interval: {interval}s)")
        print("=" * 70)
        print("Press Ctrl+C to stop monitoring")
        
        cycle_count = 0
        
        try:
            while True:
                cycle_count += 1
                print(f"\n🔄 Monitor Cycle #{cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Run autonomous cycle
                report = self.integration.execute_autonomous_cycle()
                
                if report['decisions_executed'] > 0:
                    print(f"  ⚡ Autonomous actions taken: {report['decisions_executed']}")
                
                # Show status
                status = self.integration.get_system_status()
                print(f"  📊 Status: {status['pending_decisions']} pending decisions")
                
                # Wait for next cycle
                if cycle_count < 10:  # Only show countdown for first 10 cycles
                    print(f"  ⏰ Next cycle in {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")
            print(f"Total cycles: {cycle_count}")
            print("=" * 70)
    
    def demo(self):
        """Run a demonstration of autonomous capabilities"""
        print("\n🎬 AUTONOMOUS CAPABILITIES DEMONSTRATION")
        print("=" * 70)
        
        # Generate sample alerts
        print("\n1️⃣  Generating sample threat alerts...")
        alerts = self.integration.generate_sample_alerts()
        print(f"   ✓ Generated {len(alerts)} sample alerts")
        
        # Show what would happen with each alert
        print("\n2️⃣  Threat analysis simulation:")
        for i, alert in enumerate(alerts, 1):
            print(f"\n   Alert {i}: {alert['type']} ({alert['severity']} severity)")
            result = self.analyze(alert)
            if 'decisions' in result:
                print(f"   → {len(result['decisions'])} autonomous decisions generated")
        
        # Run actual autonomous cycle
        print("\n3️⃣  Executing autonomous decision cycle...")
        report = self.integration.execute_autonomous_cycle()
        print(f"   ✓ Cycle completed in {report['duration_seconds']:.2f}s")
        print(f"   ✓ {report['decisions_executed']} actions executed")
        
        # Show final status
        print("\n4️⃣  Final system status:")
        status = self.integration.get_system_status()
        print(f"   Success Rate: {status['success_rate']}%")
        print(f"   Average Confidence: {status['average_confidence']}%")
        
        print("\n🎉 Demonstration completed!")
        print("=" * 70)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Omega Nexus Autonomous Edition - Central orchestrator with AI-driven decision making",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'command',
        choices=['status', 'autonomous', 'analyze', 'monitor', 'demo', 'help'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--cycles', '-c',
        type=int,
        default=1,
        help='Number of autonomous cycles to run (default: 1)'
    )
    
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=60,
        help='Monitoring interval in seconds (default: 60)'
    )
    
    parser.add_argument(
        '--threat-file', '-t',
        type=str,
        help='JSON file containing threat data for analysis'
    )
    
    args = parser.parse_args()
    
    nexus = OmegaNexusAutonomous()
    
    if args.command == 'status':
        nexus.status()
    
    elif args.command == 'autonomous':
        nexus.autonomous(cycles=args.cycles)
    
    elif args.command == 'analyze':
        if args.threat_file:
            try:
                with open(args.threat_file, 'r') as f:
                    threat_data = json.load(f)
                nexus.analyze(threat_data)
            except Exception as e:
                print(f"❌ Failed to load threat file: {e}")
        else:
            print("⚠️  Please provide a threat file with --threat-file")
    
    elif args.command == 'monitor':
        nexus.monitor(interval=args.interval)
    
    elif args.command == 'demo':
        nexus.demo()
    
    elif args.command == 'help':
        print("\n" + "=" * 70)
        print("🏛️ OMEGA NEXUS AUTONOMOUS EDITION - HELP")
        print("=" * 70)
        print("\nAvailable Commands:")
        print("  status      - Show system and autonomous engine status")
        print("  autonomous  - Run autonomous decision cycles")
        print("  analyze     - Analyze threat data from JSON file")
        print("  monitor     - Continuous monitoring with autonomous response")
        print("  demo        - Run a demonstration of autonomous capabilities")
        print("  help        - Show this help message")
        print("\nExamples:")
        print("  python3 omega_nexus_autonomous.py status")
        print("  python3 omega_nexus_autonomous.py autonomous --cycles 3")
        print("  python3 omega_nexus_autonomous.py analyze --threat-file threat.json")
        print("  python3 omega_nexus_autonomous.py monitor --interval 30")
        print("=" * 70)

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🏛️ JAIDA-OMEGA-SAIOS - OMEGA NEXUS AUTONOMOUS EDITION")
    print("🤖 AI-Driven Cybersecurity Decision Making")
    print("=" * 70)
    main()
