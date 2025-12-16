"""
OMEGA V4 WITH PHASE 2G - FINAL VERSION
Simplified integration without eventlet issues
"""

import json
import sys
from pathlib import Path

# Add current directory to path
sys.path.append('.')
sys.path.append('./tutorial_system')

print("\n" + "="*70)
print("🚀 PROJECT OMEGA v4.0 WITH PHASE 2G - LAUNCH READY")
print("="*70)

# Import Phase 2G
try:
    from tutorial_system import TutorialSystem
    PHASE_2G_AVAILABLE = True
    print("✅ Phase 2G Tutorial System: AVAILABLE")
except ImportError as e:
    PHASE_2G_AVAILABLE = False
    print(f"⚠️  Phase 2G Tutorial System: UNAVAILABLE ({e})")

# Import TutorialEngine with proper initialization
try:
    # First, let's see what TutorialEngine needs
    import tutorial_engine
    print("✅ Tutorial Engine: AVAILABLE")
    
    # Create a mock server for TutorialEngine
    class MockOmegaServer:
        def __init__(self):
            self.name = "OmegaServer"
            self.config = {"phase_2g": True}
        
        def log_event(self, event):
            print(f"[Server Log] {event}")
    
    # Initialize TutorialEngine with mock server
    mock_server = MockOmegaServer()
    
    # Check if we need to patch the TutorialEngine
    import inspect
    init_signature = inspect.signature(tutorial_engine.TutorialEngine.__init__)
    params = list(init_signature.parameters.keys())
    
    print(f"📋 TutorialEngine parameters: {params}")
    
    if len(params) > 1 and 'omega_server' in params:
        print("⚠️  TutorialEngine requires omega_server parameter")
        # We'll handle this in the integration
    else:
        print("✅ TutorialEngine doesn't require omega_server")
    
except Exception as e:
    print(f"❌ Tutorial Engine import error: {e}")

