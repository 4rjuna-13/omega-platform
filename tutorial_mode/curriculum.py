CURRICULUM = {
    1: {
        "name": "Digital Literacy & Core Concepts", 
        "modules": [
            {"id": "cia_triad", "name": "CIA Security Triad", "type": "lesson", "file": "cia_triad_module.py"},
            {"id": "net_basics", "name": "How the Internet Works", "type": "lesson", "file": "network_basics.py"}
        ]
    },
    2: {
        "name": "The Defender's Toolkit", 
        "modules": [
            {"id": "cia_lab", "name": "CIA Triad Sandbox Lab", "type": "lab", "file": "cia_sandbox_lab.py"},
            {"id": "firewalls", "name": "Firewalls & Networks", "type": "lesson", "file": "firewall_basics.py"}
        ]
    },
    3: {
        "name": "Offensive Knowledge", 
        "modules": [
            {"id": "threat_model", "name": "Threat Modeling", "type": "lesson"},
            {"id": "vuln_basics", "name": "Vulnerability Basics", "type": "lesson"}
        ]
    },
    4: {
        "name": "Advanced Operations", 
        "modules": [
            {"id": "incident_response", "name": "Incident Response", "type": "lab"},
            {"id": "forensics", "name": "Digital Forensics", "type": "lab"},
            {"id": "threat_intel", "name": "Threat Intelligence", "type": "lesson"}
        ]
    },
    5: {
        "name": "Guru Level", 
        "modules": [
            {"id": "autonomous_design", "name": "Autonomous System Design", "type": "lesson"},
            {"id": "deception", "name": "Deception & Counterintel", "type": "lab"},
            {"id": "contributing", "name": "Contributing to the Field", "type": "lesson"}
        ]
    }
}

def get_path_for_level(level):
    """One-liner: Fetches the curriculum for a specific level."""
    return CURRICULUM.get(level, {"name": "Custom Expert Path", "modules": []})

def get_module(module_id):
    """Find a specific module by ID across all levels."""
    for level in CURRICULUM.values():
        for module in level.get("modules", []):
            if module.get("id") == module_id:
                return module
    return None
