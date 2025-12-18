#!/usr/bin/env python3
"""
JAIDA Tutorial CLI - Interactive command-line interface for the "0 to Guru" system.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from loguru import logger
from tutorial_mode.core import JAIDATutorialEngine, TutorialState
from tutorial_mode.assessment import run_skill_assessment
from tutorial_mode.curriculum import get_path_for_level

class JAIDATutorialCLI:
    """Command-line interface for the JAIDA tutorial system."""
    
    def __init__(self):
        self.engine = JAIDATutorialEngine()
        logger.info("JAIDA Tutorial CLI initialized")
    
    def display_welcome(self):
        """Display the welcome message and system overview."""
        print("\n" + "="*60)
        print("🚀 JAIDA CYBERSECURITY TUTORIAL SYSTEM")
        print("="*60)
        print("Welcome to your journey from Novice to Cybersecurity Guru.")
        print("This system will adapt to your skill level and provide")
        print("personalized learning paths with hands-on practice labs.")
        print("\nType 'help' for commands, 'quit' to exit.")
        print("="*60 + "\n")
    
    def handle_command(self, command):
        """Process user commands - the main one-liner dispatcher."""
        cmd_map = {
            'start': lambda: self.engine.transition_to(TutorialState.ASSESSMENT),
            'status': lambda: f"Current State: {self.engine.current_state.name}",
            'next': lambda: self.engine.run_current_step(),
            'assess': lambda: run_skill_assessment(self.engine),
            'curriculum': lambda: get_path_for_level(self.engine.user_skill_profile['level']),
            'help': self.show_help,
            'quit': lambda: sys.exit(0)
        }
        
        # The core one-liner: execute command or show error
        return cmd_map.get(command.lower(), lambda: f"Unknown command: '{command}'. Type 'help' for options.")()
    
    def show_help(self):
        """Display available commands."""
        help_text = """
📋 AVAILABLE COMMANDS:
  start     - Begin your assessment and learning journey
  status    - Show current tutorial state and progress
  next      - Execute the next step in your learning path
  assess    - Run a skill assessment (adaptive quiz)
  curriculum- View your current learning curriculum
  help      - Show this help message
  quit      - Exit the tutorial system
  
🔧 TIP: Start with 'start' to begin your assessment.
        """
        return help_text
    
    def run_interactive(self):
        """Main interactive loop - the heart of the CLI."""
        self.display_welcome()
        
        while True:
            try:
                # Get user input with a prompt
                user_input = input(f"\n[{self.engine.current_state.name.lower()}] JAIDA> ").strip()
                
                if not user_input:
                    continue
                
                # Handle the command
                result = self.handle_command(user_input)
                
                # Display result
                if result:
                    print(f"\n{result}")
                    
                # Auto-advance logic: after assessment, move to curriculum selection
                if user_input == 'start' and self.engine.current_state == TutorialState.ASSESSMENT:
                    print("\n📊 Running adaptive skill assessment...")
                    assessment_result = run_skill_assessment(self.engine)
                    print(f"Assessment complete! You'll be learning: {assessment_result.get('next_state', 'next module')}")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted. Type 'quit' to exit properly.")
            except Exception as e:
                logger.error(f"CLI error: {e}")
                print(f"⚠️  Error: {e}")

# One-liner to launch the CLI directly
if __name__ == "__main__":
    print("[*] Starting JAIDA Tutorial CLI...")
    cli = JAIDATutorialCLI()
    cli.run_interactive()
