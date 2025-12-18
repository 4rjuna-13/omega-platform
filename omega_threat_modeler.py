#!/usr/bin/env python3
"""
OMEGA Threat Modeler Component
Advanced threat modeling and simulation capabilities
"""

import json
import time
import uuid
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class ThreatCategory(Enum):
    """Threat categories based on MITRE ATT&CK"""
    RECONNAISSANCE = "TA0043"
    RESOURCE_DEVELOPMENT = "TA0042"
    INITIAL_ACCESS = "TA0001"
    EXECUTION = "TA0002"
    PERSISTENCE = "TA0003"
    PRIVILEGE_ESCALATION = "TA0004"
    DEFENSE_EVASION = "TA0005"
    CREDENTIAL_ACCESS = "TA0006"
    DISCOVERY = "TA0007"
    LATERAL_MOVEMENT = "TA0008"
    COLLECTION = "TA0009"
    COMMAND_AND_CONTROL = "TA0011"
    EXFILTRATION = "TA0010"
    IMPACT = "TA0040"

class AttackVector(Enum):
    """Attack vectors for threat modeling"""
    NETWORK = "network"
    APPLICATION = "application"
    ENDPOINT = "endpoint"
    CLOUD = "cloud"
    MOBILE = "mobile"
    IOT = "iot"
    SUPPLY_CHAIN = "supply_chain"

class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Asset:
    """System asset for threat modeling"""
    
    def __init__(self, asset_id: str, name: str, asset_type: str, value: int):
        self.asset_id = asset_id
        self.name = name
        self.asset_type = asset_type
        self.value = value
        self.vulnerabilities = []
        self.threats = []
        self.protections = []
        self.created = datetime.now()
    
    def add_vulnerability(self, vuln_name: str, cvss_score: float, description: str) -> Dict:
        """Add vulnerability to asset"""
        vuln = {
            "id": f"VULN-{str(uuid.uuid4())[:8]}",
            "name": vuln_name,
            "cvss_score": cvss_score,
            "description": description,
            "discovered": datetime.now().isoformat(),
            "status": "open"
        }
        self.vulnerabilities.append(vuln)
        return vuln
    
    def add_threat(self, threat_name: str, category: ThreatCategory, 
                   attack_vector: AttackVector, risk: RiskLevel) -> Dict:
        """Add threat to asset"""
        threat = {
            "id": f"THREAT-{str(uuid.uuid4())[:8]}",
            "name": threat_name,
            "category": category.value,
            "category_name": category.name,
            "attack_vector": attack_vector.value,
            "risk_level": risk.value,
            "risk_label": risk.name,
            "added": datetime.now().isoformat(),
            "mitigations": []
        }
        self.threats.append(threat)
        return threat
    
    def add_protection(self, protection_name: str, protection_type: str) -> Dict:
        """Add protection to asset"""
        protection = {
            "id": f"PROT-{str(uuid.uuid4())[:8]}",
            "name": protection_name,
            "type": protection_type,
            "added": datetime.now().isoformat(),
            "effectiveness": random.randint(70, 95)
        }
        self.protections.append(protection)
        return protection
    
    def get_risk_score(self) -> float:
        """Calculate overall risk score for asset"""
        if not self.threats:
            return 0.0
        
        # Base risk from asset value
        base_risk = min(self.value / 10, 10)
        
        # Add risk from threats
        threat_risk = sum(t["risk_level"] for t in self.threats) / len(self.threats)
        
        # Subtract protection effectiveness
        protection_score = sum(p["effectiveness"] for p in self.protections) / 100
        protection_factor = max(0.1, 1.0 - (protection_score / 10))
        
        return round((base_risk + threat_risk) * protection_factor, 2)
    
    def to_dict(self) -> Dict:
        """Convert asset to dictionary"""
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "type": self.asset_type,
            "value": self.value,
            "risk_score": self.get_risk_score(),
            "vulnerabilities": len(self.vulnerabilities),
            "threats": len(self.threats),
            "protections": len(self.protections),
            "created": self.created.isoformat()
        }

