"""
Enhanced Omega Platform Web Interface
"""
from flask import Flask, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from omega_platform.modules.mitre_module import MITREModule
    from omega_platform.modules.scenario_manager import ScenarioManager
    MITRE_LOADED = True
    print("✅ Modules loaded successfully")
except ImportError as e:
    MITRE_LOADED = False
    print(f"⚠️  Module import error: {e}")

app = Flask(__name__)

# Initialize modules
if MITRE_LOADED:
    mitre = MITREModule()
    scenario_mgr = ScenarioManager()

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "status": "enhanced",
        "message": "Adversary Emulation Platform"
    })

@app.route('/api/status')
def status():
    if MITRE_LOADED:
        stats = {
            "version": "4.5",
            "modules": {
                "mitre": "loaded",
                "scenarios": "loaded"
            },
            "mitre_stats": mitre.get_stats(),
            "scenario_count": scenario_mgr.count()
        }
    else:
        stats = {
            "version": "4.5",
            "modules": {
                "mitre": "not_loaded",
                "scenarios": "not_loaded"
            }
        }
    
    return jsonify(stats)

@app.route('/api/mitre/techniques')
def get_techniques():
    if MITRE_LOADED:
        return jsonify({
            "techniques": mitre.get_all(),
            "count": len(mitre.get_all())
        })
    return jsonify({"error": "MITRE module not loaded"}), 500

@app.route('/api/scenarios')
def get_scenarios():
    if MITRE_LOADED:
        return jsonify({
            "scenarios": scenario_mgr.list_scenarios(),
            "count": scenario_mgr.count()
        })
    return jsonify({"error": "Scenario module not loaded"}), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced Omega Platform v4.5")
    print("🌐 Web interface: http://localhost:8080")
    print("📊 API endpoints:")
    print("   - GET /api/status")
    print("   - GET /api/mitre/techniques")
    print("   - GET /api/scenarios")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
