#!/usr/bin/env python3
"""
Simplified Threat Intelligence Dashboard
No external dependencies beyond standard library
"""

import json
import uuid
from datetime import datetime, timedelta
import random
from collections import defaultdict
from enum import Enum
from typing import Dict, List, Any
import sys

class DataSource(Enum):
    THREAT_MODELING = "threat_modeling"
    PURPLE_TEAM = "purple_team"
    LOTL_SIMULATOR = "lotl_simulator"
    DECEPTION_TECH = "deception_tech"

class ThreatSeverity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatIndicator:
    def __init__(self, indicator_type: str, value: str, severity: ThreatSeverity, 
                 source: DataSource, metadata: Dict = None):
        self.id = str(uuid.uuid4())
        self.type = indicator_type
        self.value = value
        self.severity = severity
        self.source = source
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.confidence = 0.8
        self.metadata = metadata or {}
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "value": self.value,
            "severity": self.severity.value,
            "source": self.source.value,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "confidence": self.confidence,
            "metadata": self.metadata
        }

class SimpleDashboard:
    def __init__(self):
        self.indicators = []
        self.alerts = []
    
    def add_sample_data(self):
        """Add sample data for demonstration"""
        
        # Threat modeling data
        self.add_threat_modeling({
            "industry": "Healthcare",
            "vulnerabilities": 18,
            "risk_score": 8.2,
            "mitre_techniques": ["T1059", "T1566", "T1027", "T1486"]
        })
        
        # Purple team data
        self.add_purple_team({
            "exercise": "Ransomware Response",
            "team_size": 6,
            "findings": ["Slow detection time", "Poor containment"],
            "mitre_techniques": ["T1486", "T1490"]
        })
        
        # LotL data
        self.add_lotl({
            "technique": "PowerShell Empire",
            "risk": "high",
            "mitre": "T1059.001",
            "platform": "Windows"
        })
        
        # Deception data
        self.add_deception({
            "honeypots": 3,
            "tokens": 12,
            "engagements": 9,
            "watermarks_detected": 2
        })
    
    def add_threat_modeling(self, data: Dict):
        indicator = ThreatIndicator(
            "threat_model",
            f"Threat Model: {data.get('industry')}",
            ThreatSeverity.HIGH if data.get('risk_score', 0) > 7 else ThreatSeverity.MEDIUM,
            DataSource.THREAT_MODELING,
            data
        )
        self.indicators.append(indicator)
        
        # Create alert for high risk
        if data.get('risk_score', 0) > 7:
            self.alerts.append({
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "severity": "high",
                "title": f"High Risk: {data.get('industry')} Threat Model",
                "source": "Threat Modeler",
                "description": f"Risk score: {data.get('risk_score')}/10"
            })
    
    def add_purple_team(self, data: Dict):
        indicator = ThreatIndicator(
            "purple_team",
            f"Exercise: {data.get('exercise')}",
            ThreatSeverity.MEDIUM,
            DataSource.PURPLE_TEAM,
            data
        )
        self.indicators.append(indicator)
        
        self.alerts.append({
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "severity": "medium",
            "title": f"Exercise Complete: {data.get('exercise')}",
            "source": "Purple Team",
            "description": f"Team size: {data.get('team_size')}, Findings: {(len(data.get('findings')) if isinstance(data.get('findings'), (list, tuple)) else 0)}"
        })
    
    def add_lotl(self, data: Dict):
        indicator = ThreatIndicator(
            "lotl_technique",
            f"LotL: {data.get('technique')}",
            ThreatSeverity.HIGH if data.get('risk') == 'high' else ThreatSeverity.MEDIUM,
            DataSource.LOTL_SIMULATOR,
            data
        )
        self.indicators.append(indicator)
    
    def add_deception(self, data: Dict):
        engagements = data.get('engagements', 0)
        if engagements > 0:
            indicator = ThreatIndicator(
                "deception",
                f"Deception Engagements: {engagements}",
                ThreatSeverity.HIGH if engagements > 5 else ThreatSeverity.MEDIUM,
                DataSource.DECEPTION_TECH,
                data
            )
            self.indicators.append(indicator)
            
            self.alerts.append({
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "severity": "high" if engagements > 5 else "medium",
                "title": "Deception System Activity",
                "source": "Deception Tech",
                "description": f"{engagements} engagement(s) detected"
            })
    
    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        
        # Calculate statistics
        severity_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for indicator in self.indicators:
            severity_counts[indicator.severity.value] += 1
            source_counts[indicator.source.value] += 1
        
        # Recent indicators (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_indicators = [
            i for i in self.indicators 
            if i.last_seen > recent_cutoff
        ]
        
        # Extract MITRE techniques
        mitre_techniques = set()
        for indicator in self.indicators:
            if 'mitre_techniques' in indicator.metadata:
                mitre_techniques.update(indicator.metadata['mitre_techniques'])
            if 'mitre' in indicator.metadata:
                mitre_value = indicator.metadata['mitre']
                if isinstance(mitre_value, str):
                    mitre_techniques.add(mitre_value)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_indicators": len(self.indicators),
                "total_alerts": len(self.alerts),
                "recent_indicators": len(recent_indicators),
                "mitre_coverage": len(mitre_techniques)
            },
            "breakdowns": {
                "by_severity": dict(severity_counts),
                "by_source": dict(source_counts)
            },
            "recent_alerts": self.alerts[-5:] if self.alerts else [],
            "recent_indicators": [i.to_dict() for i in recent_indicators[-5:]],
            "mitre_techniques": list(mitre_techniques),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # High severity indicators
        high_critical = sum(
            1 for i in self.indicators 
            if i.severity in [ThreatSeverity.HIGH, ThreatSeverity.CRITICAL]
        )
        
        if high_critical > 3:
            recommendations.append({
                "priority": "high",
                "action": "Address high/critical severity threats",
                "details": f"{high_critical} high/critical indicators require immediate attention"
            })
        
        # Check for deception engagements
        deception_engagements = sum(
            1 for i in self.indicators 
            if i.type == "deception"
        )
        
        if deception_engagements > 0:
            recommendations.append({
                "priority": "medium",
                "action": "Investigate deception system alerts",
                "details": f"{deception_engagements} potential intrusion attempts detected"
            })
        
        # Check threat modeling coverage
        threat_models = sum(
            1 for i in self.indicators 
            if i.source == DataSource.THREAT_MODELING
        )
        
        if threat_models == 0:
            recommendations.append({
                "priority": "medium",
                "action": "Conduct threat modeling assessment",
                "details": "No threat modeling data available"
            })
        
        return recommendations
    
    def display_console_dashboard(self):
        """Display dashboard in console"""
        
        report = self.generate_report()
        
        print("\n" + "="*60)
        print("🚀 OMEGA PLATFORM - THREAT INTELLIGENCE DASHBOARD")
        print("="*60)
        
        print(f"\n📊 EXECUTIVE SUMMARY")
        print(f"   Generated: {report['generated_at'][11:19]}")
        print(f"   Total Indicators: {report['summary']['total_indicators']}")
        print(f"   Active Alerts: {report['summary']['total_alerts']}")
        print(f"   Recent Activity (24h): {report['summary']['recent_indicators']}")
        print(f"   MITRE ATT&CK Coverage: {report['summary']['mitre_coverage']}")
        
        print(f"\n⚠️  THREAT SEVERITY")
        severity_icons = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡', 
            'low': '🟢',
            'info': '🔵'
        }
        
        for severity, count in report['breakdowns']['by_severity'].items():
            icon = severity_icons.get(severity, '⚪')
            print(f"   {icon} {severity.upper():10} {count:3} indicators")
        
        print(f"\n📡 DATA SOURCES")
        source_icons = {
            'threat_modeling': '🎯',
            'purple_team': '👥',
            'lotl_simulator': '🛠️',
            'deception_tech': '🎣'
        }
        
        for source, count in report['breakdowns']['by_source'].items():
            icon = source_icons.get(source, '📊')
            source_name = source.replace('_', ' ').title()
            print(f"   {icon} {source_name:20} {count:3} indicators")
        
        print(f"\n🚨 RECENT ALERTS")
        if report['recent_alerts']:
            for alert in report['recent_alerts']:
                severity = alert.get('severity', 'info')
                icon = severity_icons.get(severity, '⚪')
                print(f"   {icon} [{severity.upper()}] {alert.get('title', 'Unknown')}")
                print(f"     Source: {alert.get('source', 'Unknown')}")
        else:
            print("   No recent alerts")
        
        print(f"\n🎯 MITRE ATT&CK DETECTED")
        if report['mitre_techniques']:
            techniques = ', '.join(report['mitre_techniques'][:8])
            print(f"   {techniques}")
            if len(report['mitre_techniques']) > 8:
                print(f"   ... and {len(report['mitre_techniques']) - 8} more")
        else:
            print("   No MITRE techniques detected")
        
        print(f"\n💡 RECOMMENDATIONS")
        if report['recommendations']:
            for rec in report['recommendations']:
                priority = rec.get('priority', 'medium')
                priority_icon = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(priority, '⚪')
                print(f"   {priority_icon} [{priority.upper()}] {rec.get('action', 'Unknown')}")
        else:
            print("   No recommendations at this time")
        
        print(f"\n" + "="*60)
        print("📈 NEXT STEPS:")
        print("   1. Review high severity threats")
        print("   2. Investigate deception engagements")
        print("   3. Update detection rules")
        print("   4. Schedule purple team exercises")
        print("="*60)
        
        return report

