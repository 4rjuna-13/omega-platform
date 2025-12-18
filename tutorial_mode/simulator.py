def launch_sandbox_exercise(module_name):
    """One-liner concept: Spins up an isolated environment for a specific learning module."""
    sandboxes = {
        "Network Analysis": "docker run --rm -it net_analysis_sandbox",
        "Log Investigation": "python3 -m tutorial_mode.sandboxes.log_lab",
        "Crypto Challenge": "python3 -m tutorial_mode.sandboxes.crypto_breaker"
    }
    command = sandboxes.get(module_name, f"echo 'Sandbox for {module_name} coming soon!'")
    return {"action": "start_sandbox", "command": command, "description": f"Practical lab for {module_name}"}
