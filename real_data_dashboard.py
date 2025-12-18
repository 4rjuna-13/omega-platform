#!/usr/bin/env python3
"""
Real Data Integration Dashboard
"""

import json
from datetime import datetime
from real_data_adapter import RealDataAdapter

class RealDataDashboard:
    def __init__(self):
        self.adapter = RealDataAdapter()
    
    def display_summary(self):
        """Display real-time summary"""
        summary = self.adapter.get_alert_summary()
        
        print("=" * 60)
        print("📊 REAL DATA INTEGRATION DASHBOARD")
        print("=" * 60)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Alerts: {summary['total_alerts']}")
        print()
        
        print("📈 ALERTS BY SEVERITY:")
        for severity, count in sorted(summary['by_severity'].items(), 
                                    key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].index(x[0]) 
                                    if x[0] in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'] else 99):
            bar = "█" * min(count, 20)
            print(f"  {severity:10} {count:4} {bar}")
        
        print()
        print("📡 DATA SOURCES:")
        for source, data in summary['by_source'].items():
            print(f"  {source:15} {data['total']} alerts")
            for severity, count in data['severities'].items():
                print(f"    {severity}: {count}")
        
        print()
        print("🚀 RECOMMENDED ACTIONS:")
        if summary['by_severity'].get('CRITICAL', 0) > 0:
            print("  ⚠️  Immediate investigation required for critical alerts")
        if summary['total_alerts'] > 50:
            print("  📈 Consider adjusting alert thresholds")
        if len(summary['by_source']) < 2:
            print("  🔗 Add more data sources for better coverage")
        
        print("=" * 60)

if __name__ == "__main__":
    dashboard = RealDataDashboard()
    dashboard.display_summary()
    
    # Update data
    print("\n🔄 Updating data from sources...")
    adapter = RealDataAdapter()
    for source in ["mock_siem", "mock_edr"]:
        adapter.fetch_alerts(source, hours=24)
    
    print("\n" + "=" * 60)
    print("✅ Data updated! Run again to see latest statistics.")
