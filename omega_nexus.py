#!/usr/bin/env python3
"""
OMEGA_NEXUS: Central Orchestrator for JAIDA-OMEGA-SAIOS
Main entry point that integrates all system modules.
"""

import sys
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import importlib.util
import importlib
import subprocess
import threading
from queue import Queue
import traceback


class OmegaNexus:
    """Central orchestrator for the JAIDA-OMEGA-SAIOS platform"""
    
    def __init__(self, config_path: str = "nexus_config.json"):
        self.start_time = datetime.now()
        print(f"🏛️  OMEGA_NEXUS Initializing at {self.start_time}")
        print("=" * 60)
        
        self.config = self._load_config(config_path)
        self.modules = {}
        self.command_queue = Queue()
        self.running = True
        self.db = None  # Add this line
        
        self._init_modules()
        
        # Add SovereignDB integration AFTER module initialization
        try:
            from sovereign_db import SovereignDB
            self.db = SovereignDB()
            self.modules["sovereign_db"] = {
                "module": SovereignDB,
                "instance": self.db,
                "path": "sovereign_db"
            }
            print("  ✅ Integrated: sovereign_db -> Persistent data layer")
        except ImportError as e:
            print(f"  ⚠️  SovereignDB not available: {e}")
            self.db = None
        
        print("=" * 60)
        
        self.config = self._load_config(config_path)
        self.modules = {}
        self.command_queue = Queue()
        self.running = True
        self._init_modules()
        # Add SovereignDB integration
        try:
            from sovereign_db import SovereignDB
            self.db = SovereignDB()
            self.modules["sovereign_db"] = {
                "module": SovereignDB,
                "instance": self.db,
                "path": "sovereign_db"
            }
            print("  ✅ Integrated: sovereign_db -> Persistent data layer")
        except ImportError as e:
            print(f"  ⚠️  SovereignDB not available: {e}")
            self.db = None
        print("=" * 60)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load nexus configuration"""
        default_config = {
            "system_name": "JAIDA-OMEGA-SAIOS",
            "version": "1.0.0",
            "modules": {
                "hierarchy": "sovereign_hierarchy",
                "bot_father": "bot_father_system", 
                "crawler": "web_crawler_system",
                "dashboard": "simple_threat_dashboard",
                "enterprise": "enterprise_platform_simple"
            },
            "log_level": "INFO",
            "auto_start": ["hierarchy", "bot_father"],
            "data_dir": "./nexus_data"
        }
        
        # Create data directory
        os.makedirs(default_config["data_dir"], exist_ok=True)
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    config.setdefault(key, value)
                return config
        except FileNotFoundError:
            print(f"⚠️  Config '{config_path}' not found, using defaults")
            return default_config
            
    def _init_modules(self):
        """Dynamically import and initialize configured modules"""
        print("🔧 Initializing OMEGA_NEXUS modules...")
        
        for module_name, module_path in self.config.get("modules", {}).items():
            try:
                # Try to import the module
                module = importlib.import_module(module_path)
                self.modules[module_name] = {
                    "module": module,
                    "instance": None,
                    "path": module_path
                }
                print(f"  ✅ Loaded: {module_name:15} -> {module_path}")
                
            except ImportError as e:
                print(f"  ⚠️  Module '{module_path}' not found: {e}")
                self.modules[module_name] = {"error": str(e), "path": module_path}
                
    def get_module(self, module_name: str):
        """Get a module instance"""
        if module_name not in self.modules:
            return None
            
        module_info = self.modules[module_name]
        if "error" in module_info:
            print(f"❌ Module '{module_name}' has error: {module_info['error']}")
            return None
            
        return module_info["module"]
        
    def run_command(self, command: str, args: List[str] = None):
        """Execute a system command through the nexus"""
        print(f"📡 Nexus Command: {command} {' '.join(args) if args else ''}")
        
        commands = {
            "status": self._cmd_status,
            "dbstatus": self._cmd_dbstatus,
            "test": self._cmd_test,
            "deploy": self._cmd_deploy,
            "crawl": self._cmd_crawl,
            "dashboard": self._cmd_dashboard,
            "dbstatus": self._cmd_dbstatus
        }
        
        if command in commands:
            return commands[command](args or [])
        else:
            print(f"❌ Unknown command: {command}")
            return False
            
    def _cmd_status(self, args: List[str]) -> bool:
        """Show system status"""
        print("\n📊 OMEGA_NEXUS STATUS REPORT")
        print("-" * 40)
        print(f"System: {self.config.get('system_name')}")
        print(f"Uptime: {datetime.now() - self.start_time}")
        print(f"Modules loaded: {len([m for m in self.modules.values() if 'module' in m])}")
        print(f"Modules with errors: {len([m for m in self.modules.values() if 'error' in m])}")
        
        # Run quick test of all components
        print("\n🧪 Quick Component Check:")
        for name, info in self.modules.items():
            if "module" in info:
                print(f"  ✅ {name:15} - LOADED")
            elif "error" in info:
                print(f"  ❌ {name:15} - ERROR: {info['error']}")
            else:
                print(f"  ⚠️  {name:15} - UNKNOWN STATE")
                
        return True
        
    def _cmd_test(self, args: List[str]) -> bool:
        """Run system tests"""
        print("\n🧪 Running comprehensive system tests...")
        
        try:
            # Import and run the test suite
            result = subprocess.run(
                [sys.executable, "test_all_components.py"],
                capture_output=True,
                text=True
            )
            
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  Stderr: {result.stderr}")
                
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Test execution failed: {e}")
            return False
            
    def _cmd_deploy(self, args: List[str]) -> bool:
        """Deploy bots via BotFather"""
        print("
🤖 Deploying bot fleet...")
        
        bot_father = self.get_module("bot_father")
        if bot_father and hasattr(bot_father, "BotFather"):
            try:
                # Create instance
                bf = bot_father.BotFather()
                
                # Try to find a valid bot type
                bot_types = []
                if hasattr(bot_father, "BotType"):
                    bot_types = [bt.value for bt in bot_father.BotType]
                
                if bot_types:
                    # Use first available bot type
                    bot_type = bot_types[0]
                    print(f"  Using bot type: {bot_type}")
                    result = bf.create_bot(bot_type, "NEXUS-DEPLOYED-001")
                else:
                    # Fallback to default
                    print("  Using default bot creation")
                    result = bf.create_bot("default", "NEXUS-DEPLOYED-001")
                
                print(f"  Deployment result: {result}")
                
                # Register in SovereignDB
                if self.db and hasattr(self.db, 'register_bot'):
                    self.db.register_bot(
                        bot_id="NEXUS-DEPLOYED-001",
                        bot_class="WD",
                        bot_type=bot_type if 'bot_type' in locals() else "unknown",
                        capabilities=["autonomous_deployment"]
                    )
                    print("  ✅ Registered in SovereignDB")
                
                return True
            except Exception as e:
                print(f"❌ Deployment failed: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print("❌ Bot Father module not available")
            return False
        else:
            print("❌ Bot Father module not available")
            return False
            
    def _cmd_crawl(self, args: List[str]) -> bool:
        """Execute web crawling"""
        print("\n🕸️ Executing web crawl operation...")
        
        crawler = self.get_module("crawler")
        if crawler and hasattr(crawler, "WebCrawlerCoordinator"):
            try:
                # Create instance and crawl
                from web_crawler_system import WebCrawlerCoordinator
                coordinator = WebCrawlerCoordinator()
                results = coordinator.execute_crawl_operation("surface")
                print(f"  Collected {len(results)} IOCs")
                return len(results) > 0
            except Exception as e:
                print(f"❌ Crawl failed: {e}")
                print(traceback.format_exc())
                return False
        else:
            print("❌ Web crawler module not available")
            return False
            
    def _cmd_dashboard(self, args: List[str]) -> bool:
        """Generate threat dashboard"""
        print("\n📈 Generating threat dashboard...")
        
        dashboard = self.get_module("dashboard")
        if dashboard and hasattr(dashboard, "ThreatDashboard"):
            try:
                td = dashboard.ThreatDashboard()
                report = td.generate_report()
                print(f"  Threat Level: {report.get('threat_level', 'UNKNOWN')}")
                print(f"  IOCs Generated: {len(report.get('iocs', []))}")
                return True
            except Exception as e:
                print(f"❌ Dashboard failed: {e}")
                return False
        else:
            print("❌ Dashboard module not available")
            return False
        
    def _cmd_dbstatus(self, args: List[str]) -> bool:
        """Show database status"""
        if not self.db:
            print("❌ SovereignDB not available")
            return False
            
        print("\n📊 SOVEREIGN DATABASE STATUS")
        print("-" * 40)
        
        metrics = self.db.get_metrics()
        
        print(f"🤖 BOT FLEET: {metrics['bots']['total']} bots")
        print(f"⚠️  THREAT INTELLIGENCE: {metrics['threats']['total']} threats")
        print(f"📅 LAST UPDATE: {metrics['timestamp']}")
        
        return True
    def interactive_mode(self):
        """Start interactive command mode"""
        print("\n💻 OMEGA_NEXUS Interactive Mode")
        print("Commands: status, test, deploy, crawl, dashboard, exit")
        
        while self.running:
            try:
                cmd_input = input("\nnexus> ").strip().split()
                if not cmd_input:
                    continue
                    
                command = cmd_input[0].lower()
                args = cmd_input[1:] if len(cmd_input) > 1 else []
                
                if command == "exit":
                    print("👋 Exiting OMEGA_NEXUS")
                    self.running = False
                else:
                    self.run_command(command, args)
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting OMEGA_NEXUS")
                self.running = False
            except Exception as e:
                print(f"❌ Command error: {e}")


def main():
    """Main entry point"""
    nexus = OmegaNexus()
    
    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        nexus.run_command(command, args)
    else:
        # Interactive mode
        nexus.interactive_mode()


if __name__ == "__main__":
    main()
