#!/usr/bin/env python3
"""
Fixed Enhanced JAIDA with AI Threat Detection
"""

import time
import json
import random
from datetime import datetime
import sqlite3

class EnhancedJAIDA:
    def __init__(self):
        self.db_path = "data/sovereign_data.db"
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.setup_database()
        
    def setup_database(self):
        """Setup enhanced database tables"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS enhanced_alerts (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source TEXT,
                severity TEXT,
                category TEXT,
                description TEXT,
                confidence REAL,
                ai_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def generate_intelligent_alerts(self, source, count=3):
        """Generate alerts with AI-like intelligence - FIXED VERSION"""
        alert_templates = {
            "SIEM": [
                {"category": "Authentication", "desc": "Multiple failed logins detected"},
                {"category": "Privilege", "desc": "Unusual privilege escalation"},
                {"category": "Data", "desc": "Large data transfer detected"}
            ],
            "EDR": [
                {"category": "Process", "desc": "Suspicious process execution"},
                {"category": "File", "desc": "Malicious file detected"},
                {"category": "Registry", "desc": "Unauthorized registry modification"}
            ],
            "Firewall": [
                {"category": "Connection", "desc": "Blocked malicious connection"},
                {"category": "PortScan", "desc": "Port scan detected"},
                {"category": "DDoS", "desc": "DDoS attempt blocked"}
            ],
            "IDS": [
                {"category": "Exploit", "desc": "Exploit attempt detected"},
                {"category": "Malware", "desc": "Malware signature matched"},
                {"category": "Anomaly", "desc": "Network anomaly detected"}
            ]
        }
        
        alerts = []
        templates = alert_templates.get(source, [{"category": "Unknown", "desc": "Security alert"}])
        
        for i in range(count):
            template = random.choice(templates)
            
            # AI-like confidence scoring
            confidence = random.uniform(0.7, 0.99)
            
            # Severity based on confidence
            if confidence > 0.9:
                severity = "CRITICAL"
            elif confidence > 0.8:
                severity = "HIGH"
            elif confidence > 0.7:
                severity = "MEDIUM"
            else:
                severity = "LOW"
            
            # Add some realistic details
            details = {
                "SIEM": ["from external IP", "by service account", "during off-hours"],
                "EDR": ["with obfuscated code", "in memory only", "via PowerShell"],
                "Firewall": ["to known C2 server", "using encrypted tunnel", "from botnet"],
                "IDS": ["matching known APT", "using zero-day", "with lateral movement"]
            }.get(source, [""])
            
            description = f"{template['desc']} {random.choice(details)}"
            
            alert = {
                "id": f"{source}-AI-{int(time.time())}-{i}",
                "timestamp": datetime.now().isoformat(),
                "source": source,
                "severity": severity,
                "category": template["category"],
                "description": description,
                "confidence": round(confidence, 2),
                "ai_analysis": random.choice([
                    "Behavioral analysis indicates malicious intent",
                    "Pattern matches known threat actor TTPs",
                    "Anomaly detection triggered",
                    "Correlation with threat intelligence"
                ])
            }
            
            # Insert into database
            self.cursor.execute('''
                INSERT INTO enhanced_alerts 
                (id, timestamp, source, severity, category, description, confidence, ai_analysis)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                alert["id"],
                alert["timestamp"],
                alert["source"],
                alert["severity"],
                alert["category"],
                alert["description"],
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
        
        # Get threat summary
        self.cursor.execute("SELECT COUNT(*) FROM enhanced_alerts")
        total = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM enhanced_alerts WHERE severity IN ('HIGH', 'CRITICAL')")
        critical = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT source, COUNT(*) FROM enhanced_alerts GROUP BY source")
        sources = self.cursor.fetchall()
        
        print(f"Total Alerts: {total}")
        print(f"Critical Alerts: {critical}")
        print("\nBy Source:")
        for source, count in sources:
            print(f"  {source}: {count}")
        
        # Threat level calculation
        if critical > 10:
            threat_level = "🚨 CRITICAL"
            action = "Immediate investigation required"
        elif critical > 5:
            threat_level = "⚠️ HIGH"
            action = "Elevated monitoring"
        elif critical > 2:
            threat_level = "🟡 ELEVATED"
            action = "Review alerts"
        else:
            threat_level = "✅ NORMAL"
            action = "Routine monitoring"
        
        print(f"\n📈 Threat Level: {threat_level}")
        print(f"🎯 Action: {action}")
        
        return threat_level
    
    def run(self):
        """Main execution loop"""
        print("🤖 Enhanced JAIDA with AI Threat Detection (FIXED)")
        print("=" * 50)
        print(f"Started at: {datetime.now()}")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"\n🔁 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Generate alerts
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
                    "threat_level": threat_level
                }
                
                with open(f"logs/enhanced_fixed_cycle_{cycle}_report.json", "w") as f:
                    json.dump(report, f, indent=2)
                
                print(f"   💾 Report saved: logs/enhanced_fixed_cycle_{cycle}_report.json")
                
                time.sleep(10)  # 10-second cycles
                
        except KeyboardInterrupt:
            print("\n\n🛑 Enhanced JAIDA stopped by user")
        finally:
            self.conn.close()
            print("✅ Database connection closed")
            print(f"\n📊 Final stats: {cycle} enhanced cycles completed")

if __name__ == "__main__":
    jaida = EnhancedJAIDA()
    jaida.run()
