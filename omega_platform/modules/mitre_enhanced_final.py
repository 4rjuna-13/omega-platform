"""
Enhanced MITRE Module with all techniques from scenarios
"""
import json
from pathlib import Path

class MITREModuleEnhanced:
    def __init__(self):
        self.data_dir = Path("omega_platform/data/mitre_attack")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.techniques = self._load_techniques()
    
    def _load_techniques(self):
        """Load techniques with all known mappings"""
        techniques = {
            "T1566": {
                "id": "T1566",
                "name": "Phishing",
                "description": "Adversaries send phishing messages to gain access",
                "tactics": ["Initial Access"],
                "mitigation": "User training, email filtering"
            },
            "T1486": {
                "id": "T1486",
                "name": "Data Encrypted for Impact",
                "description": "Adversaries encrypt data to disrupt availability",
                "tactics": ["Impact"],
                "mitigation": "Regular backups"
            },
            "T1190": {
                "id": "T1190",
                "name": "Exploit Public-Facing Application",
                "description": "Adversaries exploit vulnerabilities in internet-facing systems",
                "tactics": ["Initial Access"],
                "mitigation": "Patching, WAF"
            },
            "T1059": {
                "id": "T1059",
                "name": "Command and Scripting Interpreter",
                "description": "Adversaries abuse command and scripting interpreters",
                "tactics": ["Execution"],
                "mitigation": "Restrict scripting, application whitelisting"
            },
            "T1210": {
                "id": "T1210",
                "name": "Exploitation of Remote Services",
                "description": "Adversaries exploit remote services to gain access",
                "tactics": ["Lateral Movement"],
                "mitigation": "Network segmentation, patching"
            },
            "T1490": {
                "id": "T1490",
                "name": "Inhibit System Recovery",
                "description": "Adversaries delete backups to prevent recovery",
                "tactics": ["Impact"],
                "mitigation": "Offsite backups, immutable storage"
            },
            "T1566.001": {
                "id": "T1566.001",
                "name": "Spearphishing Attachment",
                "description": "Spearphishing with malicious attachments",
                "tactics": ["Initial Access"],
                "mitigation": "Attachment filtering, sandboxing"
            }
        }
        
        # Save to file
        techniques_file = self.data_dir / "techniques_enhanced.json"
        with open(techniques_file, 'w') as f:
            json.dump(techniques, f, indent=2)
        
        return techniques
    
    def get_technique(self, tech_id):
        return self.techniques.get(tech_id, {
            "id": tech_id,
            "name": f"Technique {tech_id}",
            "tactics": ["Unknown"],
            "description": "No description available"
        })
    
    def get_all(self):
        return list(self.techniques.values())
    
    def get_stats(self):
        return {
            "total_techniques": len(self.techniques),
            "tactics_covered": len(set().union(*[t.get('tactics', []) for t in self.techniques.values()])),
            "technique_ids": list(self.techniques.keys())
        }
    
    def get_techniques_by_tactic(self, tactic):
        return [t for t in self.techniques.values() if tactic in t.get('tactics', [])]
