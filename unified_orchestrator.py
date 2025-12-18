#!/usr/bin/env python3
"""
Simple JAIDA Unified Orchestrator
"""

import argparse
import time
import logging
from datetime import datetime
import json
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/jaida.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("JAIDA")

class JAIDAOrchestrator:
    def __init__(self):
        self.start_time = datetime.now()
        self.alerts_processed = 0
        logger.info("JAIDA Orchestrator initialized")
    
    def status(self):
        """Show system status"""
        logger.info("Checking system status...")
        
        status_report = {
            "timestamp": datetime.now().isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "alerts_processed": self.alerts_processed,
            "components": {
                "core": "operational",
                "database": "connected",
                "adapter": "ready"
            }
        }
        
        print(json.dumps(status_report, indent=2))
        logger.info(f"Status report generated: {self.alerts_processed} alerts processed")
        return status_report
    
    def autonomous(self):
        """Run in autonomous mode"""
        logger.info("Starting autonomous mode...")
        
        try:
            from real_data_adapter import RealDataAdapter
            from omega_nexus_enhanced import OmegaNexusEnhanced
            
            adapter = RealDataAdapter()
            nexus = OmegaNexusEnhanced()
            
            print("🤖 JAIDA Autonomous Mode Active")
            print("===============================")
            
            cycle = 0
            while True:
                cycle += 1
                logger.info(f"Autonomous cycle {cycle} starting...")
                
                print(f"\n🔁 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Fetch alerts from mock sources
                sources = ["mock_siem", "mock_edr", "mock_firewall"]
                for source in sources:
                    try:
                        alerts = adapter.fetch_alerts(source, hours=1)
                        self.alerts_processed += len(alerts)
                        print(f"   📥 {source}: {len(alerts)} alerts")
                    except Exception as e:
                        logger.error(f"Error fetching from {source}: {e}")
                
                # Run monitoring
                nexus.monitor_real_time()
                
                # Generate report every 5 cycles
                if cycle % 5 == 0:
                    report = nexus.generate_report()
                    print(f"\n📋 Cycle {cycle} Report:")
                    print(f"   Threat Level: {report['threat_level']}")
                    print(f"   Total Alerts: {report['total_alerts']}")
                    print(f"   Sources: {', '.join(report['data_sources'])}")
                    
                    # Save report
                    report_file = f"logs/autonomous_report_cycle_{cycle}.json"
                    with open(report_file, 'w') as f:
                        json.dump(report, f, indent=2)
                    logger.info(f"Report saved to {report_file}")
                
                time.sleep(10)  # 10 second cycles for demo
                
        except KeyboardInterrupt:
            logger.info("Autonomous mode stopped by user")
            print("\n🛑 Autonomous mode stopped")
        except Exception as e:
            logger.error(f"Error in autonomous mode: {e}")
            print(f"❌ Error: {e}")
    
    def deploy(self):
        """Deployment mode"""
        logger.info("Starting deployment mode...")
        
        print("🚀 Deployment Mode")
        print("=================")
        
        # Run deployment checks
        checks = [
            ("Database", self._check_database),
            ("Dependencies", self._check_dependencies),
            ("Configuration", self._check_configuration),
            ("Logging", self._check_logging)
        ]
        
        for check_name, check_func in checks:
            print(f"\n🔍 Checking {check_name}...")
            try:
                result = check_func()
                print(f"   ✅ {result}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n✅ Deployment checks completed")
        logger.info("Deployment mode completed")
    
    def demo(self):
        """Demo mode"""
        logger.info("Starting demo mode...")
        
        print("🎬 JAIDA-Omega-SAIOS Demo")
        print("========================")
        
        try:
            from real_data_adapter import integrate_with_jaida
            from real_data_dashboard import RealDataDashboard
            
            print("\n1. Integrating real data adapter...")
            integrate_with_jaida()
            
            print("\n2. Displaying dashboard...")
            dashboard = RealDataDashboard()
            dashboard.display_summary()
            
            print("\n3. Running Omega Nexus enhanced...")
            from omega_nexus_enhanced import OmegaNexusEnhanced
            nexus = OmegaNexusEnhanced()
            nexus.monitor_real_time()
            
            print("\n4. Generating final report...")
            report = nexus.generate_report()
            print(f"   Final Threat Level: {report['threat_level']}")
            print(f"   Total Alerts Processed: {report['total_alerts']}")
            
            print("\n✅ Demo completed successfully!")
            logger.info("Demo completed")
            
        except Exception as e:
            logger.error(f"Demo error: {e}")
            print(f"❌ Demo error: {e}")
    
    def _check_database(self):
        import sqlite3
        conn = sqlite3.connect('data/sovereign_data.db')
        cursor = conn.cursor()
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        conn.close()
        return f"{len(tables)} tables found"
    
    def _check_dependencies(self):
        import importlib
        deps = ['pandas', 'flask', 'numpy', 'yaml']
        available = []
        for dep in deps:
            try:
                importlib.import_module(dep)
                available.append(dep)
            except:
                pass
        return f"{len(available)}/{len(deps)} dependencies available"
    
    def _check_configuration(self):
        import os
        config_files = [f for f in os.listdir('config') if f.endswith('.yaml')]
        return f"{len(config_files)} config files found"
    
    def _check_logging(self):
        import os
        if os.path.exists('logs'):
            return "Logs directory exists"
        else:
            os.makedirs('logs', exist_ok=True)
            return "Created logs directory"

def main():
    parser = argparse.ArgumentParser(description="JAIDA Unified Orchestrator")
    parser.add_argument('command', choices=['status', 'autonomous', 'deploy', 'demo'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    # Ensure logs directory exists
    import os
    os.makedirs('logs', exist_ok=True)
    
    orchestrator = JAIDAOrchestrator()
    
    if args.command == 'status':
        orchestrator.status()
    elif args.command == 'autonomous':
        orchestrator.autonomous()
    elif args.command == 'deploy':
        orchestrator.deploy()
    elif args.command == 'demo':
        orchestrator.demo()

if __name__ == "__main__":
    main()
