#!/usr/bin/env python3
"""
INTEGRATE TUTORIAL ENGINE WITH OMEGA v4.0
Universal integration guide
"""

import sys
sys.path.append('.')

print("="*70)
print("PROJECT OMEGA - TUTORIAL ENGINE INTEGRATION GUIDE")
print("Phase 2G: Adding Interactive Learning to Omega v4.0")
print("="*70)

print("\n📋 FILES CREATED FOR PHASE 2G:")
print("1. tutorial_engine.py    - Core tutorial system (✓ Working)")
print("2. tutorial_api.py       - API endpoints for web interface")
print("3. tutorial_integration.py - Command processor integration")
print("4. omega_tutorial_demo_fixed.py - Working demo (✓ Tested)")
print("5. TUTORIAL_README.md    - Complete documentation")

print("\n🎯 INTEGRATION STEPS:")
print("\nSTEP 1: Choose your main Omega server file")
print("   Based on your directory, you have these main servers:")
print("   • omega_v3_integrated.py (11,104 lines - Dec 16)")
print("   • omega_v3_ultimate.py (15,755 lines - Dec 16)")
print("   • omega_final_v2e.py (8,114 lines - Dec 16)")

print("\nSTEP 2: Add imports to your Omega server")
print("""
At the top of your Omega server file, add these imports:

# Add to existing imports
from tutorial_engine import TutorialEngine
import tutorial_api
import tutorial_integration
""")

print("\nSTEP 3: Initialize Tutorial Engine in OmegaServer.__init__()")
print("""
Find the __init__ method of your OmegaServer class and add:

# Initialize tutorial engine (add this after other engine initializations)
self.tutorial_engine = TutorialEngine(self)
print("[TUTORIAL] Tutorial Engine initialized")
""")

print("\nSTEP 4: Integrate with command processor")
print("""
In the __init__ method, after creating tutorial_engine, add:

# Integrate tutorial with command processor
tutorial_integration.integrate_tutorial_with_commands(self, self.tutorial_engine)
print("[TUTORIAL] Command processor integrated")
""")

print("\nSTEP 5: Setup API routes")
print("""
Find where your Flask app is setup (usually in setup_routes() method)
and add:

# Setup tutorial API routes
tutorial_api.setup_tutorial_api(self.app, self.tutorial_engine)
""")

print("\nSTEP 6: Update the HTML dashboard (optional)")
print("""
If you have a web dashboard, update it to include:
• Tutorial progress display
• Sandbox mode toggle
• Tutorial start buttons
""")

print("\n🔧 QUICK INTEGRATION TEMPLATE:")
print("""
# Here's exactly what to add to omega_v3_integrated.py:

# 1. At the top with other imports (around line 10):
from tutorial_engine import TutorialEngine
import tutorial_api
import tutorial_integration

# 2. In OmegaServer.__init__() method (find the method, around line 50):
#    Add after other engine initializations:
self.tutorial_engine = TutorialEngine(self)
print("[SYSTEM] Tutorial Engine ready")

# 3. Still in __init__, add:
tutorial_integration.integrate_tutorial_with_commands(self, self.tutorial_engine)

# 4. In setup_routes() or similar method:
tutorial_api.setup_tutorial_api(self.app, self.tutorial_engine)
""")

print("\n🎮 USER COMMANDS AFTER INTEGRATION:")
print("""
Users will be able to type these commands:
• tutorial start welcome    - Start the welcome tutorial
• tutorial list            - List all available tutorials  
• tutorial status          - Check progress
• sandbox activate        - Enable safe sandbox mode
• sandbox deactivate      - Disable sandbox mode
• help                    - Show tutorial-enhanced help
""")

print("\n🧪 TEST INTEGRATION:")
print("""
To test if integration worked:
1. Start your Omega server: python3 omega_v3_integrated.py
2. Connect to the web interface (usually http://localhost:8081)
3. Type 'tutorial start welcome' in the command input
4. You should see the tutorial starting message!
""")

print("\n" + "="*70)
print("✅ INTEGRATION READY!")
print("="*70)

print("\n💡 PRO TIP: The tutorial system is designed to be modular.")
print("If you encounter any issues, you can:")
print("1. Check the demo works: python3 omega_tutorial_demo_fixed.py")
print("2. Review error logs in: tutorial_engine/logs/tutorial.log")
print("3. Start with just the tutorial engine, then add API routes")

