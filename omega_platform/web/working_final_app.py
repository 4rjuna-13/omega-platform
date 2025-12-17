"""
WORKING FINAL Omega Platform Web App
Combines simple structure with real modules
"""
from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime

app = Flask(__name__)

print("=== LOADING OMEGA PLATFORM v4.5 ===")

# Add current directory to path - THIS WORKS
sys.path.insert(0, os.getcwd())

# Try to load real modules, fall back to simple ones
try:
    from omega_platform.modules.mitre_module import MITREModule
    from omega_platform.modules.scenario_manager import ScenarioManager
    from omega_platform.modules.data_lake import SecurityDataLake
    
    mitre = MITREModule()
    scenarios = ScenarioManager()
    data_lake = SecurityDataLake()
    
    USE_REAL_MODULES = True
    print("✅ USING REAL MODULES")
    print(f"   MITRE: {len(mitre.get_all())} techniques")
    print(f"   Scenarios: {scenarios.count()} scenarios")
    print(f"   Data Lake: {len(data_lake.get_all_events())} events")
    
except ImportError as e:
    print(f"⚠️  Using simple modules: {e}")
    USE_REAL_MODULES = False
    
    # Simple fallback implementations
    class SimpleMITRE:
        def __init__(self):
            self.techniques = [
                {"id": "T1566", "name": "Phishing", "tactics": ["Initial Access"]},
                {"id": "T1486", "name": "Ransomware", "tactics": ["Impact"]}
            ]
        def get_all(self): return self.techniques
        def get_stats(self): return {"total": 2}
    
    class SimpleScenarios:
        def __init__(self):
            self.scenarios = [
                {"id": "phishing_001", "name": "Basic Phishing", "mitre_techniques": ["T1566"]}
            ]
        def list_scenarios(self): return self.scenarios
        def count(self): return 1
    
    class SimpleDataLake:
        def __init__(self):
            self.events = []
        def get_all_events(self): return self.events
        def store_event(self, e):
            e["event_id"] = f"event_{len(self.events)+1}"
            e["timestamp"] = datetime.now().isoformat() + "Z"
            self.events.append(e)
            return e["event_id"]
        def get_stats(self):
            return {"total_events": len(self.events)}
    
    mitre = SimpleMITRE()
    scenarios = SimpleScenarios()
    data_lake = SimpleDataLake()

print(f"\n📊 MODE: {'REAL MODULES' if USE_REAL_MODULES else 'SIMPLE MODULES'}")

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "status": "OPERATIONAL",
        "modules": "real" if USE_REAL_MODULES else "simple",
        "endpoints": [
            "/api/status",
            "/api/mitre",
            "/api/scenarios",
            "/api/data-lake/events",
            "/api/data-lake/stats",
            "POST /api/simulate/<id>"
        ]
    })

@app.route('/api/status')
def status():
    return jsonify({
        "version": "4.5",
        "modules": "real" if USE_REAL_MODULES else "simple",
        "mitre_techniques": len(mitre.get_all()),
        "scenarios": scenarios.count(),
        "data_lake_events": len(data_lake.get_all_events())
    })

@app.route('/api/mitre')
def get_mitre():
    return jsonify({
        "techniques": mitre.get_all(),
        "stats": mitre.get_stats(),
        "module_type": "real" if USE_REAL_MODULES else "simple"
    })

@app.route('/api/scenarios')
def get_scenarios():
    return jsonify({
        "scenarios": scenarios.list_scenarios(),
        "count": scenarios.count(),
        "module_type": "real" if USE_REAL_MODULES else "simple"
    })

@app.route('/api/data-lake/events')
def get_events():
    limit = request.args.get('limit', default=20, type=int)
    events = data_lake.get_all_events()
    if limit and len(events) > limit:
        events = events[-limit:]
    
    return jsonify({
        "events": events,
        "count": len(events),
        "total": len(data_lake.get_all_events()),
        "module_type": "real" if USE_REAL_MODULES else "simple"
    })

@app.route('/api/data-lake/stats')
def get_stats():
    return jsonify({
        **data_lake.get_stats(),
        "module_type": "real" if USE_REAL_MODULES else "simple"
    })

@app.route('/api/simulate/<scenario_id>', methods=['POST'])
def simulate(scenario_id):
    event_data = {
        "event_type": "simulation_execution",
        "scenario_id": scenario_id,
        "scenario_name": f"Scenario: {scenario_id}",
        "threat_level": "medium",
        "mitre_techniques": ["T1566"],
        "details": request.json if request.json else {"source": "api"}
    }
    
    event_id = data_lake.store_event(event_data)
    
    return jsonify({
        "success": True,
        "event_id": event_id,
        "message": f"Simulation {scenario_id} stored in data lake",
        "module_type": "real" if USE_REAL_MODULES else "simple"
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 OMEGA PLATFORM v4.5 - WORKING FINAL VERSION")
    print("="*50)
    print("🌐 http://localhost:8080")
    print("\nTry these commands:")
    print("  curl http://localhost:8080/api/status")
    print("  curl -X POST http://localhost:8080/api/simulate/test123 -H 'Content-Type: application/json' -d '{\"test\": true}'")
    print("  curl http://localhost:8080/api/data-lake/events")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
