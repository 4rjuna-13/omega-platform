"""
Threat Intelligence Dashboard - Standalone Python Script
Run with: python3 threat_intelligence_dashboard.py
"""

import json
import uuid
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random
from collections import defaultdict, Counter
from enum import Enum

# Define enums first
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

@dataclass
class ThreatIndicator:
    id: str
    type: str
    value: str
    severity: ThreatSeverity
    first_seen: datetime
    last_seen: datetime
    confidence: float
    source: DataSource
    related_entities: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "value": self.value,
            "severity": self.severity.value,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "confidence": self.confidence,
            "source": self.source.value,
            "related_entities": self.related_entities,
            "tags": self.tags,
            "metadata": self.metadata
        }

class SimpleDashboard:
    """Simplified threat intelligence dashboard"""
    
    def __init__(self):
        self.indicators = []
        self.alerts = []
        self.data_sources = {}
        
    def add_sample_data(self):
        """Add sample data for demonstration"""
        
        # Sample threat modeling data
        self.add_threat_modeling_data({
            "industry": "healthcare",
            "vulnerabilities": 15,
            "risk_score": 7.8,
            "mitre_techniques": ["T1059", "T1566", "T1027"]
        })
        
        # Sample purple team data
        self.add_purple_team_data({
            "exercise_name": "Ransomware Defense",
            "findings": ["SSH brute force detected", "Data exfiltration attempt"],
            "mitre_techniques": ["T1110", "T1048"]
        })
        
        # Sample LotL data
        self.add_lotl_data({
            "technique": "PowerShell Execution",
            "risk": "high",
            "mitre": "T1059.001"
        })
        
        # Sample deception data
        self.add_deception_data({
            "honeypot_hits": 8,
            "token_triggers": 3,
            "decoy_accesses": 5
        })
    
    def add_threat_modeling_data(self, data):
        """Add threat modeling data"""
        indicator = ThreatIndicator(
            id=str(uuid.uuid4()),
            type="threat_model",
            value=f"Threat model: {data.get('industry', 'Unknown')} industry",
            severity=ThreatSeverity.HIGH if data.get('risk_score', 0) > 7 else ThreatSeverity.MEDIUM,
            first_seen=datetime.now(),
            last_seen=datetime.now(),
            confidence=0.85,
            source=DataSource.THREAT_MODELING,
            metadata=data
        )
        self.indicators.append(indicator)
        
        # Add alert if high risk
        if data.get('risk_score', 0) > 7:
            self.alerts.append({
                "id": str(uuid.uuid4()),
                "title": f"High Risk Threat Model - {data.get('industry')}",
                "severity": "high",
                "timestamp": datetime.now().isoformat(),
                "source": "Threat Modeler",
                "description": f"Risk score: {data.get('risk_score')}"
            })
    
    def add_purple_team_data(self, data):
        """Add purple team exercise data"""
        indicator = ThreatIndicator(
            id=str(uuid.uuid4()),
            type="purple_team",
            value=f"Exercise: {data.get('exercise_name', 'Unknown')}",
            severity=ThreatSeverity.MEDIUM,
            first_seen=datetime.now(),
            last_seen=datetime.now(),
            confidence=0.9,
            source=DataSource.PURPLE_TEAM,
            metadata=data
        )
        self.indicators.append(indicator)
        
        self.alerts.append({
            "id": str(uuid.uuid4()),
            "title": f"Exercise Completed: {data.get('exercise_name')}",
            "severity": "medium",
            "timestamp": datetime.now().isoformat(),
            "source": "Purple Team",
            "description": f"Findings: {len(data.get('findings', []))}"
        })
    
    def add_lotl_data(self, data):
        """Add LotL simulation data"""
        indicator = ThreatIndicator(
            id=str(uuid.uuid4()),
            type="lotl_technique",
            value=f"LotL: {data.get('technique', 'Unknown')}",
            severity=ThreatSeverity.HIGH if data.get('risk') == 'high' else ThreatSeverity.MEDIUM,
            first_seen=datetime.now(),
            last_seen=datetime.now(),
            confidence=0.95,
            source=DataSource.LOTL_SIMULATOR,
            metadata=data
        )
        self.indicators.append(indicator)
    
    def add_deception_data(self, data):
        """Add deception technology data"""
        total_engagements = sum([
            data.get('honeypot_hits', 0),
            data.get('token_triggers', 0),
            data.get('decoy_accesses', 0)
        ])
        
        if total_engagements > 0:
            indicator = ThreatIndicator(
                id=str(uuid.uuid4()),
                type="deception_engagement",
                value=f"Deception engagements: {total_engagements}",
                severity=ThreatSeverity.HIGH if total_engagements > 10 else ThreatSeverity.MEDIUM,
                first_seen=datetime.now(),
                last_seen=datetime.now(),
                confidence=0.8,
                source=DataSource.DECEPTION_TECH,
                metadata=data
            )
            self.indicators.append(indicator)
            
            self.alerts.append({
                "id": str(uuid.uuid4()),
                "title": "Deception Technology Engagements",
                "severity": "high",
                "timestamp": datetime.now().isoformat(),
                "source": "Deception System",
                "description": f"Total engagements: {total_engagements}"
            })
    
    def generate_dashboard_report(self):
        """Generate comprehensive dashboard report"""
        
        # Calculate statistics
        total_indicators = len(self.indicators)
        total_alerts = len(self.alerts)
        
        # Severity breakdown
        severity_counts = defaultdict(int)
        for indicator in self.indicators:
            severity_counts[indicator.severity.value] += 1
        
        # Source breakdown
        source_counts = defaultdict(int)
        for indicator in self.indicators:
            source_counts[indicator.source.value] += 1
        
        # Recent activity (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_indicators = [
            i for i in self.indicators 
            if i.last_seen > recent_cutoff
        ]
        
        # MITRE technique coverage
        mitre_techniques = set()
        for indicator in self.indicators:
            if 'mitre' in indicator.metadata:
                mitre_value = indicator.metadata.get('mitre')
                if isinstance(mitre_value, str):
                    mitre_techniques.add(mitre_value)
                elif isinstance(mitre_value, list):
                    mitre_techniques.update(mitre_value)
        
        # Create report
        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_indicators": total_indicators,
                "total_alerts": total_alerts,
                "recent_indicators": len(recent_indicators),
                "mitre_techniques_covered": len(mitre_techniques)
            },
            "breakdowns": {
                "by_severity": dict(severity_counts),
                "by_source": dict(source_counts)
            },
            "recent_alerts": self.alerts[-10:] if self.alerts else [],
            "recent_indicators": [
                i.to_dict() for i in recent_indicators[-10:]
            ] if recent_indicators else [],
            "mitre_coverage": list(mitre_techniques),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self):
        """Generate recommendations based on data"""
        recommendations = []
        
        # Check for high severity indicators
        high_severity_count = sum(
            1 for i in self.indicators 
            if i.severity in [ThreatSeverity.HIGH, ThreatSeverity.CRITICAL]
        )
        
        if high_severity_count > 5:
            recommendations.append({
                "priority": "high",
                "action": "Review and respond to high severity threats",
                "details": f"{high_severity_count} high/critical severity indicators require attention"
            })
        
        # Check deception engagement rate
        deception_engagements = sum(
            1 for i in self.indicators 
            if i.type == "deception_engagement"
        )
        
        if deception_engagements > 0:
            recommendations.append({
                "priority": "medium",
                "action": "Investigate deception engagement alerts",
                "details": f"{deception_engagements} deception system engagements detected"
            })
        
        # Check for threat modeling gaps
        if len([i for i in self.indicators if i.source == DataSource.THREAT_MODELING]) == 0:
            recommendations.append({
                "priority": "medium",
                "action": "Conduct threat modeling exercise",
                "details": "No recent threat modeling data available"
            })
        
        return recommendations
    
    def generate_console_dashboard(self):
        """Generate a console-based dashboard display"""
        
        report = self.generate_dashboard_report()
        
        print("\n" + "="*60)
        print("OMEGA PLATFORM - THREAT INTELLIGENCE DASHBOARD")
        print("="*60)
        
        print(f"\n📊 SUMMARY")
        print(f"   Generated: {report['generated_at'][11:19]}")
        print(f"   Total Indicators: {report['summary']['total_indicators']}")
        print(f"   Total Alerts: {report['summary']['total_alerts']}")
        print(f"   Recent Indicators (24h): {report['summary']['recent_indicators']}")
        print(f"   MITRE Techniques Covered: {report['summary']['mitre_techniques_covered']}")
        
        print(f"\n⚠️  SEVERITY BREAKDOWN")
        for severity, count in report['breakdowns']['by_severity'].items():
            severity_icon = {
                'critical': '🔴',
                'high': '🟠', 
                'medium': '🟡',
                'low': '🟢',
                'info': '🔵'
            }.get(severity, '⚪')
            print(f"   {severity_icon} {severity.upper()}: {count}")
        
        print(f"\n📡 DATA SOURCES")
        for source, count in report['breakdowns']['by_source'].items():
            source_icon = {
                'threat_modeling': '🎯',
                'purple_team': '👥',
                'lotl_simulator': '🛠️',
                'deception_tech': '🎣'
            }.get(source, '📊')
            print(f"   {source_icon} {source.replace('_', ' ').title()}: {count}")
        
        print(f"\n🚨 RECENT ALERTS")
        if report['recent_alerts']:
            for alert in report['recent_alerts'][:3]:
                severity_icon = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(alert.get('severity', 'info'), '⚪')
                print(f"   {severity_icon} [{alert.get('severity', 'N/A').upper()}] {alert.get('title', 'Unknown')}")
                print(f"     Source: {alert.get('source', 'Unknown')}")
        else:
            print("   No recent alerts")
        
        print(f"\n🎯 MITRE ATT&CK COVERAGE")
        if report['mitre_coverage']:
            print(f"   Techniques detected: {', '.join(report['mitre_coverage'][:5])}")
            if len(report['mitre_coverage']) > 5:
                print(f"   (+ {len(report['mitre_coverage']) - 5} more)")
        else:
            print("   No MITRE techniques detected")
        
        print(f"\n💡 RECOMMENDATIONS")
        if report['recommendations']:
            for rec in report['recommendations'][:3]:
                priority_icon = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(rec.get('priority', 'medium'), '⚪')
                print(f"   {priority_icon} [{rec.get('priority', 'medium').upper()}] {rec.get('action', 'Unknown')}")
        else:
            print("   All systems operating normally")
        
        print(f"\n" + "="*60)
        print("Use this data to:")
        print("  • Prioritize security response efforts")
        print("  • Identify threat trends and patterns")
        print("  • Measure security program effectiveness")
        print("  • Guide security investment decisions")
        print("="*60)
        
        return report

