#!/usr/bin/env python3
"""
JAIDA Real-time Dashboard
"""

import json
import time
from datetime import datetime
import sqlite3
from collections import defaultdict

class JAIDADashboard:
    def __init__(self):
        self.db_path = "data/sovereign_data.db"
        self.update_interval = 5  # seconds
        
    def get_stats(self):
        """Get current system statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_alerts": 0,
            "by_severity": defaultdict(int),
            "by_source": defaultdict(int),
            "recent_alerts": [],
            "threat_level": "NORMAL"
        }
        
        # Get alert counts
        cursor.execute("SELECT severity, COUNT(*) FROM simple_alerts GROUP BY severity")
        for severity, count in cursor.fetchall():
            stats["by_severity"][severity] = count
            stats["total_alerts"] += count
        
        # Get source counts
        cursor.execute("SELECT source, COUNT(*) FROM simple_alerts GROUP BY source")
        for source, count in cursor.fetchall():
            stats["by_source"][source] = count
        
        # Get recent alerts
        cursor.execute("""
            SELECT timestamp, source, severity, description 
            FROM simple_alerts 
            ORDER BY timestamp DESC 
            LIMIT 10
        """)
        stats["recent_alerts"] = cursor.fetchall()
        
        # Determine threat level
        critical = stats["by_severity"].get("CRITICAL", 0) + stats["by_severity"].get("HIGH", 0)
        if critical > 20:
            stats["threat_level"] = "🚨 CRITICAL"
        elif critical > 10:
            stats["threat_level"] = "⚠️ HIGH"
        elif critical > 5:
            stats["threat_level"] = "🟡 ELEVATED"
        else:
            stats["threat_level"] = "✅ NORMAL"
        
        conn.close()
        return stats
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        import os
        
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            stats = self.get_stats()
            
            print("=" * 60)
            print("🤖 JAIDA-OMEGA-SAIOS REAL-TIME DASHBOARD")
            print("=" * 60)
            print(f"Last Updated: {stats['timestamp']}")
            print(f"Threat Level: {stats['threat_level']}")
            print(f"Total Alerts: {stats['total_alerts']}")
            print()
            
            # Alert severity breakdown
            print("📊 ALERT SEVERITY:")
            severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            for severity in severities:
                count = stats["by_severity"].get(severity, 0)
                bar = "█" * min(count // 2 + 1, 30)  # Scale for display
                print(f"  {severity:10} {count:4} {bar}")
            
            print()
            
            # Data sources
            print("📡 DATA SOURCES:")
            for source, count in sorted(stats["by_source"].items()):
                percentage = (count / stats["total_alerts"] * 100) if stats["total_alerts"] > 0 else 0
                print(f"  {source:12} {count:4} alerts ({percentage:.1f}%)")
            
            print()
            
            # Recent alerts
            print("🚨 RECENT ALERTS (last 10):")
            if stats["recent_alerts"]:
                for alert in stats["recent_alerts"][:5]:  # Show first 5
                    timestamp, source, severity, description = alert
                    time_str = timestamp[11:19] if len(timestamp) > 10 else timestamp
                    print(f"  {time_str} [{source}] {severity}: {description[:40]}...")
                if len(stats["recent_alerts"]) > 5:
                    print(f"  ... and {len(stats['recent_alerts']) - 5} more")
            else:
                print("  No recent alerts")
            
            print()
            print("=" * 60)
            print("Auto-refreshing every 5 seconds... Press Ctrl+C to exit")
            
            time.sleep(self.update_interval)

if __name__ == "__main__":
    try:
        dashboard = JAIDADashboard()
        dashboard.display_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")
        print("✅ JAIDA-Omega-SAIOS is still running in the background")
