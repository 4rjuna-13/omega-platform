#!/usr/bin/env python3
"""
Simple Threat Dashboard for JAIDA-OMEGA-SAIOS
Provides basic threat visualization and reporting
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import random


class ThreatDashboard:
    """Simple threat dashboard for visualizing security data"""
    
    def __init__(self):
        self.iocs = []  # Indicator of Compromise storage
        self.threat_levels = ["Low", "Medium", "High", "Critical"]
        self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate sample IOC data for demonstration"""
        sample_iocs = [
            {
                "id": f"IOC-{i:04d}",
                "type": random.choice(["ip", "domain", "hash", "url"]),
                "value": self._generate_ioc_value(),
                "source": random.choice(["OMEGA Crawler", "JAIDA Intel", "External Feed"]),
                "confidence": random.randint(50, 100),
                "first_seen": (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat(),
                "last_seen": datetime.now().isoformat(),
                "severity": random.choice(["Low", "Medium", "High"])
            }
            for i in range(1, 21)
        ]
        self.iocs = sample_iocs
    
    def _generate_ioc_value(self) -> str:
        """Generate a sample IOC value"""
        ioc_type = random.choice(["ip", "domain", "hash", "url"])
        
        if ioc_type == "ip":
            return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        elif ioc_type == "domain":
            domains = ["malicious.com", "phishing-site.net", "c2-server.org", "exploit-kit.io"]
            return random.choice(domains)
        elif ioc_type == "hash":
            import hashlib
            return hashlib.md5(str(time.time()).encode()).hexdigest()
        else:  # url
            return f"https://{random.choice(['evil', 'malware', 'phish', 'attack'])}.com/{random.choice(['payload', 'exploit', 'loader', 'c2'])}.exe"
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive threat report"""
        # Calculate statistics
        recent_iocs = [ioc for ioc in self.iocs if ioc.get("severity") in ["High", "Critical"]]
        
        # Count by type
        type_counts = {}
        severity_counts = {}
        
        for ioc in self.iocs:
            ioc_type = ioc.get("type", "unknown")
            severity = ioc.get("severity", "unknown")
            
            type_counts[ioc_type] = type_counts.get(ioc_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Determine overall threat level
        if severity_counts.get("Critical", 0) > 0:
            threat_level = "Critical"
        elif severity_counts.get("High", 0) > 3:
            threat_level = "High"
        elif severity_counts.get("Medium", 0) > 5:
            threat_level = "Medium"
        else:
            threat_level = "Low"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "threat_level": threat_level,
            "total_iocs": len(self.iocs),
            "recent_iocs": recent_iocs[:10],  # Top 10 recent high/critical IOCs
            "type_distribution": type_counts,
            "severity_distribution": severity_counts,
            "top_sources": self._get_top_sources(),
            "recommendations": self._generate_recommendations(threat_level, severity_counts)
        }
    
    def _get_top_sources(self) -> List[Dict[str, Any]]:
        """Get top IOC sources"""
        source_counts = {}
        
        for ioc in self.iocs:
            source = ioc.get("source", "Unknown")
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Convert to list of dicts
        return [
            {"source": source, "count": count}
            for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ]
    
    def _generate_recommendations(self, threat_level: str, severity_counts: Dict) -> List[str]:
        """Generate recommendations based on threat level"""
        recommendations = []
        
        if threat_level in ["Critical", "High"]:
            recommendations.extend([
                "Immediate review of critical IOCs",
                "Isolate affected systems",
                "Increase monitoring on perimeter devices",
                "Notify incident response team"
            ])
        
        if severity_counts.get("High", 0) > 0:
            recommendations.extend([
                "Review firewall rules for IOCs",
                "Check SIEM for related alerts",
                "Update threat intelligence feeds"
            ])
        
        # Always include these
        recommendations.extend([
            "Regular IOC database maintenance",
            "Update signature databases",
            "Review security device logs"
        ])
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def add_ioc(self, ioc_data: Dict[str, Any]) -> str:
        """Add a new IOC to the dashboard"""
        ioc_id = f"IOC-{len(self.iocs) + 1:04d}"
        
        ioc_data["id"] = ioc_id
        ioc_data["first_seen"] = ioc_data.get("first_seen", datetime.now().isoformat())
        ioc_data["last_seen"] = datetime.now().isoformat()
        
        self.iocs.append(ioc_data)
        return ioc_id
    
    def get_ioc_by_id(self, ioc_id: str) -> Optional[Dict[str, Any]]:
        """Get IOC by ID"""
        for ioc in self.iocs:
            if ioc.get("id") == ioc_id:
                return ioc
        return None
    
    def search_iocs(self, query: str) -> List[Dict[str, Any]]:
        """Search IOCs by value, type, or source"""
        query = query.lower()
        results = []
        
        for ioc in self.iocs:
            if (query in ioc.get("value", "").lower() or
                query in ioc.get("type", "").lower() or
                query in ioc.get("source", "").lower() or
                query in ioc.get("severity", "").lower()):
                results.append(ioc)
        
        return results


def test_dashboard():
    """Test the threat dashboard"""
    print("🧪 Testing Threat Dashboard...")
    
    dashboard = ThreatDashboard()
    
    # Generate report
    report = dashboard.generate_report()
    
    print(f"✅ Dashboard generated successfully!")
    print(f"   Threat Level: {report['threat_level']}")
    print(f"   Total IOCs: {report['total_iocs']}")
    print(f"   Recent High/Critical IOCs: {len(report['recent_iocs'])}")
    
    # Test adding a new IOC
    new_ioc = {
        "type": "ip",
        "value": "192.168.1.100",
        "source": "Manual Entry",
        "confidence": 95,
        "severity": "High"
    }
    
    ioc_id = dashboard.add_ioc(new_ioc)
    print(f"✅ Added new IOC: {ioc_id}")
    
    # Test search
    search_results = dashboard.search_iocs("High")
    print(f"✅ Found {len(search_results)} high severity IOCs")
    
    return True


if __name__ == "__main__":
    test_dashboard()