def demonstrate():
    """Run dashboard demonstration"""
    print("Starting Omega Platform Threat Intelligence Dashboard...")
    
    dashboard = SimpleDashboard()
    
    print("\n📥 Loading sample data from all components...")
    dashboard.add_sample_data()
    
    print("\n📈 Generating dashboard report...")
    report = dashboard.display_console_dashboard()
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"threat_dashboard_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Report saved to: {report_file}")
    
    # Generate simple HTML
    html_file = f"threat_dashboard_{timestamp}.html"
    with open(html_file, 'w') as f:
        f.write(generate_html_report(report))
    
    print(f"📄 HTML report saved to: {html_file}")
    
    return dashboard, report

def generate_html_report(report: Dict) -> str:
    """Generate simple HTML report"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Omega Platform - Threat Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .metric {{ display: inline-block; width: 200px; margin: 10px; padding: 15px; background: #f0f0f0; border-radius: 5px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #007acc; }}
        .severity {{ padding: 3px 8px; border-radius: 3px; margin: 2px; display: inline-block; }}
        .critical {{ background: #dc3545; color: white; }}
        .high {{ background: #fd7e14; color: white; }}
        .medium {{ background: #ffc107; }}
        .low {{ background: #28a745; color: white; }}
        .info {{ background: #17a2b8; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; }}
        th {{ background: #007acc; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Omega Platform - Threat Intelligence Dashboard</h1>
            <p>Generated: {report['generated_at']}</p>
        </div>
        
        <div style="text-align: center;">
            <div class="metric">
                <div>Total Indicators</div>
                <div class="metric-value">{report['summary']['total_indicators']}</div>
            </div>
            <div class="metric">
                <div>Active Alerts</div>
                <div class="metric-value">{report['summary']['total_alerts']}</div>
            </div>
            <div class="metric">
                <div>Recent Activity</div>
                <div class="metric-value">{report['summary']['recent_indicators']}</div>
            </div>
            <div class="metric">
                <div>MITRE Coverage</div>
                <div class="metric-value">{report['summary']['mitre_coverage']}</div>
            </div>
        </div>
        
        <h2>Threat Severity Breakdown</h2>
"""
    
    # Add severity breakdown
    for severity, count in report['breakdowns']['by_severity'].items():
        html += f"""
        <div>
            <span class="severity {severity}">{severity.upper()}</span>
            <span>{count} indicators</span>
        </div>
"""
    
    html += """
        <h2>Recent Alerts</h2>
        <table>
            <tr><th>Time</th><th>Severity</th><th>Title</th><th>Source</th></tr>
"""
    
    # Add alerts table
    for alert in report['recent_alerts']:
        time_str = alert['timestamp'][11:16] if 'timestamp' in alert else 'N/A'
        severity = alert.get('severity', 'info')
        html += f"""
            <tr>
                <td>{time_str}</td>
                <td><span class="severity {severity}">{severity.upper()}</span></td>
                <td>{alert.get('title', 'Unknown')}</td>
                <td>{alert.get('source', 'Unknown')}</td>
            </tr>
"""
    
    html += """
        </table>
        
        <h2>Recommendations</h2>
        <ul>
"""
    
    # Add recommendations
    for rec in report['recommendations']:
        priority = rec.get('priority', 'medium')
        html += f"""
            <li>
                <span class="severity {priority}">{priority.upper()}</span>
                {rec.get('action', 'Unknown')}
                <br><small>{rec.get('details', '')}</small>
            </li>
"""
    
    html += """
        </ul>
        
        <div style="text-align: center; margin-top: 40px; color: #666;">
            <p>Omega Platform - Advanced Security Testing Framework</p>
            <p>Generated automatically by the threat intelligence system</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    demonstrate()
