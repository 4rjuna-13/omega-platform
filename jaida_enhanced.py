#!/usr/bin/env python3
"""
Enhanced JAIDA with AI Threat Detection
"""

import time
import json
import random
from datetime import datetime, timedelta
import sqlite3

class EnhancedJAIDA:
    def __init__(self):
        self.db_path = "data/sovereign_data.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.setup_database()
        
    def setup_database(self):
        """Setup enhanced database tables"""
        # Enhanced alerts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_alerts (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source TEXT,
                severity TEXT,
                category TEXT,
                description TEXT,
                ioc_type TEXT,
                ioc_value TEXT,
                confidence REAL,
                ai_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Threat intelligence table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS threat_intel (
                id TEXT PRIMARY KEY,
                ioc_type TEXT,
                ioc_value TEXT,
                threat_type TEXT,
                confidence REAL,
                first_seen TEXT,
                last_seen TEXT,
                source TEXT,
                metadata TEXT
            )
        ''')
        
        self.conn.commit()
    
    def generate_intelligent_alerts(self, source, count=3):
        """Generate alerts with AI-like intelligence"""
        alert_templates = {
            "SIEM": [
                {"category": "Authentication", "desc": "Multiple failed logins from {ip}", "ioc": "ip"},
                {"category": "Privilege", "desc": "Unusual privilege escalation by {user}", "ioc": "user"},
                {"category": "Data", "desc": "Large data transfer to {domain}", "ioc": "domain"}
            ],
            "EDR": [
                {"category": "Process", "desc": "Suspicious process {process} execution", "ioc": "process"},
                {"category": "File", "desc": "Malicious file {hash} detected", "ioc": "hash"},
                {"category": "Registry", "desc": "Unauthorized registry modification {key}", "ioc": "registry"}
            ],
            "Firewall": [
                {"category": "Connection", "desc": "Blocked connection to {ip}:{port}", "ioc": "ip"},
                {"category": "PortScan", "desc": "Port scan detected from {ip}", "ioc": "ip"},
                {"category": "DDoS", "desc": "DDoS attempt from {ip_range}", "ioc": "ip_range"}
            ]
        }
        
        alerts = []
        for i in range(count):
            template = random.choice(alert_templates.get(source, [{"category": "Unknown", "desc": "Alert", "ioc": "unknown"}]))
            
            # Generate realistic IOC values
            ioc_values = {
                "ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                "user": random.choice(["admin", "svc_account", "guest", "system"]),
                "domain": random.choice(["malicious.com", "suspicious.net", "exfil.site"]),
                "process": random.choice(["powershell.exe", "cmd.exe", "wmic.exe", "regsvr32.exe"]),
                "hash": f"{random.getrandbits(128):032x}",
                "registry": f"HKLM\\\\{random.choice(['SOFTWARE', 'SYSTEM', 'SAM'])}\\\\...",
                "ip_range": f"10.0.{random.randint(0,255)}.0/24",
                "unknown": "unknown"
            }
            
            # AI-like confidence scoring
            confidence = random.uniform(0.7, 0.99)
            
            # Severity based on confidence and category
            if confidence > 0.9:
                severity = "CRITICAL"
            elif confidence > 0.8:
                severity = "HIGH"
            elif confidence > 0.7:
                severity = "MEDIUM"
            else:
                severity = "LOW"
            
            alert = {
                "id": f"{source}-AI-{int(time.time())}-{i}",
                "timestamp": datetime.now().isoformat(),
                "source": source,
                "severity": severity,
                "category": template["category"],
                "description": template["desc"].format(**{template["ioc"]: ioc_values.get(template["ioc"], "unknown")}),
                "ioc_type": template["ioc"],
                "ioc_value": ioc_values[template["ioc"]],
                "confidence": round(confidence, 2),
                "ai_analysis": random.choice([
                    "Behavioral analysis indicates malicious intent",
                    "Pattern matches known threat actor TTPs",
                    "Anomaly detection triggered based on baseline",
                    "Correlation with threat intelligence feeds"
                ])
            }
            
            # Insert into database
            self.cursor.execute('''
                INSERT INTO enhanced_alerts 
                (id, timestamp, source, severity, category, description, ioc_type, ioc_value, confidence, ai_analysis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert["id"],
                alert["timestamp"],
                alert["source"],
                alert["severity"],
                alert["category"],
                alert["description"],
                alert["ioc_type"],
                alert["ioc_value"],
                alert["confidence"],
                alert["ai_analysis"]
            ))
            
            alerts.append(alert)
        
        self.conn.commit()
        return alerts
    
    def analyze_threats(self):
        """AI threat analysis"""
        print("\n🔍 AI Threat Analysis:")
        print("-" * 40)
        
        # Analyze by IOC
        self.cursor.execute('''
            SELECT ioc_type, ioc_value, COUNT(*) as count, 
                   AVG(confidence) as avg_confidence,
                   GROUP_CONCAT(DISTINCT source) as sources
            FROM enhanced_alerts 
            WHERE ioc_type != 'unknown'
            GROUP BY ioc_type, ioc_value
            HAVING count > 1
            ORDER BY count DESC
            LIMIT 5
        ''')
        
        ioc_analysis = self.cursor.fetchall()
        
        if ioc_analysis:
            print("Top IOC Correlations:")
            for ioc_type, ioc_value, count, avg_conf, sources in ioc_analysis:
                print(f"  {ioc_type}: {ioc_value}")
                print(f"    Occurrences: {count}, Avg Confidence: {avg_conf:.2f}")
                print(f"    Sources: {sources}")
        else:
            print("  No IOC correlations detected")
        
        # Threat level calculation
        self.cursor.execute("SELECT COUNT(*) FROM enhanced_alerts WHERE severity IN ('HIGH', 'CRITICAL')")
        critical_count = self.cursor.fetchone()[0]
        
        if critical_count > 10:
            threat_level = "🚨 CRITICAL"
            action = "Immediate investigation required"
        elif critical_count > 5:
            threat_level = "⚠️ HIGH"
            action = "Elevated monitoring"
        elif critical_count > 2:
            threat_level = "🟡 ELEVATED"
            action = "Review alerts"
        else:
            threat_level = "✅ NORMAL"
            action = "Routine monitoring"
        
        print(f"\n📈 Threat Level: {threat_level}")
        print(f"📊 Critical Alerts: {critical_count}")
        print(f"🎯 Recommended Action: {action}")
        
        return threat_level
    
    def run(self):
        """Main execution loop"""
        print("🤖 Enhanced JAIDA with AI Threat Detection")
        print("=" * 50)
        print(f"Started at: {datetime.now()}")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"\n🔁 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Generate alerts from enhanced sources
                sources = ["SIEM", "EDR", "Firewall", "IDS"]
                total_alerts = 0
                
                for source in sources:
                    alerts = self.generate_intelligent_alerts(source, random.randint(1, 3))
                    print(f"   📥 {source}: {len(alerts)} AI-enhanced alerts")
                    total_alerts += len(alerts)
                
                # Run AI analysis
                threat_level = self.analyze_threats()
                
                # Save cycle report
                self.cursor.execute("SELECT COUNT(*) FROM enhanced_alerts")
                total_in_db = self.cursor.fetchone()[0]
                
                report = {
                    "cycle": cycle,
                    "timestamp": datetime.now().isoformat(),
                    "alerts_generated": total_alerts,
                    "total_in_db": total_in_db,
                    "threat_level": threat_level,
                    "ai_analysis": "completed"
                }
                
                with open(f"logs/enhanced_cycle_{cycle}_report.json", "w") as f:
                    json.dump(report, f, indent=2)
                
                print(f"   💾 Enhanced report saved: logs/enhanced_cycle_{cycle}_report.json")
                
                time.sleep(15)  # 15-second cycles
                
        except KeyboardInterrupt:
            print("\n\n🛑 Enhanced JAIDA stopped by user")
        finally:
            self.conn.close()
            print("✅ Database connection closed")
            print(f"\n📊 Final stats: {cycle} enhanced cycles completed")

if __name__ == "__main__":
    jaida = EnhancedJAIDA()
    jaida.run()
