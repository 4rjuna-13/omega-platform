#!/usr/bin/env python3
"""
Omega Nexus Enhanced with Real Integration
Main orchestrator with full real-world integration capabilities
"""

import argparse
import sys
import time
import json
import yaml
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("OmegaNexusReal")

class OmegaNexusRealIntegration:
    """Omega Nexus with real integration capabilities"""
    
    def __init__(self):
        """Initialize enhanced Omega Nexus"""
        self.integration_manager = None
        self.operational_mode = "hybrid"  # autonomous, manual, hybrid
        self.system_status = "initialized"
        
        logger.info("Omega Nexus Real Integration initialized")
    
    def start_real_integration(self):
        """Start real integration pipeline"""
        try:
            from src.integration.real.integration_manager import RealIntegrationManager
            
            logger.info("🚀 Starting real integration pipeline...")
            
            self.integration_manager = RealIntegrationManager()
            
            if self.integration_manager.start():
                self.system_status = "integration_running"
                logger.info("✅ Real integration pipeline started")
                
                # Log startup information
                self._log_integration_startup()
                
                return True
            else:
                logger.error("❌ Failed to start integration pipeline")
                return False
                
        except ImportError as e:
            logger.error(f"Integration module not found: {e}")
            logger.info("Make sure real integration modules are in src/integration/real/")
            return False
        except Exception as e:
            logger.error(f"Error starting integration: {e}")
            return False
    
    def stop_real_integration(self):
        """Stop real integration pipeline"""
        if self.integration_manager:
            logger.info("🛑 Stopping real integration pipeline...")
            self.integration_manager.stop()
            self.system_status = "integration_stopped"
            logger.info("Real integration pipeline stopped")
    
    def set_operational_mode(self, mode: str):
        """Set operational mode"""
        valid_modes = ["autonomous", "manual", "hybrid"]
        if mode not in valid_modes:
            logger.error(f"Invalid mode: {mode}. Must be one of {valid_modes}")
            return False
        
        self.operational_mode = mode
        logger.info(f"Operational mode set to: {mode}")
        
        # Update configuration
        self._update_operational_config(mode)
        
        return True
    
    def get_system_status(self):
        """Get complete system status"""
        status = {
            "system": "Omega Nexus Real Integration",
            "version": "2.1",
            "status": self.system_status,
            "operational_mode": self.operational_mode,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.integration_manager:
            integration_status = self.integration_manager.get_status()
            status["integration"] = integration_status
        
        return status
    
    def run_demo(self, duration: int = 300):
        """Run complete demonstration"""
        print("\n" + "="*60)
        print("🚀 JAIDA-OMEGA-SAIOS REAL INTEGRATION DEMO")
        print("="*60)
        
        try:
            # Step 1: Start integration
            print("\n1️⃣ Starting real integration pipeline...")
            if not self.start_real_integration():
                print("❌ Failed to start integration")
                return
            
            # Step 2: Show status
            print("\n2️⃣ System Status:")
            status = self.get_system_status()
            print(json.dumps(status, indent=2))
            
            # Step 3: Run for duration
            print(f"\n3️⃣ Running real integration for {duration} seconds...")
            print("   Generating and processing real alerts...")
            print("   Alerts will be forwarded to autonomous engine...")
            print("   Check dashboard at http://localhost:8050 (if enabled)")
            
            # Monitor progress
            for i in range(duration // 10):
                if self.system_status != "integration_running":
                    break
                
                if self.integration_manager:
                    int_status = self.integration_manager.get_status()
                    alerts = int_status.get('statistics', {}).get('alerts_processed', 0)
                    forwarded = int_status.get('statistics', {}).get('alerts_forwarded', 0)
                    
                    print(f"   Progress: {(i+1)*10}s - Alerts: {alerts}, Forwarded: {forwarded}")
                
                time.sleep(10)
            
            # Step 4: Show results
            print("\n4️⃣ Demonstration Results:")
            self._show_demo_results()
            
            print("\n" + "="*60)
            print("✅ DEMONSTRATION COMPLETE")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n⏹️  Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Demo error: {e}")
        finally:
            # Step 5: Cleanup
            print("\n5️⃣ Cleaning up...")
            self.stop_real_integration()
    
    def _log_integration_startup(self):
        """Log integration startup information"""
        logger.info("📊 Integration Startup Information:")
        
        try:
            import sqlite3
            conn = sqlite3.connect('data/sovereign.db')
            cursor = conn.cursor()
            
            # Count decisions
            cursor.execute("SELECT COUNT(*) FROM autonomous_decisions")
            decision_count = cursor.fetchone()[0]
            
            # Count successful executions
            cursor.execute("SELECT COUNT(*) FROM autonomous_decisions WHERE executed = 1")
            executed_count = cursor.fetchone()[0]
            
            # Get decision confidence stats
            cursor.execute("SELECT AVG(confidence) FROM autonomous_decisions")
            avg_confidence = cursor.fetchone()[0] or 0
            
            conn.close()
            
            logger.info(f"   Historical autonomous decisions: {decision_count}")
            logger.info(f"   Successfully executed: {executed_count}")
            logger.info(f"   Average confidence: {avg_confidence:.2%}")
            
        except Exception as e:
            logger.error(f"Error getting startup stats: {e}")
    
    def _update_operational_config(self, mode: str):
        """Update operational configuration"""
        try:
            config_path = "config/autonomous.yaml"
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Update operational mode
            config['operational_mode'] = mode
            
            # Set thresholds based on mode
            if mode == "autonomous":
                config['decision_threshold'] = 0.7
                config['require_human_approval'] = False
            elif mode == "manual":
                config['decision_threshold'] = 0.9
                config['require_human_approval'] = True
            else:  # hybrid
                config['decision_threshold'] = 0.8
                config['require_human_approval'] = "critical_only"
            
            # Save updated config
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            logger.info(f"Updated autonomous configuration for {mode} mode")
            
        except Exception as e:
            logger.error(f"Error updating config: {e}")
    
    def _show_demo_results(self):
        """Show demonstration results"""
        try:
            import sqlite3
            
            conn = sqlite3.connect('data/sovereign.db')
            cursor = conn.cursor()
            
            # Get real alerts statistics
            cursor.execute("SELECT COUNT(*) FROM real_alerts")
            total_alerts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM real_alerts WHERE forwarded_to_autonomous = 1")
            forwarded_alerts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT autonomous_decision_id) FROM real_alerts WHERE autonomous_decision_id IS NOT NULL")
            decisions_made = cursor.fetchone()[0]
            
            # Get recent decisions
            cursor.execute('''
            SELECT decision_id, action, confidence, timestamp 
            FROM autonomous_decisions 
            ORDER BY timestamp DESC LIMIT 5
            ''')
            recent_decisions = cursor.fetchall()
            
            conn.close()
            
            print(f"\n📊 Real Integration Results:")
            print(f"   Total alerts processed: {total_alerts}")
            print(f"   Alerts forwarded to autonomous: {forwarded_alerts}")
            print(f"   Autonomous decisions triggered: {decisions_made}")
            
            if recent_decisions:
                print(f"\n📋 Recent Autonomous Decisions:")
                for decision in recent_decisions:
                    print(f"   • {decision[0]}: {decision[1]} "
                          f"(Confidence: {decision[2]:.2f}, Time: {decision[3][11:19]})")
            
            # Success rate
            if forwarded_alerts > 0:
                success_rate = (decisions_made / forwarded_alerts) * 100
                print(f"\n🎯 Success Rate: {success_rate:.1f}% of forwarded alerts triggered decisions")
            
        except Exception as e:
            print(f"Error showing results: {e}")
    
    def run_cli(self):
        """Run command line interface"""
        parser = argparse.ArgumentParser(description="Omega Nexus Real Integration")
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Start command
        start_parser = subparsers.add_parser('start', help='Start real integration')
        
        # Stop command
        stop_parser = subparsers.add_parser('stop', help='Stop real integration')
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show system status')
        
        # Mode command
        mode_parser = subparsers.add_parser('mode', help='Set operational mode')
        mode_parser.add_argument('--mode', choices=['autonomous', 'manual', 'hybrid'], 
                               required=True, help='Operational mode')
        
        # Demo command
        demo_parser = subparsers.add_parser('demo', help='Run demonstration')
        demo_parser.add_argument('--duration', type=int, default=300, 
                               help='Demo duration in seconds')
        
        # Simulate command
        sim_parser = subparsers.add_parser('simulate', help='Run simulation')
        sim_parser.add_argument('--scenario', choices=['basic', 'phishing', 'ddos', 'advanced', 'real'],
                              default='real', help='Simulation scenario')
        sim_parser.add_argument('--duration', type=int, default=180, 
                               help='Simulation duration in seconds')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        # Execute command
        if args.command == 'start':
            print("🚀 Starting Omega Nexus Real Integration...")
            if self.start_real_integration():
                print("✅ Real integration started")
                print("Use 'status' command to check progress")
            else:
                print("❌ Failed to start real integration")
        
        elif args.command == 'stop':
            print("🛑 Stopping Omega Nexus Real Integration...")
            self.stop_real_integration()
            print("✅ Real integration stopped")
        
        elif args.command == 'status':
            status = self.get_system_status()
            print(json.dumps(status, indent=2))
        
        elif args.command == 'mode':
            if self.set_operational_mode(args.mode):
                print(f"✅ Operational mode set to: {args.mode}")
            else:
                print(f"❌ Failed to set mode: {args.mode}")
        
        elif args.command == 'demo':
            self.run_demo(args.duration)
        
        elif args.command == 'simulate':
            print(f"🧪 Running {args.scenario} scenario simulation...")
            # For now, just run demo for simulation
            self.run_demo(args.duration)
        
        else:
            parser.print_help()

def main():
    """Main entry point"""
    nexus = OmegaNexusRealIntegration()
    
    if len(sys.argv) > 1:
        nexus.run_cli()
    else:
        # Interactive mode
        print("\n" + "="*60)
        print("🏛️ JAIDA-OMEGA-SAIOS REAL INTEGRATION")
        print("="*60)
        print("\nCommands:")
        print("  start     - Start real integration")
        print("  stop      - Stop real integration")
        print("  status    - Show system status")
        print("  mode      - Set operational mode")
        print("  demo      - Run complete demonstration")
        print("  simulate  - Run attack simulation")
        print("\nExamples:")
        print("  python3 omega_nexus_real_integration.py start")
        print("  python3 omega_nexus_real_integration.py demo --duration 180")
        print("  python3 omega_nexus_real_integration.py mode --mode autonomous")
        print("\nDashboard: http://localhost:8050 (if enabled)")
        print("="*60)

if __name__ == "__main__":
    main()