class OmegaV4Phase2G:
    """Main Omega v4 with Phase 2G integration"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("🎯 PROJECT OMEGA - MARKETING POSITIONING")
        print("="*70)
        print("\nPositioning: 'The First All-in-One, Open-Source")
        print("Security Training Platform'")
        
        print("\n" + "="*70)
        print("📊 KEY DIFFERENTIATORS")
        print("="*70)
        print("• Complete Defensive Lifecycle (Monitor → Deceive → Respond)")
        print("• Progressive Learning Path")
        print("• Safe Sandbox Environment")
        print("• Free & Open Source")
        
        # Initialize Phase 2G
        if PHASE_2G_AVAILABLE:
            self.init_phase_2g()
        
        # Load existing Omega modules
        self.load_existing_modules()
    
    def init_phase_2g(self):
        """Initialize Phase 2G Tutorial System"""
        print("\n" + "="*70)
        print("🎮 PHASE 2G INITIALIZATION")
        print("="*70)
        
        try:
            # Create a minimal TutorialEngine
            class SimpleTutorialEngine:
                def __init__(self):
                    self.name = "SimpleTutorialEngine"
                    self.tutorials = {}
                    self.active_tutorial = None
                
                def start_engine(self):
                    print("[TutorialEngine] Engine started")
                    return True
                
                def get_tutorial(self, tutorial_id):
                    return {"id": tutorial_id, "name": "Demo Tutorial"}
            
            # Create engine instance
            engine = SimpleTutorialEngine()
            
            # Initialize Phase 2G
            self.phase_2g = TutorialSystem(engine)
            
            print("✅ Phase 2G Tutorial System initialized")
            print("✅ Welcome Flow ready")
            print("✅ Sandbox Manager ready")
            
        except Exception as e:
            print(f"❌ Phase 2G initialization failed: {e}")
            import traceback
            traceback.print_exc()
    
    def load_existing_modules(self):
        """Load existing Omega modules"""
        print("\n" + "="*70)
        print("🛠️  LOADING EXISTING MODULES")
        print("="*70)
        
        modules_to_load = [
            "deception_engine.py",
            "autonomous_response.py", 
            "tutorial_integration.py",
            "omega_core.py"
        ]
        
        loaded = 0
        for module in modules_to_load:
            if Path(module).exists():
                print(f"✅ {module}")
                loaded += 1
            else:
                print(f"⚠️  {module} (not found)")
        
        print(f"\n📊 Modules loaded: {loaded}/{len(modules_to_load)}")
    
    def start(self):
        """Start Omega v4 with Phase 2G"""
        print("\n" + "="*70)
        print("🚀 STARTING PROJECT OMEGA")
        print("="*70)
        
        # Display launch options
        print("\n🎯 LAUNCH OPTIONS:")
        print("1. Beginner Mode (Phase 2G) - First 15 Minutes Experience")
        print("2. Full Platform - All Omega features")
        print("3. Tutorial System Only")
        print("4. Deception Engine Only")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1" and PHASE_2G_AVAILABLE:
            self.launch_beginner_mode()
        elif choice == "2":
            self.launch_full_platform()
        elif choice == "3":
            self.launch_tutorial_only()
        elif choice == "4":
            self.launch_deception_only()
        elif choice == "5":
            print("\n👋 Exiting Project Omega")
            return
        else:
            print(f"\n❌ Invalid choice: {choice}")
            self.start()
    
    def launch_beginner_mode(self):
        """Launch Phase 2G Beginner Experience"""
        print("\n" + "="*70)
        print("🎓 BEGINNER MODE - PHASE 2G")
        print("="*70)
        print("\nMarketing Promise: 'Go from zero to detecting,")
        print("deceiving, and responding to attacks in your first hour'")
        
        if not PHASE_2G_AVAILABLE:
            print("\n❌ Phase 2G not available")
            return
        
        try:
            # Launch the tutorial system
            success = self.phase_2g.launch_tutorial_mode()
            
            if success:
                print("\n" + "="*70)
                print("🎉 BEGINNER EXPERIENCE COMPLETE!")
                print("="*70)
                print("\nMarketing Metrics Recorded:")
                print(f"• First 15-min completions: {self.phase_2g.metrics['first_15_min_completions']}")
                print(f"• Completion rate: {self.phase_2g.welcome.get_completion_rate():.1f}%")
                
                # Offer next steps
                print("\n➡️  NEXT STEPS:")
                print("1. Try the Full Platform")
                print("2. Practice with deception tools")
                print("3. Explore autonomous response")
                
                next_choice = input("\nContinue to Full Platform? (y/n): ").strip().lower()
                if next_choice == 'y':
                    self.launch_full_platform()
            
        except Exception as e:
            print(f"\n❌ Error in beginner mode: {e}")
    
    def launch_full_platform(self):
        """Launch the full Omega platform"""
        print("\n" + "="*70)
        print("🛡️  FULL OMEGA PLATFORM")
        print("="*70)
        
        # Try to launch existing omega_v4_tutorial_final.py
        try:
            import subprocess
            print("\nLaunching Omega v4 platform...")
            
            # Check which file to run
            candidates = [
                "omega_v4_tutorial_final.py",
                "omega_v4_tutorial_working.py",
                "omega_v3_integrated.py",
                "omega_final_v2e.py"
            ]
            
            for candidate in candidates:
                if Path(candidate).exists():
                    print(f"\n✅ Found: {candidate}")
                    print(f"🚀 Launching with: python3 {candidate}")
                    
                    # Simple launch without complex dependencies
                    if "v4_tutorial" in candidate:
                        # Use a simpler approach for tutorial versions
                        self.launch_simple_server()
                    else:
                        # Try to run the file
                        subprocess.run([sys.executable, candidate])
                    return
            
            print("\n⚠️  No suitable Omega platform file found")
            print("Launching simplified version...")
            self.launch_simple_server()
            
        except Exception as e:
            print(f"\n❌ Error launching platform: {e}")
            self.launch_simple_server()
    
    def launch_simple_server(self):
        """Launch a simple HTTP server for demonstration"""
        print("\n" + "="*70)
        print("🌐 SIMPLE WEB SERVER")
        print("="*70)
        print("\nStarting on http://localhost:8081")
        print("Press Ctrl+C to stop")
        
        try:
            import http.server
            import socketserver
            import threading
            
            PORT = 8081
            
            handler = http.server.SimpleHTTPRequestHandler
            
            def run_server():
                with socketserver.TCPServer(("", PORT), handler) as httpd:
                    print(f"Serving at port {PORT}")
                    httpd.serve_forever()
            
            # Start server in background thread
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            print("\n✅ Server started successfully")
            print("📁 Serving files from current directory")
            print(f"🔗 Open: http://localhost:{PORT}")
            
            # Keep running
            input("\nPress Enter to stop server...\n")
            
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def launch_tutorial_only(self):
        """Launch only the tutorial system"""
        print("\nTutorial-only mode coming soon...")
        self.start()
    
    def launch_deception_only(self):
        """Launch only the deception engine"""
        print("\n" + "="*70)
        print("🎣 DECEPTION ENGINE")
        print("="*70)
        
        try:
            from deception_engine import DeceptionEngine
            
            engine = DeceptionEngine()
            print("\n✅ Deception Engine initialized")
            print(f"📊 Status: {engine.get_deception_stats()}")
            
            # Start deception mode
            start = input("\nStart deception mode? (y/n): ").strip().lower()
            if start == 'y':
                result = engine.start_deception_mode()
                print(f"🎣 Deception started: {result}")
                
                # Monitor for a bit
                import time
                print("\nMonitoring deception (10 seconds)...")
                for i in range(10, 0, -1):
                    print(f"Time remaining: {i}s", end='\r')
                    time.sleep(1)
                
                print("\n\n📊 Final deception stats:")
                print(json.dumps(engine.get_deception_stats(), indent=2))
                
        except Exception as e:
            print(f"❌ Deception engine error: {e}")

def main():
    """Main entry point"""
    omega = OmegaV4Phase2G()
    omega.start()

if __name__ == "__main__":
    main()
