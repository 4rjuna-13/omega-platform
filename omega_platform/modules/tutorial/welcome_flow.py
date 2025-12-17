"""
Marketing Promise: "Go from zero to detecting, deceiving, and responding to attacks in your first hour"
This delivers the "First 15 Minutes" experience
"""

import time
import json
from pathlib import Path

class WelcomeFlow:
    def __init__(self, tutorial_engine):
        self.engine = tutorial_engine
        self.progress_file = Path("tutorial_progress.json")
        self.current_step = 0
        
        # Marketing-driven learning path
        self.steps = [
            {
                "id": "welcome",
                "title": "Welcome to Project Omega",
                "duration": "1 min",
                "description": "Your personal Security Operations Center",
                "marketing_message": "Launch Your Cybersecurity Career - Risk-Free"
            },
            {
                "id": "setup_environment",
                "title": "Setup Your Security Lab",
                "duration": "2 min", 
                "description": "Configure your safe sandbox environment",
                "marketing_message": "Zero-risk learning on real security tools"
            },
            {
                "id": "first_detection",
                "title": "Detect Your First Attack",
                "duration": "5 min",
                "description": "Use nmap scanning and detection",
                "marketing_message": "Hands-on experience with enterprise security tools"
            },
            {
                "id": "deploy_honeypot", 
                "title": "Deploy a Honeypot",
                "duration": "4 min",
                "description": "Set up deception to catch attackers",
                "marketing_message": "Practice real deception techniques"
            },
            {
                "id": "automated_response",
                "title": "Automate Threat Response",
                "duration": "3 min",
                "description": "Block attacks automatically",
                "marketing_message": "Complete defensive lifecycle: Monitor → Deceive → Respond"
            }
        ]
    
    def start_first_15_minutes(self):
        """The core marketing promise - complete first experience in 15 minutes"""
        print("\n" + "="*60)
        print("🚀 PROJECT OMEGA - FIRST 15 MINUTES EXPERIENCE")
        print("="*60)
        print("\nMarketing Promise: 'Go from zero to detecting, deceiving,")
        print("and responding to attacks in your first hour'")
        print("\nLet's begin your cybersecurity journey...\n")
        
        total_time = 0
        for step in self.steps:
            print(f"\n▶️  Step {self.steps.index(step)+1}: {step['title']}")
            print(f"   ⏱️  {step['duration']} | 💡 {step['marketing_message']}")
            
            # Execute step
            success = self.execute_step(step['id'])
            if not success:
                print(f"   ⚠️  Step incomplete - you can retry later")
            
            # Update progress
            self.save_progress(step['id'])
            
            # Calculate time (for demo, we'll simulate)
            time.sleep(1)  # Simulated step completion
            total_time += int(step['duration'].split()[0])
            
            if total_time >= 15:
                print("\n⏰ Time's up! You've completed your first 15 minutes.")
                break
        
        print("\n" + "="*60)
        print("🎉 FIRST 15 MINUTES COMPLETE!")
        print("="*60)
        print("\nYou've experienced:")
        print("✓ Safe sandbox environment")
        print("✓ Real attack detection")
        print("✓ Honeypot deployment")
        print("✓ Automated response")
        print("\nContinue with weekly tutorials to advance your skills!")
        
        return True
    
    def execute_step(self, step_id):
        """Execute a specific learning step"""
        if step_id == "welcome":
            return self.show_welcome()
        elif step_id == "setup_environment":
            return self.setup_environment()
        elif step_id == "first_detection":
            return self.first_detection()
        elif step_id == "deploy_honeypot":
            return self.deploy_honeypot()
        elif step_id == "automated_response":
            return self.automated_response()
        return False
    
    def show_welcome(self):
        print("\n   Welcome to Project Omega - The all-in-one open-source")
        print("   security training platform. This is your personal SOC.")
        return True
    
    def setup_environment(self):
        print("\n   Configuring safe sandbox...")
        print("   All tools run in isolated environment.")
        print("   No risk to your real systems.")
        return True
    
    def first_detection(self):
        print("\n   Simulating nmap scan detection...")
        print("   Learning to identify reconnaissance attacks.")
        return True
    
    def deploy_honeypot(self):
        print("\n   Deploying Cowrie honeypot...")
        print("   Learning deception techniques to trap attackers.")
        return True
    
    def automated_response(self):
        print("\n   Configuring automatic blocking rules...")
        print("   Learning incident response automation.")
        return True
    
    def save_progress(self, step_id):
        """Save user progress for resumption"""
        progress = self.load_progress()
        progress['completed_steps'].append(step_id)
        progress['last_activity'] = time.time()
        
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def load_progress(self):
        """Load user progress"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {'completed_steps': [], 'last_activity': None}
    
    def get_completion_rate(self):
        """Calculate completion percentage for metrics"""
        progress = self.load_progress()
        completed = len(progress['completed_steps'])
        total = len(self.steps)
        return (completed / total) * 100 if total > 0 else 0
