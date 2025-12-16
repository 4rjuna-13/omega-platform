#!/usr/bin/env python3
"""
Project Omega - Intelligence Interface
Main interface for Phase 2C
"""

import sys
import json
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init()

class OmegaIntelligence:
    def __init__(self):
        print(f"{Fore.CYAN}{'='*60}")
        print("   PROJECT OMEGA - INTELLIGENCE LAYER")
        print("           Phase 2C: Predictive Threat Model")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        # Try to load components
        self.load_components()
        
    def load_components(self):
        """Load available components"""
        print(f"{Fore.YELLOW}Loading components...{Style.RESET_ALL}")
        
        # Try to load threat predictor
        try:
            from predictive_threat import ThreatPredictor
            self.predictor = ThreatPredictor()
            if self.predictor.load_model():
                print(f"{Fore.GREEN}  ✅ Threat Predictor: Model loaded{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}  ⚠️  Threat Predictor: Ready for training{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}  ❌ Threat Predictor: Not available ({e}){Style.RESET_ALL}")
            self.predictor = None
        
        # Try to load voice module
        try:
            from voice_module import VoiceCommandProcessor
            self.voice = VoiceCommandProcessor()
            status = self.voice.get_status()
            print(f"{Fore.GREEN}  ✅ Voice System: Ready{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.YELLOW}  ⚠️  Voice System: Limited ({e}){Style.RESET_ALL}")
            self.voice = None
        
        print()
    
    def show_status(self):
        """Show system status"""
        status = f"{Fore.CYAN}=== OMEGA INTELLIGENCE STATUS ==={Style.RESET_ALL}\n"
        
        if self.predictor:
            status += f"Threat Predictor: {'Trained' if self.predictor.is_trained else 'Ready for training'}\n"
        else:
            status += "Threat Predictor: Not available\n"
        
        if self.voice:
            status += "Voice System: Available\n"
        else:
            status += "Voice System: Not available\n"
        
        status += f"Security Level: MONITOR\n"
        status += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return status
    
    def handle_command(self, command):
        """Handle user commands"""
        cmd = command.lower().strip()
        
        if cmd == 'status':
            return self.show_status()
        
        elif cmd == 'predict':
            if not self.predictor:
                return f"{Fore.RED}Threat predictor not available{Style.RESET_ALL}"
            
            # Sample prediction
            sample_data = {
                'ports': [22, 80, 443, 8080, 4444],
                'auth_attempts': {'ssh': 5, 'failed': 2},
                'scan_data': {'intensity': 0.7}
            }
            
            try:
                score, explanation = self.predictor.predict_threat(sample_data)
                return (f"{Fore.CYAN}Sample Threat Analysis:{Style.RESET_ALL}\n"
                       f"Threat Score: {score:.2%}\n"
                       f"Assessment: {explanation}")
            except Exception as e:
                return f"{Fore.RED}Prediction error: {e}{Style.RESET_ALL}"
        
        elif cmd == 'train':
            if not self.predictor:
                return f"{Fore.RED}Threat predictor not available{Style.RESET_ALL}"
            
            try:
                self.predictor.generate_sample_data(100)
                self.predictor.train_model()
                return f"{Fore.GREEN}Model training initiated{Style.RESET_ALL}"
            except Exception as e:
                return f"{Fore.RED}Training error: {e}{Style.RESET_ALL}"
        
        elif cmd == 'voice':
            if not self.voice:
                return f"{Fore.YELLOW}Voice system not available{Style.RESET_ALL}"
            
            return f"{Fore.CYAN}Voice commands: 'listen' or 'speak [text]'{Style.RESET_ALL}"
        
        elif cmd == 'listen':
            if not self.voice:
                return f"{Fore.YELLOW}Voice system not available{Style.RESET_ALL}"
            
            result = self.voice.listen_command(timeout=3)
            return f"{Fore.CYAN}Voice input: {result}{Style.RESET_ALL}"
        
        elif cmd.startswith('speak '):
            if not self.voice:
                return f"{Fore.YELLOW}Voice system not available{Style.RESET_ALL}"
            
            text = cmd[6:]
            self.voice.speak(text)
            return f"{Fore.CYAN}Speaking: {text}{Style.RESET_ALL}"
        
        elif cmd == 'help':
            return self.show_help()
        
        elif cmd in ['exit', 'quit']:
            return 'exit'
        
        else:
            return f"{Fore.YELLOW}Unknown command. Type 'help' for options.{Style.RESET_ALL}"
    
    def show_help(self):
        """Show help information"""
        return f"""{Fore.GREEN}=== OMEGA INTELLIGENCE COMMANDS ==={Style.RESET_ALL}

{Fore.CYAN}Core Commands:{Style.RESET_ALL}
  status    - Show system status
  predict   - Run threat prediction on sample data
  train     - Train threat prediction model

{Fore.CYAN}Voice Commands:{Style.RESET_ALL}
  voice     - Show voice options
  listen    - Listen for voice command
  speak [text] - Convert text to speech

{Fore.CYAN}System Commands:{Style.RESET_ALL}
  help      - Show this help
  exit      - Exit Omega Intelligence

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  predict
  train
  speak Hello Omega
  status
"""
    
    def run(self):
        """Main interactive loop"""
        print(self.show_help())
        
        while True:
            try:
                # Get command
                command = input(f"\n{Fore.GREEN}OMEGA-INTEL>{Style.RESET_ALL} ").strip()
                
                if not command:
                    continue
                
                # Handle command
                result = self.handle_command(command)
                
                if result == 'exit':
                    print(f"{Fore.YELLOW}Exiting Omega Intelligence...{Style.RESET_ALL}")
                    break
                
                print(result)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def main():
    """Main entry point"""
    try:
        omega = OmegaIntelligence()
        omega.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
