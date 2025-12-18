#!/usr/bin/env python3
"""
JAIDA-Omega-SAIOS - Working Entry Point
"""

import sys
import os
import time
import json
import random
from datetime import datetime
import sqlite3

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class WorkingJAIDA:
    """Simple working JAIDA system"""
    
    def __init__(self):
        self.db_path = "data/sovereign_data.db"
        self.setup_database()
    
    def setup_database(self):
        """Ensure database and tables exist"""
        os.makedirs("data", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create working alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS working_alerts (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                source TEXT,
                severity TEXT,
                description TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_alerts(self):
        """Generate realistic alerts"""
        sources = ["SIEM", "EDR", "Firewall", "IDS", "Cloud"]
        severities = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        events = [
            "Failed login attempt",
            "Suspicious process execution",
            "Port scan detected",
            "Malware signature match",
            "Data exfiltration attempt",
            "Privilege escalation",
            "Unusual network traffic",
            "Configuration change",
            "Vulnerability scan finding",
            "Threat intelligence match"
        ]
        
        alerts = []
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for i in range(random.randint(3, 8)):
            alert = {
                "id": f"ALERT-{int(time.time())}-{i}",
                "timestamp": datetime.now().isoformat(),
                "source": random.choice(sources),
                "severity": random.choice(severities),
                "description": random.choice(events),
                "confidence": round(random.uniform(0.5, 0.99), 2)
            }
            
            cursor.execute('''
                INSERT INTO working_alerts 
                (id, timestamp, source, severity, description, confidence)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                alert["id"],
                alert["timestamp"],
                alert["source"],
                alert["severity"],
                alert["description"],
                alert["confidence"]
            ))
            
            alerts.append(alert)
        
        conn.commit()
        conn.close()
        return alerts
    
    def analyze_threats(self):
        """Analyze current threat level"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get stats
        cursor.execute("SELECT COUNT(*) FROM working_alerts")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT severity, COUNT(*) FROM working_alerts GROUP BY severity")
        severity_counts = dict(cursor.fetchall())
        
        cursor.execute("SELECT source, COUNT(*) FROM working_alerts GROUP BY source")
        source_counts = dict(cursor.fetchall())
        
        conn.close()
        
        # Calculate threat level
        critical = severity_counts.get("CRITICAL", 0) + severity_counts.get("HIGH", 0)
        
        if critical > 5:
            threat_level = "🚨 CRITICAL"
        elif critical > 2:
            threat_level = "⚠️ HIGH"
        elif total > 10:
            threat_level = "🟡 ELEVATED"
        else:
            threat_level = "✅ NORMAL"
        
        return {
            "total_alerts": total,
            "severity_counts": severity_counts,
            "source_counts": source_counts,
            "threat_level": threat_level,
            "critical_count": critical
        }
    
    def display_dashboard(self, stats):
        """Display simple dashboard"""
        print("\n" + "=" * 60)
        print("🤖 JAIDA-OMEGA-SAIOS - REAL-TIME DASHBOARD")
        print("=" * 60)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Threat Level: {stats['threat_level']}")
        print(f"Total Alerts: {stats['total_alerts']}")
        print(f"Critical Alerts: {stats['critical_count']}")
        
        print("\n📊 ALERT BREAKDOWN:")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
            count = stats['severity_counts'].get(severity, 0)
            if count > 0:
                bar = "█" * min(count, 20)
                print(f"  {severity:10} {count:4} {bar}")
        
        print("\n📡 DATA SOURCES:")
        for source, count in stats['source_counts'].items():
            print(f"  {source:12} {count:4} alerts")
        
        print("\n🚨 RECOMMENDATIONS:")
        if stats['threat_level'] == "🚨 CRITICAL":
            print("  • Immediate investigation required")
            print("  • Notify security team")
            print("  • Increase monitoring frequency")
        elif stats['threat_level'] == "⚠️ HIGH":
            print("  • Review critical alerts")
            print("  • Consider incident response")
            print("  • Monitor closely")
        else:
            print("  • Routine monitoring")
            print("  • Continue normal operations")
        
        print("=" * 60)
    
    def run(self):
        """Main execution loop"""
        print("🚀 Starting JAIDA-Omega-SAIOS Working System")
        print("=" * 60)
        print(f"Started at: {datetime.now()}")
        
        cycle = 0
        try:
            while True:
                cycle += 1
                print(f"\n🔁 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Generate new alerts
                alerts = self.generate_alerts()
                print(f"   📥 Generated {len(alerts)} new alerts")
                
                # Analyze threats
                stats = self.analyze_threats()
                
                # Display dashboard
                self.display_dashboard(stats)
                
                # Save report
                report = {
                    "cycle": cycle,
                    "timestamp": datetime.now().isoformat(),
                    "alerts_generated": len(alerts),
                    **stats
                }
                
                with open(f"logs/cycle_{cycle}_report.json", "w") as f:
                    json.dump(report, f, indent=2)
                
                print(f"   💾 Report saved: logs/cycle_{cycle}_report.json")
                
                # Wait for next cycle
                time.sleep(15)
                
        except KeyboardInterrupt:
            print("\n\n🛑 JAIDA stopped by user")
            print("✅ System shutdown complete")
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    """Main entry point"""
    # Simple command line interface
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            jaida = WorkingJAIDA()
            stats = jaida.analyze_threats()
            jaida.display_dashboard(stats)
            return
        elif sys.argv[1] == "test":
            print("🧪 Running system test...")
            jaida = WorkingJAIDA()
            jaida.setup_database()
            alerts = jaida.generate_alerts()
            print(f"✅ Generated {len(alerts)} test alerts")
            return
        elif sys.argv[1] == "clean":
            print("🧹 Cleaning database...")
            conn = sqlite3.connect("data/sovereign_data.db")
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS working_alerts")
            conn.commit()
            conn.close()
            print("✅ Database cleaned")
            return
    
    # Default: run the system
    jaida = WorkingJAIDA()
    jaida.run()

if __name__ == "__main__":
    main()
