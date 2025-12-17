"""
Omega Platform WITH Marketplace
"""
from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime

app = Flask(__name__)

print("=== OMEGA PLATFORM v4.5 WITH MARKETPLACE ===")

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Load ALL modules
modules_loaded = {}
all_modules = {}

try:
    from omega_platform.modules.mitre_module import MITREModule
    all_modules['mitre'] = MITREModule()
    modules_loaded['mitre'] = True
    print("✅ MITRE Module loaded")
except ImportError as e:
    print(f"⚠️  MITRE Module: {e}")
    modules_loaded['mitre'] = False

try:
    from omega_platform.modules.scenario_manager import ScenarioManager
    all_modules['scenarios'] = ScenarioManager()
    modules_loaded['scenarios'] = True
    print("✅ Scenario Manager loaded")
except ImportError as e:
    print(f"⚠️  Scenario Manager: {e}")
    modules_loaded['scenarios'] = False

try:
    from omega_platform.modules.data_lake import SecurityDataLake
    all_modules['data_lake'] = SecurityDataLake()
    modules_loaded['data_lake'] = True
    print("✅ Data Lake loaded")
except ImportError as e:
    print(f"⚠️  Data Lake: {e}")
    modules_loaded['data_lake'] = False

try:
    from omega_platform.modules.marketplace import ScenarioMarketplace
    all_modules['marketplace'] = ScenarioMarketplace()
    modules_loaded['marketplace'] = True
    print("✅ Marketplace loaded")
except ImportError as e:
    print(f"⚠️  Marketplace: {e}")
    modules_loaded['marketplace'] = False

print(f"\n📊 Loaded {sum(modules_loaded.values())} of {len(modules_loaded)} modules")

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "modules": modules_loaded,
        "endpoints": [
            "GET  /api/status",
            "GET  /api/mitre",
            "GET  /api/scenarios",
            "GET  /api/marketplace",
            "POST /api/marketplace/import/<id>",
            "GET  /api/data-lake/events",
            "POST /api/simulate/<id>"
        ]
    })

@app.route('/api/status')
def status():
    stats = {"version": "4.5", "modules": modules_loaded}
    
    if modules_loaded.get('mitre'):
        stats['mitre_techniques'] = len(all_modules['mitre'].get_all())
    
    if modules_loaded.get('scenarios'):
        stats['scenarios'] = all_modules['scenarios'].count()
    
    if modules_loaded.get('data_lake'):
        stats['data_lake_events'] = len(all_modules['data_lake'].get_all_events())
    
    if modules_loaded.get('marketplace'):
        marketplace_stats = all_modules['marketplace'].get_stats()
        stats['marketplace'] = marketplace_stats
    
    return jsonify(stats)

@app.route('/api/mitre')
def get_mitre():
    if not modules_loaded.get('mitre'):
        return jsonify({"error": "MITRE module not loaded"}), 500
    return jsonify(all_modules['mitre'].get_all())

@app.route('/api/scenarios')
def get_scenarios():
    if not modules_loaded.get('scenarios'):
        return jsonify({"error": "Scenario module not loaded"}), 500
    return jsonify(all_modules['scenarios'].list_scenarios())

@app.route('/api/marketplace')
def get_marketplace():
    if not modules_loaded.get('marketplace'):
        return jsonify({"error": "Marketplace module not loaded"}), 500
    return jsonify(all_modules['marketplace'].get_marketplace_scenarios())

@app.route('/api/marketplace/import/<scenario_id>', methods=['POST'])
def import_scenario(scenario_id):
    if not modules_loaded.get('marketplace'):
        return jsonify({"error": "Marketplace module not loaded"}), 500
    
    result = all_modules['marketplace'].import_scenario(scenario_id)
    return jsonify(result)

@app.route('/api/data-lake/events')
def get_events():
    if not modules_loaded.get('data_lake'):
        return jsonify({"error": "Data Lake module not loaded"}), 500
    
    limit = request.args.get('limit', default=20, type=int)
    events = all_modules['data_lake'].get_all_events()
    
    if limit and len(events) > limit:
        events = events[-limit:]
    
    return jsonify({
        "events": events,
        "count": len(events)
    })

@app.route('/api/simulate/<scenario_id>', methods=['POST'])
def simulate(scenario_id):
    if not modules_loaded.get('data_lake'):
        return jsonify({"error": "Data Lake module not loaded"}), 500
    
    event_data = {
        "event_type": "simulation_execution",
        "scenario_id": scenario_id,
        "scenario_name": f"Scenario: {scenario_id}",
        "threat_level": "medium",
        "mitre_techniques": ["T1566"],
        "details": request.json if request.json else {}
    }
    
    event_id = all_modules['data_lake'].store_event(event_data)
    
    return jsonify({
        "success": True,
        "event_id": event_id,
        "message": "Simulation stored in data lake"
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 OMEGA PLATFORM v4.5 - WITH MARKETPLACE")
    print("="*50)
    print("🌐 http://localhost:8080")
    print("\nTry these new endpoints:")
    print("  curl http://localhost:8080/api/marketplace")
    print("  curl -X POST http://localhost:8080/api/marketplace/import/market_001")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
