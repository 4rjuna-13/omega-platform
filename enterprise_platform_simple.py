#!/usr/bin/env python3
"""
Enterprise Platform - Simple Version
Core components for enterprise-level threat intelligence and orchestration
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import threading
from queue import Queue
import random


class EnterpriseThreatOrchestrator:
    """Orchestrates enterprise-wide threat detection and response"""
    
    def __init__(self, enterprise_name: str = "JAIDA-OMEGA"):
        self.enterprise_name = enterprise_name
        self.assets = {}
        self.threat_feeds = []
        self.response_actions = Queue()
        self.active_incidents = []
        self.incident_counter = 1000
        
        # Initialize core components
        self._load_default_assets()
        self._setup_default_feeds()
        
    def _load_default_assets(self):
        """Load default enterprise assets"""
        self.assets = {
            "network_segments": [
                {"name": "Corporate LAN", "cidr": "10.0.0.0/16", "risk": "Low"},
                {"name": "DMZ", "cidr": "192.168.1.0/24", "risk": "High"},
                {"name": "Executive VLAN", "cidr": "172.16.1.0/24", "risk": "Critical"}
            ],
            "critical_servers": [
                {"name": "DC-01", "ip": "10.0.0.10", "role": "Domain Controller"},
                {"name": "FS-01", "ip": "10.0.0.20", "role": "File Server"},
                {"name": "WEB-01", "ip": "192.168.1.100", "role": "Web Server"}
            ],
            "security_devices": [
                {"name": "FW-01", "type": "Firewall", "model": "Palo Alto PA-3200"},
                {"name": "IDS-01", "type": "Intrusion Detection", "model": "Snort"},
                {"name": "SIEM-01", "type": "SIEM", "model": "Splunk Enterprise"}
            ]
        }
    
    def _setup_default_feeds(self):
        """Setup default threat intelligence feeds"""
        self.threat_feeds = [
            {
                "name": "OMEGA IOC Feed",
                "url": "internal://omega/ioc-feed",
                "type": "internal",
                "update_frequency": 300  # 5 minutes
            },
            {
                "name": "JAIDA Threat Intel",
                "url": "internal://jaida/threat-intel",
                "type": "internal",
                "update_frequency": 600  # 10 minutes
            },
            {
                "name": "External CTI Feed",
                "url": "https://cti.jaida-omega.com/feed",
                "type": "external",
                "update_frequency": 3600  # 1 hour
            }
        ]
    
    def detect_threat(self, ioc_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect threats based on IOCs"""
        if not ioc_data:
            return None
            
        threat_score = 0
        matched_assets = []
        
        # Check against network segments
        for segment in self.assets["network_segments"]:
            if self._ip_in_cidr(ioc_data.get("ip", ""), segment["cidr"]):
                threat_score += 10
                matched_assets.append(f"Network: {segment['name']}")
        
        # Check against critical servers
        for server in self.assets["critical_servers"]:
            if ioc_data.get("ip") == server["ip"]:
                threat_score += 50
                matched_assets.append(f"Server: {server['name']}")
        
        # Create incident if threat score is significant
        if threat_score > 20:
            incident = self._create_incident(ioc_data, threat_score, matched_assets)
            self.active_incidents.append(incident)
            return incident
        
        return None
    
    def _ip_in_cidr(self, ip: str, cidr: str) -> bool:
        """Simple CIDR check (simplified for demo)"""
        # In real implementation, use ipaddress module
        return True  # Placeholder
    
    def _create_incident(self, ioc_data: Dict, score: int, assets: List[str]) -> Dict[str, Any]:
        """Create a new incident"""
        self.incident_counter += 1
        
        incident = {
            "id": f"INC-{self.incident_counter}",
            "timestamp": datetime.now().isoformat(),
            "severity": "HIGH" if score > 50 else "MEDIUM" if score > 20 else "LOW",
            "score": score,
            "ioc": ioc_data,
            "affected_assets": assets,
            "status": "OPEN",
            "assigned_to": None,
            "actions_taken": [],
            "recommendations": self._generate_recommendations(score, assets)
        }
        
        # Queue for response actions
        self.response_actions.put({
            "type": "NEW_INCIDENT",
            "incident_id": incident["id"],
            "severity": incident["severity"],
            "timestamp": incident["timestamp"]
        })
        
        return incident
    
    def _generate_recommendations(self, score: int, assets: List[str]) -> List[str]:
        """Generate response recommendations"""
        recommendations = []
        
        if score > 50:
            recommendations.extend([
                "Immediate isolation of affected assets",
                "Full traffic capture on affected segments",
                "Escalate to SOC Level 3",
                "Notify CISO and legal team"
            ])
        elif score > 20:
            recommendations.extend([
                "Monitor affected assets closely",
                "Review firewall rules for suspicious traffic",
                "Check for lateral movement",
                "Update threat intelligence feeds"
            ])
        else:
            recommendations.extend([
                "Log and monitor",
                "Add to watchlist",
                "Update baseline behavior"
            ])
        
        return recommendations
    
    def get_incident_report(self) -> Dict[str, Any]:
        """Generate incident report"""
        open_incidents = [i for i in self.active_incidents if i["status"] == "OPEN"]
        closed_incidents = [i for i in self.active_incidents if i["status"] == "CLOSED"]
        
        return {
            "enterprise": self.enterprise_name,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_incidents": len(self.active_incidents),
                "open_incidents": len(open_incidents),
                "closed_incidents": len(closed_incidents),
                "high_severity": len([i for i in open_incidents if i["severity"] == "HIGH"]),
                "pending_actions": self.response_actions.qsize()
            },
            "recent_incidents": open_incidents[:5],  # Last 5 open incidents
            "assets_at_risk": list(set(
                asset for incident in open_incidents 
                for asset in incident.get("affected_assets", [])
            )),
            "recommendations": [
                rec for incident in open_incidents 
                for rec in incident.get("recommendations", [])
            ][:10]  # Top 10 recommendations
        }
    
    def simulate_threat(self) -> Dict[str, Any]:
        """Simulate a threat for testing"""
        simulated_ioc = {
            "id": f"SIM-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
            "timestamp": datetime.now().isoformat(),
            "type": random.choice(["malware", "phishing", "recon", "lateral_movement"]),
            "ip": f"10.0.0.{random.randint(100, 200)}",
            "indicator": random.choice([
                "Known malware hash",
                "Suspicious domain",
                "Anomalous traffic pattern",
                "Privilege escalation attempt"
            ]),
            "confidence": random.randint(70, 100)
        }
        
        return self.detect_threat(simulated_ioc)


