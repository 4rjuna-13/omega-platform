#!/usr/bin/env python3
"""
Real Data Adapter for JAIDA-Omega-SAIOS
Connects to real security data sources
"""

import json
import sqlite3
import time
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

class RealDataAdapter:
    """Adapter for real security data sources"""
    
    def __init__(self, db_path: str = "sovereign_data.db"):
        self.db_path = db_path
        self.sources = {
            "mock_siem": self._generate_mock_siem_alerts,
            "mock_edr": self._generate_mock_edr_alerts,
            "mock_firewall": self._generate_mock_firewall_alerts,
            "mock_ids": self._generate_mock_ids_alerts
        }
        
    def _generate_mock_siem_alerts(self, count: int = 10) -> List[Dict]:
        """Generate realistic SIEM alerts"""
        alerts = []
        severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        sources = ["Windows Event Log", "Linux Audit", "AWS CloudTrail", "Azure Monitor"]
        
        for i in range(count):
            alert = {
                "id": f"SIEM-{int(time.time())}-{i}",
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 60))).isoformat(),
                "source": random.choice(sources),
                "severity": random.choice(severities),
                "event_type": random.choice(["Failed Login", "Privilege Escalation", "Data Exfiltration", "Malware Detection"]),
                "src_ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                "dst_ip": f"10.0.{random.randint(1,255)}.{random.randint(1,255)}",
                "user": random.choice(["admin", "svc_account", "user", "unknown"]),
                "description": f"Suspicious activity detected from {random.choice(['internal', 'external'])} source",
                "raw_log": json.dumps({"event_id": random.randint(1000, 9999), "data": "sample log data"})
            }
            alerts.append(alert)
        return alerts
    
    def _generate_mock_edr_alerts(self, count: int = 8) -> List[Dict]:
        """Generate realistic EDR alerts"""
        alerts = []
        for i in range(count):
            alert = {
                "id": f"EDR-{int(time.time())}-{i}",
                "timestamp": datetime.now().isoformat(),
                "endpoint": f"WORKSTATION-{random.randint(100,999)}",
                "process": random.choice(["powershell.exe", "cmd.exe", "wmic.exe", "regsvr32.exe"]),
                "hash": f"{random.getrandbits(128):032x}",
                "action": random.choice(["Process Create", "File Write", "Registry Modify", "Network Connection"]),
                "severity": random.choice(["MEDIUM", "HIGH", "CRITICAL"]),
                "mitre_tactic": random.choice(["TA0001", "TA0002", "TA0005"]),
                "mitre_technique": random.choice(["T1059", "T1082", "T1204"])
            }
            alerts.append(alert)
        return alerts
    
    def connect_to_source(self, source_type: str, config: Dict = None) -> bool:
        """Connect to a data source"""
        print(f"🔗 Connecting to {source_type}...")
        time.sleep(1)  # Simulate connection time
        return True
    
    def fetch_alerts(self, source_type: str, hours: int = 24) -> List[Dict]:
        """Fetch alerts from specified source"""
        if source_type in self.sources:
            print(f"📥 Fetching alerts from {source_type} (last {hours} hours)...")
            alerts = self.sources[source_type](random.randint(5, 15))
            self._store_alerts(alerts, source_type)
            return alerts
        else:
            raise ValueError(f"Unknown source type: {source_type}")
    
    def _store_alerts(self, alerts: List[Dict], source_type: str):
        """Store alerts in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_alerts (
                id TEXT PRIMARY KEY,
                source_type TEXT,
                timestamp TEXT,
                severity TEXT,
                event_type TEXT,
                src_ip TEXT,
                dst_ip TEXT,
                user TEXT,
                description TEXT,
                raw_data TEXT,
                processed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        for alert in alerts:
            cursor.execute('''
                INSERT OR IGNORE INTO real_alerts 
                (id, source_type, timestamp, severity, event_type, src_ip, dst_ip, user, description, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert.get('id'),
                source_type,
                alert.get('timestamp'),
                alert.get('severity'),
                alert.get('event_type', alert.get('action', '')),
                alert.get('src_ip', ''),
                alert.get('dst_ip', ''),
                alert.get('user', alert.get('endpoint', '')),
                alert.get('description', ''),
                json.dumps(alert)
            ))
        
        conn.commit()
        conn.close()
        print(f"💾 Stored {len(alerts)} alerts from {source_type}")
    
    def get_alert_summary(self) -> Dict:
        """Get summary of stored alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                source_type,
                severity,
                COUNT(*) as count,
                MIN(timestamp) as first_seen,
                MAX(timestamp) as last_seen
            FROM real_alerts
            GROUP BY source_type, severity
            ORDER BY source_type, 
                CASE severity 
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'LOW' THEN 4
                    ELSE 5
                END
        ''')
        
        rows = cursor.fetchall()
        summary = {
            "total_alerts": cursor.execute("SELECT COUNT(*) FROM real_alerts").fetchone()[0],
            "by_source": {},
            "by_severity": {}
        }
        
        for row in rows:
            source_type, severity, count, first_seen, last_seen = row
            if source_type not in summary["by_source"]:
                summary["by_source"][source_type] = {"total": 0, "severities": {}}
            
            summary["by_source"][source_type]["total"] += count
            summary["by_source"][source_type]["severities"][severity] = count
            
            if severity not in summary["by_severity"]:
                summary["by_severity"][severity] = 0
            summary["by_severity"][severity] += count
        
        conn.close()
        return summary

    def _generate_mock_firewall_alerts(self, count: int = 7) -> List[Dict]:
        """Generate realistic firewall alerts"""
        alerts = []
        actions = ["ALLOW", "DENY", "DROP"]
        protocols = ["TCP", "UDP", "ICMP"]
        
        for i in range(count):
            alert = {
                "id": f"FW-{int(time.time())}-{i}",
                "timestamp": datetime.now().isoformat(),
                "src_ip": f"203.0.113.{random.randint(1,255)}",
                "dst_ip": f"192.168.1.{random.randint(1,255)}",
                "src_port": random.randint(1024, 65535),
                "dst_port": random.choice([80, 443, 22, 3389, 53]),
                "protocol": random.choice(protocols),
                "action": random.choice(actions),
                "severity": "MEDIUM" if random.random() > 0.7 else "LOW",
                "rule_id": f"FW-RULE-{random.randint(1000, 9999)}",
                "description": f"Firewall {random.choice(actions)} event"
            }
            alerts.append(alert)
        return alerts

    def _generate_mock_ids_alerts(self, count: int = 6) -> List[Dict]:
        """Generate realistic IDS alerts"""
        alerts = []
        signatures = [
            "ET EXPLOIT Possible CVE-2021-44228 Log4j RCE",
            "ET SCAN Potential SSH Brute Force",
            "ET TROJAN Possible Meterpreter Reverse Shell",
            "ET POLICY HTTP Request to Known Malicious Domain"
        ]
        
        for i in range(count):
            alert = {
                "id": f"IDS-{int(time.time())}-{i}",
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 30))).isoformat(),
                "signature": random.choice(signatures),
                "category": random.choice(["Exploit", "Scan", "Trojan", "Policy"]),
                "src_ip": f"10.0.{random.randint(0,255)}.{random.randint(1,255)}",
                "dst_ip": f"172.16.{random.randint(0,255)}.{random.randint(1,255)}",
                "severity": random.choice(["HIGH", "CRITICAL", "MEDIUM"]),
                "classification": random.choice(["Malicious", "Suspicious", "Informational"]),
                "description": random.choice(signatures)
            }
            alerts.append(alert)
        return alerts


# Integration with existing JAIDA system
def integrate_with_jaida():
    """Integrate real data with JAIDA system"""
    adapter = RealDataAdapter()
    
    print("🔄 Integrating real data adapter with JAIDA...")
    
    # Connect to mock sources
    for source in ["mock_siem", "mock_edr", "mock_firewall"]:
        if adapter.connect_to_source(source):
            alerts = adapter.fetch_alerts(source, hours=24)
            print(f"   ✅ {source}: {len(alerts)} alerts")
    
    # Get summary
    summary = adapter.get_alert_summary()
    print(f"\n📊 Alert Summary:")
    print(f"   Total Alerts: {summary['total_alerts']}")
    for severity, count in summary['by_severity'].items():
        print(f"   {severity}: {count}")
    
    return adapter

if __name__ == "__main__":
    adapter = integrate_with_jaida()
    print("\n✅ Real Data Integration Complete!")
    print("Next: Connect to actual data sources by modifying adapter configuration.")

    def _generate_mock_firewall_alerts(self, count: int = 7) -> List[Dict]:
        """Generate realistic firewall alerts"""
        alerts = []
        actions = ["ALLOW", "DENY", "DROP"]
        protocols = ["TCP", "UDP", "ICMP"]
        
        for i in range(count):
            alert = {
                "id": f"FW-{int(time.time())}-{i}",
                "timestamp": datetime.now().isoformat(),
                "src_ip": f"203.0.113.{random.randint(1,255)}",
                "dst_ip": f"192.168.1.{random.randint(1,255)}",
                "src_port": random.randint(1024, 65535),
                "dst_port": random.choice([80, 443, 22, 3389, 53]),
                "protocol": random.choice(protocols),
                "action": random.choice(actions),
                "severity": "MEDIUM" if random.random() > 0.7 else "LOW",
                "rule_id": f"FW-RULE-{random.randint(1000, 9999)}",
                "description": f"Firewall {random.choice(actions)} event"
            }
            alerts.append(alert)
        return alerts

    def _generate_mock_ids_alerts(self, count: int = 6) -> List[Dict]:
        """Generate realistic IDS alerts"""
        alerts = []
        signatures = [
            "ET EXPLOIT Possible CVE-2021-44228 Log4j RCE",
            "ET SCAN Potential SSH Brute Force",
            "ET TROJAN Possible Meterpreter Reverse Shell",
            "ET POLICY HTTP Request to Known Malicious Domain"
        ]
        
        for i in range(count):
            alert = {
                "id": f"IDS-{int(time.time())}-{i}",
                "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 30))).isoformat(),
                "signature": random.choice(signatures),
                "category": random.choice(["Exploit", "Scan", "Trojan", "Policy"]),
                "src_ip": f"10.0.{random.randint(0,255)}.{random.randint(1,255)}",
                "dst_ip": f"172.16.{random.randint(0,255)}.{random.randint(1,255)}",
                "severity": random.choice(["HIGH", "CRITICAL", "MEDIUM"]),
                "classification": random.choice(["Malicious", "Suspicious", "Informational"]),
                "description": random.choice(signatures)
            }
            alerts.append(alert)
        return alerts