def demonstrate_dashboard():
    """Demonstrate the threat intelligence dashboard"""
    print("\n🚀 DEMONSTRATING THREAT INTELLIGENCE DASHBOARD")
    print("="*60)
    
    # Create dashboard
    dashboard = SimpleDashboard()
    
    # Add sample data
    print("\n📥 Loading sample data from Omega Platform components...")
    dashboard.add_sample_data()
    
    # Generate and display dashboard
    print("\n📈 Generating dashboard report...")
    report = dashboard.generate_console_dashboard()
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"threat_dashboard_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Dashboard report saved to: {report_file}")
    
    # Generate HTML report
    html_report = create_html_report(report)
    html_file = f"threat_dashboard_{timestamp}.html"
    
    with open(html_file, 'w') as f:
        f.write(html_report)
    
    print(f"📄 HTML report saved to: {html_file}")
    
    return dashboard, report

def create_html_report(report):
    """Create HTML report from dashboard data"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Omega Platform - Threat Intelligence Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #007bff; }}
        .section {{ margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0; }}
        .metric-card {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #007bff; margin: 10px 0; }}
        .severity-badge {{ display: inline-block; padding: 5px 10px; border-radius: 4px; margin: 2px; font-size: 0.9em; }}
        .critical {{ background: #dc3545; color: white; }}
        .high {{ background: #fd7e14; color: white; }}
        .medium {{ background: #ffc107; color: black; }}
        .low {{ background: #28a745; color: white; }}
        .info {{ background: #17a2b8; color: white; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #dee2e6; }}
        th {{ background: #007bff; color: white; }}
        tr:hover {{ background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Omega Platform - Threat Intelligence Dashboard</h1>
            <p>Generated: {report['generated_at']}</p>
        </div>
        
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="metrics">
                <div class="metric-card">
                    <div>Total Indicators</div>
                    <div class="metric-value">{report['summary']['total_indicators']}</div>
                </div>
                <div class="metric-card">
                    <div>Active Alerts</div>
                    <div class="metric-value">{report['summary']['total_alerts']}</div>
                </div>
                <div class="metric-card">
                    <div>Recent Indicators</div>
                    <div class="metric-value">{report['summary']['recent_indicators']}</div>
                </div>
                <div class="metric-card">
                    <div>MITRE Coverage</div>
                    <div class="metric-value">{report['summary']['mitre_techniques_covered']}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>⚠️ Threat Severity Breakdown</h2>
    """
    
    # Add severity breakdown
    for severity, count in report['breakdowns']['by_severity'].items():
        html += f"""
            <div style="margin: 10px 0;">
                <span class="severity-badge {severity}">{severity.upper()}</span>
                <span style="margin-left: 10px;">{count} indicators</span>
                <div style="background: #e9ecef; height: 10px; border-radius: 5px; margin-top: 5px;">
                    <div style="background: #007bff; width: {min(count * 10, 100)}%; height: 100%; border-radius: 5px;"></div>
                </div>
            </div>
        """
    
    html += """
        </div>
        
        <div class="section">
            <h2>📡 Data Source Analysis</h2>
            <table>
                <tr><th>Source</th><th>Indicators</th><th>Coverage</th></tr>
    """
    
    # Add source breakdown
    for source, count in report['breakdowns']['by_source'].items():
        source_name = source.replace('_', ' ').title()
        html += f"""
                <tr>
                    <td>{source_name}</td>
                    <td>{count}</td>
                    <td>
                        <div style="background: #e9ecef; height: 10px; border-radius: 5px;">
                            <div style="background: #28a745; width: {min(count * 20, 100)}%; height: 100%; border-radius: 5px;"></div>
                        </div>
                    </td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>🚨 Recent Alerts</h2>
    """
    
    # Add recent alerts
    if report['recent_alerts']:
        html += """
            <table>
                <tr><th>Time</th><th>Severity</th><th>Title</th><th>Source</th></tr>
        """
        
        for alert in report['recent_alerts'][:5]:
            time_str = alert['timestamp'][11:16] if 'timestamp' in alert else 'N/A'
            severity = alert.get('severity', 'info')
            title = alert.get('title', 'Unknown')[:50] + ('...' if len(alert.get('title', '')) > 50 else '')
            source = alert.get('source', 'Unknown')
            
            html += f"""
                <tr>
                    <td>{time_str}</td>
                    <td><span class="severity-badge {severity}">{severity.upper()}</span></td>
                    <td>{title}</td>
                    <td>{source}</td>
                </tr>
            """
        
        html += "</table>"
    else:
        html += "<p>No recent alerts</p>"
    
    html += """
        </div>
        
        <div class="section">
            <h2>🎯 MITRE ATT&CK Coverage</h2>
            <p>Detected Techniques: 
    """
    
    # Add MITRE coverage
    if report['mitre_coverage']:
        html += ', '.join(report['mitre_coverage'][:10])
        if len(report['mitre_coverage']) > 10:
            html += f' (+ {len(report["mitre_coverage"]) - 10} more)'
    else:
        html += "None detected"
    
    html += """
            </p>
        </div>
        
        <div class="section">
            <h2>💡 Recommendations</h2>
    """
    
    # Add recommendations
    if report['recommendations']:
        html += "<ul>"
        for rec in report['recommendations']:
            priority = rec.get('priority', 'medium')
            html += f"""
                <li style="margin: 10px 0;">
                    <span class="severity-badge {priority}">{priority.upper()}</span>
                    {rec.get('action', 'Unknown')}
                    <br><small>{rec.get('details', '')}</small>
                </li>
            """
        html += "</ul>"
    else:
        html += "<p>No specific recommendations at this time.</p>"
    
    html += """
        </div>
        
        <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d;">
            <p>Omega Platform - Threat Intelligence Dashboard</p>
            <p>Generated by the Omega Platform Security Suite</p>
        </div>
    </div>
</body>
</html>
    """
    
    return html

if __name__ == "__main__":
    # Run the demonstration
    print("Starting Threat Intelligence Dashboard...")
    dashboard, report = demonstrate_dashboard()
    
    print("\n✅ Dashboard demonstration complete!")
    print("\nNext steps:")
    print("1. Integrate with real Omega Platform components")
    print("2. Add real-time data streaming")
    print("3. Implement interactive web interface")
    print("4. Connect to external threat feeds")
    print("5. Add machine learning analytics")
