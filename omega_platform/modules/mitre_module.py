"""
Simple MITRE ATT&CK Module
"""

class MITREModule:
    def __init__(self):
        self.techniques = {
            "T1566": {
                "id": "T1566",
                "name": "Phishing",
                "description": "Adversaries send phishing messages",
                "tactics": ["Initial Access"],
                "mitigation": "User training, email filtering"
            },
            "T1486": {
                "id": "T1486",
                "name": "Data Encrypted for Impact", 
                "description": "Adversaries encrypt data",
                "tactics": ["Impact"],
                "mitigation": "Regular backups"
            }
        }
    
    def get_technique(self, tech_id):
        return self.techniques.get(tech_id, {})
    
    def get_all(self):
        return list(self.techniques.values())
    
    def get_stats(self):
        return {
            "total_techniques": len(self.techniques),
            "technique_ids": list(self.techniques.keys())
        }
