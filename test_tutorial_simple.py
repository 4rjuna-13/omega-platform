#!/usr/bin/env python3
"""
Simple test of Tutorial Engine
"""

import sys
sys.path.append('.')

try:
    from tutorial_engine import TutorialEngine
    print("✓ Tutorial Engine imported successfully")
    
    # Test basic functionality
    class MockServer:
        def __init__(self):
            self.socketio = type('obj', (object,), {'emit': lambda *args, **kwargs: None})()
    
    server = MockServer()
    tutorial = TutorialEngine(server)
    
    print("✓ Tutorial Engine initialized")
    print(f"✓ Loaded {len(tutorial.tutorials)} tutorials")
    
    # Test starting a tutorial
    result = tutorial.start_tutorial("welcome")
    print(f"✓ Started tutorial: {result['message']}")
    
    # Test getting status
    status = tutorial.get_tutorial_status()
    print(f"✓ Got tutorial status - Active: {status['active']}")
    
    # Test some methods
    print(f"✓ Sandbox mode: {tutorial.sandbox_mode}")
    print(f"✓ User level: {tutorial.user_level}")
    
    print("\n✅ All basic tests passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

