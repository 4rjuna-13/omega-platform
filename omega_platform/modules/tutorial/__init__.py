"""
Main integration point for Phase 2G
"""

from .welcome_flow import WelcomeFlow
from .sandbox_manager import SandboxManager

class TutorialSystem:
    """Main Phase 2G Tutorial System"""
    
    def __init__(self, tutorial_engine):
        self.engine = tutorial_engine
        self.welcome = WelcomeFlow(tutorial_engine)
        self.sandbox = SandboxManager()
        
        # Marketing metrics tracking
        self.metrics = {
            "first_15_min_completions": 0,
            "tutorial_start_time": None,
            "average_completion_time": None
        }
    
    def launch_tutorial_mode(self):
        """Main entry point for Phase 2G"""
        print("\n" + "="*60)
        print("🎮 PROJECT OMEGA - TUTORIAL MODE (PHASE 2G)")
        print("="*60)
        print("\nMarketing Positioning: 'The First All-in-One,")
        print("Open-Source Security Training Platform'")
        
        # Enable safe sandbox
        if not self.sandbox.enable_safe_mode():
            print("\n⚠️  Could not enable safe mode. Proceeding with caution.")
        
        # Start first 15 minutes experience
        import time
        self.metrics["tutorial_start_time"] = time.time()
        success = self.welcome.start_first_15_minutes()
        
        if success:
            self.metrics["first_15_min_completions"] += 1
            completion_time = time.time() - self.metrics["tutorial_start_time"]
            self.metrics["average_completion_time"] = completion_time
            
            # Marketing success metrics
            print(f"\n📊 MARKETING METRICS UPDATED:")
            print(f"   First 15-min completions: {self.metrics['first_15_min_completions']}")
            print(f"   Average time: {completion_time:.1f} seconds")
            print(f"   Completion rate: {self.welcome.get_completion_rate():.1f}%")
        
        return success
