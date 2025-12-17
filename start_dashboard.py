#!/usr/bin/env python3
"""
Omega Platform Simulation Dashboard Startup
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from omega_platform.web.dashboard.simulation_app import app
    print("🚀 Starting Omega Platform Simulation Dashboard...")
    print("🌐 Dashboard URL: http://localhost:5000")
    print("📊 API Status:    http://localhost:5000/api/status")
    print("")
    print("Press Ctrl+C to stop the dashboard")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Please make sure:")
    print("1. You're in the omega-platform directory")
    print("2. Flask is installed: pip install flask")
    print("3. The dashboard files exist in omega_platform/web/dashboard/")