class EnterpriseDashboard:
    """Enterprise-level dashboard"""
    
    def __init__(self, orchestrator: EnterpriseThreatOrchestrator):
        self.orchestrator = orchestrator
        self.metrics_history = []
        
    def generate_dashboard(self) -> Dict[str, Any]:
        """Generate complete dashboard"""
        report = self.orchestrator.get_incident_report()
        
        dashboard = {
            "enterprise": report["enterprise"],
            "timestamp": report["timestamp"],
            "overview": {
                "threat_level": self._calculate_threat_level(report),
                "security_posture": self._calculate_security_posture(),
                "compliance_score": random.randint(85, 98)
            },
            "metrics": {
                "mttd": random.randint(5, 30),  # Mean Time to Detect (minutes)
                "mttr": random.randint(60, 240),  # Mean Time to Respond (minutes)
                "threats_blocked": random.randint(100, 1000),
                "false_positives": random.randint(5, 20)
            },
            "incidents": report,
            "active_feeds": len(self.orchestrator.threat_feeds),
            "asset_coverage": self._calculate_asset_coverage()
        }
        
        # Store in history
        self.metrics_history.append({
            "timestamp": dashboard["timestamp"],
            "threat_level": dashboard["overview"]["threat_level"],
            "open_incidents": dashboard["incidents"]["summary"]["open_incidents"]
        })
        
        return dashboard
    
    def _calculate_threat_level(self, report: Dict[str, Any]) -> str:
        """Calculate current threat level"""
        open_incidents = report["summary"]["open_incidents"]
        high_severity = report["summary"]["high_severity"]
        
        if high_severity > 3:
            return "CRITICAL"
        elif high_severity > 0:
            return "HIGH"
        elif open_incidents > 5:
            return "ELEVATED"
        else:
            return "NORMAL"
    
    def _calculate_security_posture(self) -> str:
        """Calculate security posture"""
        scores = {
            "network_segmentation": random.randint(70, 95),
            "endpoint_protection": random.randint(80, 98),
            "access_control": random.randint(75, 92),
            "monitoring": random.randint(85, 99)
        }
        avg_score = sum(scores.values()) / len(scores)
        
        if avg_score > 90:
            return "STRONG"
        elif avg_score > 75:
            return "ADEQUATE"
        else:
            return "WEAK"
    
    def _calculate_asset_coverage(self) -> float:
        """Calculate percentage of assets covered by monitoring"""
        total_assets = (
            len(self.orchestrator.assets["network_segments"]) +
            len(self.orchestrator.assets["critical_servers"]) +
            len(self.orchestrator.assets["security_devices"])
        )
        covered = total_assets * 0.85  # 85% coverage for demo
        return round((covered / total_assets) * 100, 2) if total_assets > 0 else 0.0


def test_enterprise_platform():
    """Test the enterprise platform"""
    print("🧪 Testing Enterprise Platform...")
    
    # Create orchestrator
    orchestrator = EnterpriseThreatOrchestrator("JAIDA-OMEGA Corp")
    
    # Create dashboard
    dashboard = EnterpriseDashboard(orchestrator)
    
    # Simulate some threats
    print("  Simulating threats...")
    for _ in range(3):
        incident = orchestrator.simulate_threat()
        if incident:
            print(f"    Detected: {incident['id']} - {incident['severity']}")
    
    # Generate dashboard
    print("  Generating dashboard...")
    dash_data = dashboard.generate_dashboard()
    
    print(f"\n✅ Enterprise Platform Test Complete!")
    print(f"   Enterprise: {dash_data['enterprise']}")
    print(f"   Threat Level: {dash_data['overview']['threat_level']}")
    print(f"   Open Incidents: {dash_data['incidents']['summary']['open_incidents']}")
    print(f"   Security Posture: {dash_data['overview']['security_posture']}")
    
    return True


if __name__ == "__main__":
    test_enterprise_platform()
