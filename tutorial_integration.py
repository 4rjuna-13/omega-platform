"""
TUTORIAL INTEGRATION WITH COMMAND PROCESSOR
Enhances Omega's command processing with tutorial awareness
"""

def integrate_tutorial_with_commands(omega_server, tutorial_engine):
    """Integrate tutorial engine with command processor"""
    
    # Store original command processor
    if hasattr(omega_server, 'process_command'):
        original_process_command = omega_server.process_command
    else:
        original_process_command = None
    
    def enhanced_process_command(command):
        """Enhanced command processor with tutorial awareness"""
        
        # Check if in sandbox mode
        if tutorial_engine.sandbox_mode and not tutorial_engine.is_sandbox_command(command):
            # Process as sandbox command
            result = tutorial_engine.process_sandbox_command(command)
            return result["message"]
        
        # Check for tutorial progression triggers
        cmd_lower = command.lower()
        
        # Track tutorial progress based on commands
        if tutorial_engine.current_tutorial:
            tutorial_id = tutorial_engine.current_tutorial["id"]
            current_progress = tutorial_engine.tutorial_progress.get(tutorial_id, {})
            completed_steps = current_progress.get("completed_steps", [])
            
            # Find current step
            tutorial_steps = tutorial_engine.current_tutorial["steps"]
            current_step_index = len(completed_steps)
            
            if current_step_index < len(tutorial_steps):
                step = tutorial_steps[current_step_index]
                if "action" in step and step["action"].startswith("command:"):
                    expected_cmd = step["action"].split(":", 1)[1]
                    if expected_cmd.lower() in cmd_lower:
                        # Complete the step
                        tutorial_engine.complete_step(tutorial_id, step["id"])
        
        # Special tutorial commands
        if cmd_lower.startswith("tutorial start "):
            parts = command.split()
            if len(parts) >= 3:
                tutorial_id = parts[2]
                result = tutorial_engine.start_tutorial(tutorial_id)
                return f"Tutorial: {result.get('message', 'Started')}"
        
        elif cmd_lower == "tutorial status":
            status = tutorial_engine.get_tutorial_status()
            active = "Active" if status["active"] else "Inactive"
            current = status["current_tutorial"] or "None"
            sandbox = "ACTIVE 🧪" if status["sandbox_mode"] else "INACTIVE"
            return f"Tutorial: {active}\nCurrent: {current}\nSandbox: {sandbox}"
        
        elif cmd_lower == "tutorial list":
            tutorials = tutorial_engine.tutorials
            response = "Available Tutorials:\n"
            for tid, t in tutorials.items():
                completed = "✅" if tid in tutorial_engine.tutorial_progress and isinstance(tutorial_engine.tutorial_progress[tid], dict) and tutorial_engine.tutorial_progress[tid].get("completed") else "  "
                response += f"{completed} {t['title']} ({t['difficulty']}, {t['estimated_time']}min) - Type: 'tutorial start {tid}'\n"
            return response
        
        elif cmd_lower == "sandbox activate":
            result = tutorial_engine.activate_sandbox_mode()
            return result["message"]
        
        elif cmd_lower == "sandbox deactivate":
            result = tutorial_engine.deactivate_sandbox_mode()
            return result["message"]
        
        elif cmd_lower == "sandbox status":
            status = "ACTIVE 🧪" if tutorial_engine.sandbox_mode else "INACTIVE"
            return f"Sandbox Mode: {status}"
        
        elif cmd_lower == "help":
            return """📚 PROJECT OMEGA v4.0 - TUTORIAL EDITION

Getting Started:
  tutorial start welcome    - Start the welcome tutorial (recommended)
  tutorial list            - List all available tutorials
  tutorial status          - Check your progress

Safe Experimentation:
  sandbox activate        - Enable safe sandbox mode
  sandbox deactivate      - Disable sandbox mode
  sandbox status          - Check sandbox status

System Commands:
  system status           - Check Omega status
  help                    - Show this help message"""
        
        elif cmd_lower == "system status":
            return """Omega v4.0 Tutorial Edition - Learning Mode
CPU: 15% | Memory: 45%
Threat Level: 10/100 (Low)
Environment: tutorial_safe
Type 'help' for command list"""
        
        # Pass through to original processor if available
        if original_process_command:
            return original_process_command(command)
        
        # Default response
        return f"Command received: {command}\n💡 Tip: Type 'tutorial start welcome' to begin learning."
    
    # Replace the method
    omega_server.process_command = enhanced_process_command
    
    print("[INTEGRATION] Tutorial Engine integrated with command processor")

