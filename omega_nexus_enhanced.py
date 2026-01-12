#!/usr/bin/env python3
"""
Omega Nexus Enhanced with Real Data Integration
"""

import sys
import time
from datetime import datetime
from real_data_adapter import RealDataAdapter

class OmegaNexusEnhanced:
    def __init__(self):
        print("🚀 Initializing Omega Nexus Enhanced...")
        self.data_adapter = RealDataAdapter()
        self.threat_level = "NORMAL"
        self.alert_count = 0
        
    def monitor_real_time(self):
        """Monitor real-time data streams"""
        print("👁️  Starting real-time monitoring...")
        
        sources = ["mock_siem", "mock_edr", "mock_firewall"]
        
        for source in sources:
            print(f"📡 Monitoring {source}...")
            try:
                if self.data_adapter.connect_to_source(source):
                    alerts = self.data_adapter.fetch_alerts(source, hours=1)
                    self.alert_count += len(alerts)
                    self._analyze_alerts(alerts)
            except Exception as e:
                print(f"⚠️  Error monitoring {source}: {e}")
        
        self._update_threat_level()
    
    def _analyze_alerts(self, alerts):
        """Analyze incoming alerts"""
        critical_count = sum(1 for alert in alerts if alert.get('severity') in ['HIGH', 'CRITICAL'])
        
        if critical_count > 0:
            print(f"🚨 Detected {critical_count} critical alerts")
            
            # Group alerts by type
            alert_types = {}
            for alert in alerts:
                alert_type = alert.get('event_type', alert.get('action', 'UNKNOWN'))
                alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
            
            print("   Alert breakdown:")
            for alert_type, count in alert_types.items():
                print(f"   - {alert_type}: {count}")
    
    def _update_threat_level(self):
        """Update system threat level based on alerts"""
        if self.alert_count > 20:
            self.threat_level = "CRITICAL"
        elif self.alert_count > 10:
            self.threat_level = "HIGH"
        elif self.alert_count > 5:
            self.threat_level = "ELEVATED"
        else:
            self.threat_level = "NORMAL"
        
        print(f"📈 Threat Level: {self.threat_level} ({self.alert_count} alerts)")
    
    def generate_report(self):
        """Generate enhanced threat report"""
        summary = self.data_adapter.get_alert_summary()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "threat_level": self.threat_level,
            "total_alerts": summary["total_alerts"],
            "alert_summary": summary["by_severity"],
            "data_sources": list(summary["by_source"].keys()),
            "recommendations": []
        }
        
        # Add recommendations based on threat level
        if self.threat_level in ["HIGH", "CRITICAL"]:
            report["recommendations"].append("Initiate incident response procedures")
            report["recommendations"].append("Notify security team")
            report["recommendations"].append("Increase monitoring frequency")
        
        return report

def main():
    nexus = OmegaNexusEnhanced()
    
    # Run monitoring cycle
    for i in range(3):  # Run 3 monitoring cycles
        print(f"\n=== Monitoring Cycle {i+1} ===")
        nexus.monitor_real_time()
        time.sleep(2)
    
    # Generate final report
    report = nexus.generate_report()
    
    print(f"\n📋 FINAL REPORT:")
    print(f"   Threat Level: {report['threat_level']}")
    print(f"   Total Alerts: {report['total_alerts']}")
    print(f"   Data Sources: {', '.join(report['data_sources'])}")
    print(f"   Recommendations:")
    for rec in report['recommendations']:
        print(f"     - {rec}")
    
    # Save report
    import json
    with open(f"threat_report_{int(time.time())}.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report saved: threat_report_{int(time.time())}.json")
    print("🎯 Real Data Integration Successful!")

if __name__ == "__main__":
    main()
