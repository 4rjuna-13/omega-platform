"""
Working Omega Platform Web App
"""
from flask import Flask, jsonify
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

print("=== Debug Info ===")
print(f"Current dir: {os.getcwd()}")
print(f"Looking for omega_platform at: {os.path.join(os.getcwd(), 'omega_platform')}")

# Try to import modules with better error handling
try:
    print("\nTrying to import MITREModule...")
    # Try direct import first
    try:
        from omega_platform.modules.mitre_module import MITREModule
        mitre = MITREModule()
        MITRE_LOADED = True
        print("✅ MITREModule loaded!")
    except ImportError as e1:
        print(f"❌ First attempt failed: {e1}")
        
        # Try alternative path
        print("Trying alternative import path...")
        sys.path.insert(0, os.path.join(os.getcwd(), 'omega_platform'))
        from modules.mitre_module import MITREModule
        mitre = MITREModule()
        MITRE_LOADED = True
        print("✅ MITREModule loaded via alternative path!")
        
except Exception as e:
    print(f"❌ MITRE import failed: {e}")
    MITRE_LOADED = False

# Same for ScenarioManager
try:
    print("\nTrying to import ScenarioManager...")
    if MITRE_LOADED:
        from omega_platform.modules.scenario_manager import ScenarioManager
        scenarios = ScenarioManager()
        SCENARIOS_LOADED = True
        print("✅ ScenarioManager loaded!")
    else:
        SCENARIOS_LOADED = False
except Exception as e:
    print(f"❌ ScenarioManager import failed: {e}")
    SCENARIOS_LOADED = False

print(f"\n=== Final Status ===")
print(f"MITRE_LOADED: {MITRE_LOADED}")
print(f"SCENARIOS_LOADED: {SCENARIOS_LOADED}")

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "status": "OPERATIONAL",
        "endpoints": ["/api/status", "/api/mitre", "/api/scenarios"]
    })

@app.route('/api/status')
def status():
    return jsonify({
        "version": "4.5",
        "mitre_loaded": MITRE_LOADED,
        "scenarios_loaded": SCENARIOS_LOADED,
        "path": os.getcwd()
    })

@app.route('/api/mitre')
def get_mitre():
    if MITRE_LOADED:
        return jsonify({
            "techniques": mitre.get_all(),
            "count": len(mitre.get_all()),
            "stats": mitre.get_stats()
        })
    else:
        return jsonify({
            "error": "MITRE module not loaded",
            "sample": [
                {"id": "T1566", "name": "Phishing"},
                {"id": "T1486", "name": "Ransomware"}
            ]
        })

@app.route('/api/scenarios')
def get_scenarios():
    if SCENARIOS_LOADED:
        return jsonify({
            "scenarios": scenarios.list_scenarios(),
            "count": scenarios.count()
        })
    else:
        return jsonify({
            "scenarios": [{"id": "sample", "name": "Sample from web app"}]
        })

if __name__ == '__main__':
    print("\n🚀 STARTING OMEGA PLATFORM v4.5")
    print("📡 http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)  # debug=False for cleaner output
