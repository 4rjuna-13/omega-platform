#!/usr/bin/env python3
"""
CLEAN BOT FATHER - WORKING VERSION
"""

import time
import json
from datetime import datetime
from pathlib import Path

class CleanBotFather:
    def __init__(self):
        self.start_time = datetime.now()
        self.bots = []
        self.status = "initialized"
        
    def initialize(self):
        """Initialize the bot father"""
        print("🤖 CLEAN BOT FATHER v1.0")
        print("=" * 50)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Directory: {Path(__file__).parent}")
        print(f"Status: {self.status}")
        
        # Load available bots
        self.load_bots()
        
        print(f"Bots loaded: {len(self.bots)}")
        print("=" * 50)
        
    def load_bots(self):
        """Load available bots from bots directory"""
        bots_dir = Path(__file__).parent / 'bots'
        if bots_dir.exists():
            for bot_file in bots_dir.rglob('*.py'):
                if bot_file.is_file():
                    self.bots.append({
                        'name': bot_file.stem,
                        'path': str(bot_file.relative_to(bots_dir)),
                        'status': 'available'
                    })
    
    def run(self, daemon=False):
        """Run the bot father"""
        self.initialize()
        
        if daemon:
            print("🔄 Running in daemon mode...")
            print("Press Ctrl+C to stop")
            print("-" * 30)
            
            cycle = 0
            try:
                while True:
                    cycle += 1
                    current_time = datetime.now().strftime('%H:%M:%S')
                    print(f"[{current_time}] Cycle {cycle} - {len(self.bots)} bots available")
                    time.sleep(30)
            except KeyboardInterrupt:
                print("\n🛑 Bot Father stopped")
        else:
            print("📋 Available commands:")
            print("  --daemon    Run as background daemon")
            print("  --status    Show system status")
            print("  --help      Show this help")

if __name__ == "__main__":
    import sys
    
    father = CleanBotFather()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--daemon":
            father.run(daemon=True)
        elif sys.argv[1] == "--status":
            father.initialize()
        elif sys.argv[1] == "--help":
            print("Clean Bot Father - Simple Working Version")
            father.run()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            father.run()
    else:
        father.run()
