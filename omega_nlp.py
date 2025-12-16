"""
Natural Language Interface for Project Omega
Speak security commands like a security operations center
"""
import re
from typing import Dict, List, Any
import asyncio

class OmegaNLP:
    """Natural Language Processing for security commands"""
    
    def __init__(self):
        self.command_patterns = {
            # Scan commands
            r"scan (?:for )?(?:vulnerabilities|ports) on (.+)": "scan_target",
            r"check (.+) for (?:open ports|services)": "scan_target",
            r"what's running on (.+)": "scan_target",
            
            # Wireless commands
            r"scan (?:for )?wifi(?: networks)?": "scan_wireless",
            r"check wireless (?:security|networks)": "scan_wireless",
            r"find wifi networks": "scan_wireless",
            
            # Security commands
            r"analyze security of (.+)": "analyze_security",
            r"how secure is (.+)": "analyze_security",
            r"assess (.+) for risks": "analyze_security",
            
            # System commands
            r"show (?:system|omega) status": "show_status",
            r"what's omega (?:doing|status)": "show_status",
            r"system (?:info|status)": "show_status",
            
            # Help commands
            r"help(?: me)?": "show_help",
            r"what can you do": "show_help",
            r"show commands": "show_help"
        }
        
        self.responses = {
            "scan_target": "🔍 Scanning {target} for vulnerabilities and open ports...",
            "scan_wireless": "📡 Scanning for wireless networks and assessing security...",
            "analyze_security": "🛡️ Analyzing security posture of {target}...",
            "show_status": "📊 Getting Project Omega system status...",
            "show_help": "🤖 Here's what I can help you with:"
        }
        
        print("🗣️  Omega Natural Language Interface initialized")
        print("💡 Try commands like: 'scan for vulnerabilities on 192.168.1.1'")
        print("                    'what's running on scanme.nmap.org'")
        print("                    'show omega status'")
    
    def parse_command(self, text: str) -> Dict[str, Any]:
        """Parse natural language command"""
        text = text.lower().strip()
        
        for pattern, command_type in self.command_patterns.items():
            match = re.match(pattern, text)
            if match:
                # Extract parameters
                params = match.groups()
                
                return {
                    "command": command_type,
                    "parameters": params,
                    "original": text,
                    "matched_pattern": pattern
                }
        
        # No match found
        return {
            "command": "unknown",
            "parameters": [],
            "original": text,
            "error": "Command not recognized"
        }
    
    async def execute_command(self, parsed_command: Dict) -> Dict:
        """Execute parsed command"""
        command_type = parsed_command["command"]
        
        if command_type == "unknown":
            return {
                "status": "error",
                "message": f"❌ I didn't understand: '{parsed_command['original']}'",
                "suggestions": [
                    "Try: 'scan for vulnerabilities on scanme.nmap.org'",
                    "Try: 'show omega status'",
                    "Try: 'help' for all commands"
                ]
            }
        
        # Get response template
        response_template = self.responses.get(command_type, "Processing command...")
        
        # Format with parameters if any
        if parsed_command["parameters"]:
            response = response_template.format(target=parsed_command["parameters"][0])
        else:
            response = response_template
        
        # Simulate processing
        await asyncio.sleep(0.5)
        
        # Return structured result
        result = {
            "status": "success",
            "command": command_type,
            "response": response,
            "parameters": parsed_command["parameters"],
            "actions_triggered": []
        }
        
        # Add specific actions based on command
        if command_type == "scan_target" and parsed_command["parameters"]:
            result["actions_triggered"].append(f"nmap_scan_{parsed_command['parameters'][0]}")
        
        elif command_type == "show_help":
            result["available_commands"] = [
                "• scan [target] for vulnerabilities",
                "• check [target] for open ports",
                "• scan for wifi networks",
                "• analyze security of [target]",
                "• show omega status",
                "• help"
            ]
        
        elif command_type == "show_status":
            result["system_info"] = {
                "platform": "Linux x86_64",
                "omega_version": "1.0.0",
                "security_level": "MONITOR",
                "active_nodes": 1,
                "encryption": "XChaCha20-Poly1305"
            }
        
        return result

# Interactive interface
async def interactive_nlp():
    """Interactive natural language interface"""
    nlp = OmegaNLP()
    
    print("\n" + "="*60)
    print("🤖 PROJECT OMEGA - NATURAL LANGUAGE INTERFACE")
    print("="*60)
    print("Type 'quit' or 'exit' to leave\n")
    
    while True:
        try:
            # Get user input
            user_input = input("Omega Command> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Stay secure!")
                break
            
            if not user_input:
                continue
            
            # Parse command
            parsed = nlp.parse_command(user_input)
            
            # Execute command
            result = await nlp.execute_command(parsed)
            
            # Display result
            print(f"\n📝 Command: {user_input}")
            print(f"🔧 Parsed as: {parsed['command']}")
            
            if result["status"] == "success":
                print(f"✅ {result['response']}")
                
                # Show additional info
                if "available_commands" in result:
                    print("\nAvailable Commands:")
                    for cmd in result["available_commands"]:
                        print(f"  {cmd}")
                
                elif "system_info" in result:
                    print("\nSystem Information:")
                    for key, value in result["system_info"].items():
                        print(f"  {key}: {value}")
                
                if result["actions_triggered"]:
                    print(f"\n⚡ Actions triggered: {', '.join(result['actions_triggered'])}")
            
            else:
                print(f"❌ {result['message']}")
                if "suggestions" in result:
                    print("\n💡 Suggestions:")
                    for suggestion in result["suggestions"]:
                        print(f"  {suggestion}")
            
            print()  # Empty line for spacing
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Stay secure!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Quick test
    print("🧪 Testing Natural Language Interface...")
    nlp = OmegaNLP()
    
    test_commands = [
        "scan for vulnerabilities on scanme.nmap.org",
        "what's running on 192.168.1.1",
        "show omega status",
        "help me",
        "check wireless security",
        "this is a bad command"
    ]
    
    for cmd in test_commands:
        print(f"\nTesting: '{cmd}'")
        parsed = nlp.parse_command(cmd)
        print(f"  → Parsed as: {parsed['command']}")
        if parsed['parameters']:
            print(f"  → Parameters: {parsed['parameters']}")
    
    print("\n✅ NLP test complete")
    print("\n🚀 Starting interactive mode...")
    asyncio.run(interactive_nlp())
