#!/usr/bin/env python3
"""
Fix OmegaNexus to properly integrate SovereignDB
"""

import re

# Read the current file
with open('omega_nexus.py', 'r') as f:
    content = f.read()

# Fix 1: Add proper SovereignDB import in __init__
init_pattern = r'def __init__\(self, config_path: str = "nexus_config\.json"\):'
init_replacement = '''def __init__(self, config_path: str = "nexus_config.json"):
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
        
        print("=" * 60)'''

# Replace the __init__ method
content = re.sub(r'def __init__\(self, config_path: str = "nexus_config\.json"\):.*?print\("=" \* 60\)', 
                init_replacement, content, flags=re.DOTALL)

# Fix 2: Add dbstatus command method
# Find the right place (after other _cmd methods)
if '_cmd_dashboard' in content:
    # Add after _cmd_dashboard
    dashboard_end = content.find('def _cmd_dashboard')
    insert_point = content.find('\n    def ', dashboard_end + 20)
    
    dbstatus_method = '''
    def _cmd_dbstatus(self, args: List[str]) -> bool:
        """Show database status"""
        if not self.db:
            print("❌ SovereignDB not available")
            return False
            
        print("\\n📊 SOVEREIGN DATABASE STATUS")
        print("-" * 40)
        
        metrics = self.db.get_metrics()
        
        print(f"🤖 BOT FLEET: {metrics['bots']['total']} bots")
        print(f"⚠️  THREAT INTELLIGENCE: {metrics['threats']['total']} threats")
        print(f"📅 LAST UPDATE: {metrics['timestamp']}")
        
        return True'''
    
    content = content[:insert_point] + dbstatus_method + content[insert_point:]

# Fix 3: Add dbstatus to commands dictionary
if '"dashboard": self._cmd_dashboard' in content:
    content = content.replace('"dashboard": self._cmd_dashboard',
                             '"dashboard": self._cmd_dashboard,\n            "dbstatus": self._cmd_dbstatus')

# Write the fixed file
with open('omega_nexus_fixed.py', 'w') as f:
    f.write(content)

print("✅ Fixed omega_nexus.py created as omega_nexus_fixed.py")
