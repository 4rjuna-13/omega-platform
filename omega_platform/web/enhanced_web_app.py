"""
Enhanced Omega Platform Web App with Data Lake
"""
from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

print("=== Loading Omega Platform Modules ===")

# Import all modules
try:
    from omega_platform.modules.mitre_module import MITREModule
    from omega_platform.modules.scenario_manager import ScenarioManager
    from omega_platform.modules.data_lake import SecurityDataLake
    
    mitre = MITREModule()
    scenarios = ScenarioManager()
    data_lake = SecurityDataLake()
    
    print("✅ All modules loaded successfully!")
    MODULES_LOADED = True
    
except ImportError as e:
    print(f"❌ Module import failed: {e}")
    MODULES_LOADED = False

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "status": "ENHANCED WITH DATA LAKE",
        "version": "4.5",
        "endpoints": [
            "/api/status",
            "/api/mitre",
            "/api/scenarios", 
            "/api/data-lake/events",
            "/api/data-lake/stats",
            "/api/simulate/<scenario_id>"
        ]
    })

@app.route('/api/status')
def status():
    if MODULES_LOADED:
        stats = {
            "version": "4.5",
            "mitre_techniques": len(mitre.get_all()),
            "scenarios": scenarios.count(),
            "data_lake_events": len(data_lake.get_all_events()),
            "modules": ["mitre", "scenarios", "data_lake"]
        }
    else:
        stats = {"version": "4.5", "modules_loaded": False}
    
    return jsonify(stats)

@app.route('/api/mitre')
def get_mitre():
    if MODULES_LOADED:
        return jsonify({
            "techniques": mitre.get_all(),
            "count": len(mitre.get_all()),
            "stats": mitre.get_stats()
        })
    return jsonify({"error": "Modules not loaded"}), 500

@app.route('/api/scenarios')
def get_scenarios():
    if MODULES_LOADED:
        return jsonify({
            "scenarios": scenarios.list_scenarios(),
            "count": scenarios.count()
        })
    return jsonify({"error": "Modules not loaded"}), 500

# NEW: Data Lake Endpoints
@app.route('/api/data-lake/events')
def get_events():
    """Get all security events"""
    if MODULES_LOADED:
        limit = request.args.get('limit', default=10, type=int)
        events = data_lake.get_recent_events(limit)
        return jsonify({
            "events": events,
            "count": len(events),
            "total": len(data_lake.get_all_events())
        })
    return jsonify({"error": "Modules not loaded"}), 500

@app.route('/api/data-lake/stats')
def get_datalake_stats():
    """Get data lake statistics"""
    if MODULES_LOADED:
        stats = data_lake.get_stats()
        return jsonify(stats)
    return jsonify({"error": "Modules not loaded"}), 500

@app.route('/api/simulate/<scenario_id>', methods=['POST'])
def run_simulation(scenario_id):
    """Run a simulation and store event in data lake"""
    if not MODULES_LOADED:
        return jsonify({"error": "Modules not loaded"}), 500
    
    # Find the scenario
    all_scenarios = scenarios.list_scenarios()
    scenario = next((s for s in all_scenarios if s.get('id') == scenario_id), None)
    
    if not scenario:
        return jsonify({"error": f"Scenario {scenario_id} not found"}), 404
    
    # Create event data
    event_data = {
        "event_type": "simulation_execution",
        "scenario_id": scenario_id,
        "scenario_name": scenario.get('name', 'Unknown'),
        "threat_level": "medium",  # Could be based on scenario difficulty
        "mitre_techniques": scenario.get('mitre_techniques', []),
        "details": {
            "execution_time": datetime.now().isoformat(),
            "status": "completed",
            "user_data": request.json if request.json else {}
        }
    }
    
    # Store in data lake
    event_id = data_lake.store_event(event_data)
    
    return jsonify({
        "success": True,
        "message": f"Simulation '{scenario.get('name')}' executed",
        "event_id": event_id,
        "scenario": scenario,
        "stored_in_datalake": True
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 OMEGA PLATFORM v4.5 - ENHANCED EDITION")
    print("="*50)
    print("📊 Modules: MITRE ATT&CK, Scenario Manager, Security Data Lake")
    print("🌐 Web Interface: http://localhost:8080")
    print("📡 API Endpoints:")
    print("   • GET  /api/status")
    print("   • GET  /api/mitre")
    print("   • GET  /api/scenarios")
    print("   • GET  /api/data-lake/events")
    print("   • GET  /api/data-lake/stats")
    print("   • POST /api/simulate/<scenario_id>")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