class ThreatModel:
    """Complete threat model for a system or organization"""
    
    def __init__(self, model_id: str, name: str, description: str = ""):
        self.model_id = model_id
        self.name = name
        self.description = description
        self.assets = {}
        self.threat_actors = []
        self.attack_paths = []
        self.mitigations = []
        self.created = datetime.now()
        self.last_updated = datetime.now()
        self.graph = nx.DiGraph()
    
    def add_asset(self, asset: Asset) -> None:
        """Add asset to threat model"""
        self.assets[asset.asset_id] = asset
        self.graph.add_node(asset.asset_id, 
                           label=asset.name,
                           type=asset.asset_type,
                           risk=asset.get_risk_score())
        self.last_updated = datetime.now()
    
    def add_attack_path(self, source_asset_id: str, target_asset_id: str, 
                       technique: str, probability: float) -> Dict:
        """Add attack path between assets"""
        if source_asset_id not in self.assets or target_asset_id not in self.assets:
            raise ValueError("Source or target asset not found")
        
        path_id = f"PATH-{str(uuid.uuid4())[:8]}"
        path = {
            "path_id": path_id,
            "source": source_asset_id,
            "target": target_asset_id,
            "technique": technique,
            "probability": probability,
            "created": datetime.now().isoformat()
        }
        
        self.attack_paths.append(path)
        
        # Add edge to graph
        self.graph.add_edge(source_asset_id, target_asset_id,
                           technique=technique,
                           probability=probability,
                           path_id=path_id)
        
        self.last_updated = datetime.now()
        return path
    
    def add_threat_actor(self, name: str, sophistication: str, 
                        motivation: str, resources: str) -> Dict:
        """Add threat actor to model"""
        actor = {
            "id": f"ACTOR-{str(uuid.uuid4())[:8]}",
            "name": name,
            "sophistication": sophistication,
            "motivation": motivation,
            "resources": resources,
            "added": datetime.now().isoformat(),
            "targeted_assets": []
        }
        self.threat_actors.append(actor)
        return actor
    
    def calculate_attack_surface(self) -> Dict:
        """Calculate total attack surface"""
        total_assets = len(self.assets)
        total_vulnerabilities = sum(len(a.vulnerabilities) for a in self.assets.values())
        total_threats = sum(len(a.threats) for a in self.assets.values())
        
        # Calculate average risk
        risk_scores = [a.get_risk_score() for a in self.assets.values()]
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        # Calculate attack paths complexity
        path_complexity = len(self.attack_paths)
        
        return {
            "total_assets": total_assets,
            "total_vulnerabilities": total_vulnerabilities,
            "total_threats": total_threats,
            "average_risk": round(avg_risk, 2),
            "attack_paths": path_complexity,
            "attack_surface_score": round((avg_risk * path_complexity) / 10, 2)
        }
    
    def generate_attack_graph(self) -> nx.DiGraph:
        """Generate
cat > omega_threat_modeler.py << 'EOF'
#!/usr/bin/env python3
"""
OMEGA Threat Modeler Component
Advanced threat modeling and simulation capabilities
"""

import json
import time
import uuid
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

class ThreatCategory(Enum):
    """Threat categories based on MITRE ATT&CK"""
    RECONNAISSANCE = "TA0043"
    RESOURCE_DEVELOPMENT = "TA0042"
    INITIAL_ACCESS = "TA0001"
    EXECUTION = "TA0002"
    PERSISTENCE = "TA0003"
    PRIVILEGE_ESCALATION = "TA0004"
    DEFENSE_EVASION = "TA0005"
    CREDENTIAL_ACCESS = "TA0006"
    DISCOVERY = "TA0007"
    LATERAL_MOVEMENT = "TA0008"
    COLLECTION = "TA0009"
    COMMAND_AND_CONTROL = "TA0011"
    EXFILTRATION = "TA0010"
    IMPACT = "TA0040"

class AttackVector(Enum):
    """Attack vectors for threat modeling"""
    NETWORK = "network"
    APPLICATION = "application"
    ENDPOINT = "endpoint"
    CLOUD = "cloud"
    MOBILE = "mobile"
    IOT = "iot"
    SUPPLY_CHAIN = "supply_chain"

class RiskLevel(Enum):
    """Risk assessment levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Asset:
    """System asset for threat modeling"""
    
    def __init__(self, asset_id: str, name: str, asset_type: str, value: int):
        self.asset_id = asset_id
        self.name = name
        self.asset_type = asset_type
        self.value = value
        self.vulnerabilities = []
        self.threats = []
        self.protections = []
        self.created = datetime.now()
    
    def add_vulnerability(self, vuln_name: str, cvss_score: float, description: str) -> Dict:
        """Add vulnerability to asset"""
        vuln = {
            "id": f"VULN-{str(uuid.uuid4())[:8]}",
            "name": vuln_name,
            "cvss_score": cvss_score,
            "description": description,
            "discovered": datetime.now().isoformat(),
            "status": "open"
        }
        self.vulnerabilities.append(vuln)
        return vuln
    
    def add_threat(self, threat_name: str, category: ThreatCategory, 
                   attack_vector: AttackVector, risk: RiskLevel) -> Dict:
        """Add threat to asset"""
        threat = {
            "id": f"THREAT-{str(uuid.uuid4())[:8]}",
            "name": threat_name,
            "category": category.value,
            "category_name": category.name,
            "attack_vector": attack_vector.value,
            "risk_level": risk.value,
            "risk_label": risk.name,
            "added": datetime.now().isoformat(),
            "mitigations": []
        }
        self.threats.append(threat)
        return threat
    
    def add_protection(self, protection_name: str, protection_type: str) -> Dict:
        """Add protection to asset"""
        protection = {
            "id": f"PROT-{str(uuid.uuid4())[:8]}",
            "name": protection_name,
            "type": protection_type,
            "added": datetime.now().isoformat(),
            "effectiveness": random.randint(70, 95)
        }
        self.protections.append(protection)
        return protection
    
    def get_risk_score(self) -> float:
        """Calculate overall risk score for asset"""
        if not self.threats:
            return 0.0
        
        # Base risk from asset value
        base_risk = min(self.value / 10, 10)
        
        # Add risk from threats
        threat_risk = sum(t["risk_level"] for t in self.threats) / len(self.threats)
        
        # Subtract protection effectiveness
        protection_score = sum(p["effectiveness"] for p in self.protections) / 100
        protection_factor = max(0.1, 1.0 - (protection_score / 10))
        
        return round((base_risk + threat_risk) * protection_factor, 2)
    
    def to_dict(self) -> Dict:
        """Convert asset to dictionary"""
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "type": self.asset_type,
            "value": self.value,
            "risk_score": self.get_risk_score(),
            "vulnerabilities": len(self.vulnerabilities),
            "threats": len(self.threats),
            "protections": len(self.protections),
            "created": self.created.isoformat()
        }

