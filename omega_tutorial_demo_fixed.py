#!/usr/bin/env python3
"""
🚀 PROJECT OMEGA v4.0 - TUTORIAL DEMO
Fixed version that handles tutorial completion properly
"""

import os
import sys
import time

# Add current directory to path
sys.path.append('.')

try:
    from tutorial_engine import TutorialEngine
    print("✓ Tutorial Engine loaded successfully")
except ImportError as e:
    print(f"✗ Failed to load Tutorial Engine: {e}")
    sys.exit(1)

class MockServer:
    def __init__(self):
        # Create a mock socketio object
        class MockSocketIO:
            def emit(self, *args, **kwargs):
                pass  # Do nothing for demo
        self.socketio = MockSocketIO()
        self.mode = "TUTORIAL"
        self.clients = 0

def main():
    print("\n" + "="*70)
    print("🚀 PROJECT OMEGA - TUTORIAL ENGINE DEMO")
    print("Phase 2G: Interactive Learning & Safe Sandbox")
    print("="*70 + "\n")
    
    # Create mock server
    server = MockServer()
    
    # Initialize tutorial engine
    tutorial = TutorialEngine(server)
    
    # Demo the tutorial system
    print("1. Starting Welcome Tutorial...")
    result = tutorial.start_tutorial("welcome")
    print(f"   Result: {result['message']}")
    
    print("\n2. Simulating user actions...")
    time.sleep(1)
    
    # Complete first step
    print("   Completing step 1...")
    result = tutorial.complete_step("welcome", "welcome_1")
    if 'step_completed' in result:
        print(f"   Step completed: {result['step_completed']}")
    else:
        print(f"   Tutorial completed: {result.get('tutorial_completed', 'Unknown')}")
    
    time.sleep(1)
    
    # Complete second step
    print("   Completing step 2...")
    result = tutorial.complete_step("welcome", "welcome_2")
    if 'step_completed' in result:
        print(f"   Step completed: {result['step_completed']}")
    else:
        print(f"   Tutorial completed: {result.get('tutorial_completed', 'Unknown')}")
    
    time.sleep(1)
    
    # Complete third step
    print("   Completing step 3...")
    result = tutorial.complete_step("welcome", "welcome_3")
    if 'step_completed' in result:
        print(f"   Step completed: {result['step_completed']}")
    elif 'tutorial_completed' in result:
        print(f"   🎉 Tutorial completed! Reward: {result.get('reward', 'No reward')}")
    else:
        print(f"   Result: {result}")
    
    print("\n3. Checking tutorial status...")
    status = tutorial.get_tutorial_status()
    print(f"   Active: {status['active']}")
    print(f"   Current Tutorial: {status['current_tutorial']}")
    print(f"   Sandbox Mode: {status['sandbox_mode']}")
    completed = len([t for t in status['progress'].values() if isinstance(t, dict) and t.get('completed')])
    print(f"   Completed Tutorials: {completed}")
    
    print("\n4. Testing sandbox mode...")
    result = tutorial.activate_sandbox_mode()
    print(f"   {result['message']}")
    
    print("\n5. Testing sandbox command...")
    result = tutorial.process_sandbox_command("response activate aggressive")
    print(f"   Result: {result['message']}")
    
    print("\n6. Getting recommended next tutorial...")
    recommended = tutorial.get_recommended_tutorial()
    print(f"   Recommended: {recommended or 'All tutorials completed!'}")
    
    print("\n" + "="*70)
    print("✅ TUTORIAL ENGINE DEMO COMPLETE")
    print("="*70)
    
    print("\n🎯 Ready for launch! Key features:")
    print("   • 5 structured tutorials with progressive difficulty")
    print("   • Safe sandbox mode for zero-risk experimentation")
    print("   • Achievement system with badges")
    print("   • Training scenarios for real-world practice")
    print("   • Integrated command system")
    
    print("\n📋 Files created for Phase 2G:")
    print("   tutorial_engine.py    - Core tutorial system (✓ Working)")
    print("   tutorial_api.py       - API endpoints")
    print("   tutorial_integration.py - Command processor integration")
    print("   omega_tutorial_demo.py - Demo script")
    print("   TUTORIAL_README.md    - Documentation")
    
    print("\n💡 To integrate with Omega v4.0:")
    print("   Import tutorial_engine, tutorial_api, and tutorial_integration")
    print("   Initialize TutorialEngine with your Omega server")
    print("   Call integrate_tutorial_with_commands()")
    print("   Set up routes with setup_tutorial_api()")

if __name__ == "__main__":
    main()

