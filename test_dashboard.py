#!/usr/bin/env python3
"""
Test script for Threat Intelligence Dashboard
"""

from threat_intelligence_dashboard import SimpleDashboard, demonstrate_dashboard

if __name__ == "__main__":
    print("Testing Threat Intelligence Dashboard...")
    
    # Test basic functionality
    dashboard = SimpleDashboard()
    
    # Add test data
    dashboard.add_threat_modeling_data({
        "industry": "Finance",
        "vulnerabilities": 12,
        "risk_score": 8.5,
        "mitre_techniques": ["T1059", "T1566"]
    })
    
    # Generate report
    report = dashboard.generate_dashboard_report()
    
    print(f"✅ Test passed!")
    print(f"   Indicators: {report['summary']['total_indicators']}")
    print(f"   Alerts: {report['summary']['total_alerts']}")
    print(f"   MITRE Techniques: {report['summary']['mitre_techniques_covered']}")
    
    # Run full demonstration
    print("\nRunning full demonstration...")
    demonstrate_dashboard()
