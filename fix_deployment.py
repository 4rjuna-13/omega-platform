#!/usr/bin/env python3
"""
Fix bot deployment by checking available bot types
"""

# First, let's see what's in bot_father_system.py
import bot_father_system
import inspect

print("🔍 Available Bot Types in BotFather:")
for name, obj in inspect.getmembers(bot_father_system):
    if name == 'BotType':
        print(f"  BotType enum: {obj}")
        for member in obj:
            print(f"    - {member.name}: {member.value}")
        break

# Now let's create a simple deploy script that works
print("\n🎯 Creating working deploy command...")

with open('omega_nexus.py', 'r') as f:
    content = f.read()

# Fix the _cmd_deploy method
import re
deploy_pattern = r'def _cmd_deploy\(self, args: List\[str\]\) -> bool:.*?return False'
deploy_fix = '''def _cmd_deploy(self, args: List[str]) -> bool:
        """Deploy bots via BotFather"""
        print("\\n🤖 Deploying bot fleet...")
        
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
            return False'''

content = re.sub(deploy_pattern, deploy_fix, content, flags=re.DOTALL)

with open('omega_nexus_fixed2.py', 'w') as f:
    f.write(content)

print("✅ Deployment fix applied to omega_nexus_fixed2.py")