class ThreatModel:
    """Complete threat model for a system or organization"""
    
    def __init__(self, model_id: str, name: str, description: str = ""):
        self.model_id = model_id
        self.name = name
        self.description = description
        self.assets = {}
        self.threat_actors = []
        self.attack_paths = []
        self.mitigations = []
        self.created = datetime.now()
        self.last_updated = datetime.now()
        self.graph = nx.DiGraph()
    
    def add_asset(self, asset: Asset) -> None:
        """Add asset to threat model"""
        self.assets[asset.asset_id] = asset
        self.graph.add_node(asset.asset_id, 
                           label=asset.name,
                           type=asset.asset_type,
                           risk=asset.get_risk_score())
        self.last_updated = datetime.now()
    
    def add_attack_path(self, source_asset_id: str, target_asset_id: str, 
                       technique: str, probability: float) -> Dict:
        """Add attack path between assets"""
        if source_asset_id not in self.assets or target_asset_id not in self.assets:
            raise ValueError("Source or target asset not found")
        
        path_id = f"PATH-{str(uuid.uuid4())[:8]}"
        path = {
            "path_id": path_id,
            "source": source_asset_id,
            "target": target_asset_id,
            "technique": technique,
            "probability": probability,
            "created": datetime.now().isoformat()
        }
        
        self.attack_paths.append(path)
        
        # Add edge to graph
        self.graph.add_edge(source_asset_id, target_asset_id,
                           technique=technique,
                           probability=probability,
                           path_id=path_id)
        
        self.last_updated = datetime.now()
        return path
    
    def add_threat_actor(self, name: str, sophistication: str, 
                        motivation: str, resources: str) -> Dict:
        """Add threat actor to model"""
        actor = {
            "id": f"ACTOR-{str(uuid.uuid4())[:8]}",
            "name": name,
            "sophistication": sophistication,
            "motivation": motivation,
            "resources": resources,
            "added": datetime.now().isoformat(),
            "targeted_assets": []
        }
        self.threat_actors.append(actor)
        return actor
    
    def calculate_attack_surface(self) -> Dict:
        """Calculate total attack surface"""
        total_assets = len(self.assets)
        total_vulnerabilities = sum(len(a.vulnerabilities) for a in self.assets.values())
        total_threats = sum(len(a.threats) for a in self.assets.values())
        
        # Calculate average risk
        risk_scores = [a.get_risk_score() for a in self.assets.values()]
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        
        # Calculate attack paths complexity
        path_complexity = len(self.attack_paths)
        
        return {
            "total_assets": total_assets,
            "total_vulnerabilities": total_vulnerabilities,
            "total_threats": total_threats,
            "average_risk": round(avg_risk, 2),
            "attack_paths": path_complexity,
            "attack_surface_score": round((avg_risk * path_complexity) / 10, 2)
        }
    
    def generate_attack_graph(self) -> nx.DiGraph:
        """Generate attack graph from model"""
        return self.graph.copy()
    
    def find_critical_paths(self, limit: int = 5) -> List[Dict]:
        """Find most critical attack paths"""
        critical_paths = []
        
        for path in self.attack_paths:
            source_asset = self.assets[path["source"]]
            target_asset = self.assets[path["target"]]
            
            # Calculate path criticality
            criticality = (
                source_asset.get_risk_score() * 0.3 +
                target_asset.get_risk_score() * 0.4 +
                path["probability"] * 0.3
            )
            
            critical_paths.append({
                **path,
                "criticality": round(criticality, 2),
                "source_name": source_asset.name,
                "target_name": target_asset.name
            })
        
        # Sort by criticality and return top N
        critical_paths.sort(key=lambda x: x["criticality"], reverse=True)
        return critical_paths[:limit]
    
    def generate_report(self) -> Dict:
        """Generate comprehensive threat model report"""
        attack_surface = self.calculate_attack_surface()
        critical_paths = self.find_critical_paths(5)
        
        return {
            "model_id": self.model_id,
            "name": self.name,
            "description": self.description,
            "created": self.created.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "attack_surface": attack_surface,
            "assets": {aid: asset.to_dict() for aid, asset in self.assets.items()},
            "threat_actors": len(self.threat_actors),
            "critical_paths": critical_paths,
            "mitigations": len(self.mitigations),
            "summary": {
                "overall_risk": attack_surface["average_risk"],
                "risk_level": self._get_risk_level(attack_surface["average_risk"]),
                "recommendations": self._generate_recommendations(attack_surface, critical_paths)
            }
        }
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level from score"""
        if risk_score >= 7.5:
            return "CRITICAL"
        elif risk_score >= 5.0:
            return "HIGH"
        elif risk_score >= 2.5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendations(self, attack_surface: Dict, critical_paths: List[Dict]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if attack_surface["average_risk"] >= 5.0:
            recommendations.append("Immediate remediation needed for high-risk assets")
        
        if attack_surface["total_vulnerabilities"] > 10:
            recommendations.append(f"Prioritize fixing {attack_surface['total_vulnerabilities']} vulnerabilities")
        
        if critical_paths:
            recommendations.append(f"Monitor {len(critical_paths)} critical attack paths")
        
        if attack_surface["attack_paths"] > 20:
            recommendations.append("Reduce attack surface by segmenting network")
        
        # Always include these
        recommendations.extend([
            "Implement multi-factor authentication",
            "Regular security awareness training",
            "Continuous vulnerability assessment",
            "Incident response plan testing"
        ])
        
        return recommendations[:5]  # Return top 5

class ThreatModeler:
    """OMEGA Threat Modeler - Main component for threat modeling operations"""
    
    def __init__(self):
        self.name = "OMEGA Threat Modeler"
        self.version = "1.0.0"
        self.models = {}
        self.templates = self._load_templates()
        self.last_operation = datetime.now()
    
    def _load_templates(self) -> Dict:
        """Load threat modeling templates"""
        return {
            "web_application": {
                "name": "Web Application Template",
                "description": "Template for web application threat modeling",
                "assets": [
                    {"name": "Web Server", "type": "server", "value": 8},
                    {"name": "Database", "type": "database", "value": 9},
                    {"name": "Load Balancer", "type": "network", "value": 6},
                    {"name": "Admin Panel", "type": "application", "value": 7}
                ],
                "threats": [
                    {"name": "SQL Injection", "category": ThreatCategory.INITIAL_ACCESS},
                    {"name": "XSS Attack", "category": ThreatCategory.EXECUTION},
                    {"name": "Brute Force", "category": ThreatCategory.CREDENTIAL_ACCESS}
                ]
            },
            "enterprise_network": {
                "name": "Enterprise Network Template",
                "description": "Template for enterprise network threat modeling",
                "assets": [
                    {"name": "Active Directory", "type": "directory", "value": 10},
                    {"name": "File Server", "type": "server", "value": 7},
                    {"name": "Email Server", "type": "server", "value": 8},
                    {"name": "Firewall", "type": "network", "value": 6}
                ],
                "threats": [
                    {"name": "Credential Theft", "category": ThreatCategory.CREDENTIAL_ACCESS},
                    {"name": "Lateral Movement", "category": ThreatCategory.LATERAL_MOVEMENT},
                    {"name": "Data Exfiltration", "category": ThreatCategory.EXFILTRATION}
                ]
            }
        }
    
    def create_model(self, name: str, description: str = "", 
                    template: str = None) -> ThreatModel:
        """Create a new threat model"""
        model_id = f"TM-{str(uuid.uuid4())[:8]}"
        model = ThreatModel(model_id, name, description)
        
        # Apply template if specified
        if template and template in self.templates:
            template_data = self.templates[template]
            self._apply_template(model, template_data)
        
        self.models[model_id] = model
        self.last_operation = datetime.now()
        
        print(f"✅ Created threat model: {name} ({model_id})")
        return model
    
    def _apply_template(self, model: ThreatModel, template: Dict) -> None:
        """Apply template to threat model"""
        for asset_data in template["assets"]:
            asset = Asset(
                f"ASSET-{str(uuid.uuid4())[:8]}",
                asset_data["name"],
                asset_data["type"],
                asset_data["value"]
            )
            
            # Add template threats
            for threat_data in template["threats"]:
                asset.add_threat(
                    threat_data["name"],
                    threat_data["category"],
                    AttackVector.NETWORK,
                    RiskLevel.HIGH if asset_data["value"] >= 8 else RiskLevel.MEDIUM
                )
            
            model.add_asset(asset)
        
        print(f"   Applied template: {template['name']}")
    
    def analyze_model(self, model_id: str) -> Dict:
        """Analyze threat model and generate insights"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        report = model.generate_report()
        
        # Generate additional insights
        insights = {
            "top_risky_assets": self._get_top_risky_assets(model, 3),
            "attack_surface_trend": "increasing" if report["attack_surface"]["attack_surface_score"] > 5 else "stable",
            "recommended_actions": report["summary"]["recommendations"],
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return {
            "report": report,
            "insights": insights,
            "model_id": model_id,
            "analysis_complete": True
        }
    
    def _get_top_risky_assets(self, model: ThreatModel, limit: int = 3) -> List[Dict]:
        """Get top risky assets from model"""
        assets_with_risk = [
            {
                "asset_id": aid,
                "name": asset.name,
                "risk_score": asset.get_risk_score(),
                "threats": len(asset.threats)
            }
            for aid, asset in model.assets.items()
        ]
        
        assets_with_risk.sort(key=lambda x: x["risk_score"], reverse=True)
        return assets_with_risk[:limit]
    
    def get_status(self) -> Dict:
        """Get threat modeler status"""
        return {
            "component": self.name,
            "version": self.version,
            "status": "operational",
            "total_models": len(self.models),
            "available_templates": len(self.templates),
            "last_operation": self.last_operation.isoformat(),
            "capabilities": [
                "Asset-based threat modeling",
                "Attack path analysis",
                "Risk scoring and prioritization",
                "Template-based modeling",
                "Comprehensive reporting"
            ]
        }

def test_threat_modeler():
    """Test the OMEGA Threat Modeler"""
    print("🧪 Testing OMEGA Threat Modeler...")
    
    try:
        # Initialize threat modeler
        modeler = ThreatModeler()
        print("   ✅ Threat Modeler initialized")
        
        # Create a threat model using template
        model = modeler.create_model(
            "Test Web Application",
            "Threat model for test web application",
            template="web_application"
        )
        
        print(f"   📋 Model created: {model.name}")
        print(f"   🏗️  Assets in model: {len(model.assets)}")
        
        # Add some custom assets and threats
        custom_asset = Asset(
            "ASSET-CUSTOM-001",
            "API Gateway",
            "application",
            value=8
        )
        
        custom_asset.add_vulnerability(
            "API Key Exposure",
            cvss_score=7.5,
            description="API keys exposed in client-side code"
        )
        
        custom_asset.add_threat(
            "API Abuse",
            ThreatCategory.INITIAL_ACCESS,
            AttackVector.APPLICATION,
            RiskLevel.HIGH
        )
        
        model.add_asset(custom_asset)
        
        # Add attack paths
        model.add_attack_path(
            "ASSET-CUSTOM-001",
            list(model.assets.keys())[0],  # First asset
            "Credential Stuffing",
            probability=0.65
        )
        
        print(f"   🔗 Attack paths created: {len(model.attack_paths)}")
        
        # Analyze the model
        analysis = modeler.analyze_model(model.model_id)
        report = analysis["report"]
        
        print(f"   📊 Analysis complete:")
        print(f"      Overall risk: {report['summary']['overall_risk']}")
        print(f"      Risk level: {report['summary']['risk_level']}")
        print(f"      Attack surface score: {report['attack_surface']['attack_surface_score']}")
        
        # Show top risky assets
        insights = analysis["insights"]
        print(f"   🎯 Top risky assets:")
        for asset in insights["top_risky_assets"]:
            print(f"      • {asset['name']}: Risk {asset['risk_score']} ({asset['threats']} threats)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_threat_modeler()
    if success:
        print("\n✅ OMEGA Threat Modeler test passed!")
    else:
        print("\n❌ OMEGA Threat Modeler test failed!")
