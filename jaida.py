#!/usr/bin/env python3
"""
🏛️ JAIDA-Omega-SAIOS - Main Entry Point
Version: 1.0.0
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_system():
    """Run the main JAIDA system"""
    from core.jaida_core import EnhancedJAIDA
    
    print("🤖 JAIDA-Omega-SAIOS Autonomous System")
    print("=" * 50)
    print("Starting enhanced threat detection engine...")
    
    jaida = EnhancedJAIDA()
    jaida.run()

def show_status():
    """Show system status"""
    from core.config_manager import config
    import sqlite3
    
    print("📊 JAIDA System Status")
    print("=" * 50)
    print(f"Environment: {config.environment}")
    print(f"Config loaded: {config.get('version', 'Unknown')}")
    
    # Database status
    db_path = config.get('database.path', 'data/sovereign_data.db')
    if os.path.exists(db_path):
        size = os.path.getsize(db_path) / 1024 / 1024
        print(f"Database: {db_path} ({size:.2f} MB)")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables: {len(tables)}")
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")
    else:
        print("Database: Not found")
    
    print("\n✅ Status check complete")

def main():
    """Main entry point with command line interface"""
    parser = argparse.ArgumentParser(description="JAIDA-Omega-SAIOS Autonomous System")
    parser.add_argument('command', nargs='?', default='run', 
                       choices=['run', 'status', 'test', 'config'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_system()
    elif args.command == 'status':
        show_status()
    elif args.command == 'test':
        print("🧪 Running tests...")
        # Test imports
        try:
            import importlib
            modules = ['core.jaida_core', 'adapters.real_data_adapter', 
                      'dashboard.jaida_dashboard', 'core.config_manager']
            for module in modules:
                importlib.import_module(module)
                print(f"✅ {module}")
            print("\n✅ All imports successful")
        except ImportError as e:
            print(f"❌ Import error: {e}")
    elif args.command == 'config':
        from core.config_manager import config
        import json
        print(json.dumps(config.config, indent=2, default=str))

if __name__ == "__main__":
    main()
