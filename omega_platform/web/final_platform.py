"""
OMEGA PLATFORM v4.5 - FINAL VERSION WITH ATT&CK MATRIX
"""
from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime

app = Flask(__name__)

print("="*60)
print("🚀 OMEGA PLATFORM v4.5 - FINAL EDITION")
print("="*60)

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Load ALL modules
modules = {}
loaded = {}

MODULES_TO_LOAD = [
    ('mitre_module', 'MITREModule', 'MITRE ATT&CK'),
    ('scenario_manager_enhanced', 'ScenarioManagerEnhanced', 'Scenario Manager'),
    ('data_lake', 'SecurityDataLake', 'Data Lake'),
    ('marketplace', 'ScenarioMarketplace', 'Marketplace'),
    ('attack_matrix', 'AttackMatrix', 'ATT&CK Matrix')
]

for module_file, class_name, display_name in MODULES_TO_LOAD:
    try:
        module = __import__(f'omega_platform.modules.{module_file}', fromlist=[class_name])
        klass = getattr(module, class_name)
        
        # Special handling for AttackMatrix (needs MITRE module)
        if class_name == 'AttackMatrix' and 'mitre' in modules:
            modules['attack_matrix'] = klass(modules['mitre'])
        else:
            # Store with simpler key
            if 'scenario_manager' in module_file:
                modules['scenarios'] = klass()  # Use 'scenarios' as key
            elif 'mitre_module' in module_file:
                modules['mitre'] = klass()  # Use 'mitre' as key
            elif 'data_lake' in module_file:
                modules['data_lake'] = klass()
            elif 'marketplace' in module_file:
                modules['marketplace'] = klass()
            elif 'attack_matrix' in module_file:
                modules['attack_matrix'] = klass(modules.get('mitre'))
        
        loaded[display_name] = True
        print(f"✅ {display_name}")
        
    except ImportError as e:
        print(f"⚠️  {display_name}: {str(e)[:50]}...")
        loaded[display_name] = False
    except Exception as e:
        print(f"❌ {display_name}: {e}")
        loaded[display_name] = False

print(f"\n📊 Loaded {sum(loaded.values())} of {len(loaded)} modules")

# Store loaded status for easy access
MITRE_LOADED = loaded.get('MITRE ATT&CK', False)
SCENARIOS_LOADED = loaded.get('Scenario Manager', False)
DATALAKE_LOADED = loaded.get('Data Lake', False)
MARKETPLACE_LOADED = loaded.get('Marketplace', False)
MATRIX_LOADED = loaded.get('ATT&CK Matrix', False)

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "version": "4.5",
        "modules_loaded": loaded,
        "description": "Adversary Emulation Platform with MITRE ATT&CK",
        "endpoints": [
            "GET  /api/status",
            "GET  /api/mitre",
            "GET  /api/scenarios",
            "GET  /api/marketplace",
            "POST /api/marketplace/import/<id>",
            "GET  /api/data-lake/events",
            "GET  /api/attack-matrix",
            "GET  /api/attack-matrix/recommendations",
            "POST /api/simulate/<id>"
        ]
    })

@app.route('/api/status')
def status():
    stats = {
        "version": "4.5",
        "modules": loaded,
        "timestamp": datetime.now().isoformat()
    }
    
    if MITRE_LOADED:
        stats['mitre_techniques'] = len(modules['mitre'].get_all())
    
    if SCENARIOS_LOADED:
        stats['scenarios'] = modules['scenarios'].count()
    
    if DATALAKE_LOADED:
        stats['data_lake_events'] = len(modules['data_lake'].get_all_events())
    
    if MARKETPLACE_LOADED:
        marketplace_stats = modules['marketplace'].get_stats()
        stats['marketplace'] = marketplace_stats
    
    if MATRIX_LOADED and SCENARIOS_LOADED:
        scenarios = modules['scenarios'].list_scenarios()
        matrix_stats = modules['attack_matrix'].get_coverage_stats(scenarios)
        stats['attack_matrix'] = {
            'unique_techniques': matrix_stats['unique_techniques'],
            'coverage_gaps': len(matrix_stats.get('all_techniques', [])) - matrix_stats['unique_techniques']
        }
    
    return jsonify(stats)

@app.route('/api/mitre')
def get_mitre():
    if not MITRE_LOADED:
        return jsonify({"error": "MITRE module not loaded"}), 500
    return jsonify(modules['mitre'].get_all())

@app.route('/api/scenarios')
def get_scenarios():
    if not SCENARIOS_LOADED:
        return jsonify({"error": "Scenario module not loaded"}), 500
    return jsonify({
        "scenarios": modules['scenarios'].list_scenarios(),
        "count": modules['scenarios'].count(),
        "user_scenarios": modules['scenarios'].get_user_scenarios() if hasattr(modules['scenarios'], 'get_user_scenarios') else []
    })

@app.route('/api/marketplace')
def get_marketplace():
    if not MARKETPLACE_LOADED:
        return jsonify({"error": "Marketplace module not loaded"}), 500
    return jsonify(modules['marketplace'].get_marketplace_scenarios())

@app.route('/api/marketplace/import/<scenario_id>', methods=['POST'])
def import_scenario(scenario_id):
    if not MARKETPLACE_LOADED:
        return jsonify({"error": "Marketplace module not loaded"}), 500
    result = modules['marketplace'].import_scenario(scenario_id)
    return jsonify(result)

@app.route('/api/data-lake/events')
def get_events():
    if not DATALAKE_LOADED:
        return jsonify({"error": "Data Lake module not loaded"}), 500
    
    limit = request.args.get('limit', default=20, type=int)
    events = modules['data_lake'].get_all_events()
    
    if limit and len(events) > limit:
        events = events[-limit:]
    
    return jsonify({
        "events": events,
        "count": len(events),
        "total": len(modules['data_lake'].get_all_events())
    })

# NEW: ATT&CK Matrix Endpoints
@app.route('/api/attack-matrix')
def get_attack_matrix():
    if not MATRIX_LOADED or not SCENARIOS_LOADED:
        return jsonify({"error": "ATT&CK Matrix or Scenario module not loaded"}), 500
    
    scenarios = modules['scenarios'].list_scenarios()
    visualization = modules['attack_matrix'].generate_visualization_data(scenarios)
    
    return jsonify(visualization)

@app.route('/api/attack-matrix/recommendations')
def get_matrix_recommendations():
    if not MATRIX_LOADED or not SCENARIOS_LOADED:
        return jsonify({"error": "ATT&CK Matrix or Scenario module not loaded"}), 500
    
    scenarios = modules['scenarios'].list_scenarios()
    recommendations = modules['attack_matrix'].get_recommendations(scenarios)
    
    return jsonify({
        "recommendations": recommendations,
        "total": len(recommendations),
        "scenarios_analyzed": len(scenarios)
    })

@app.route('/api/simulate/<scenario_id>', methods=['POST'])
def simulate(scenario_id):
    if not DATALAKE_LOADED:
        return jsonify({"error": "Data Lake module not loaded"}), 500
    
    # Try to find scenario details
    scenario_name = f"Scenario: {scenario_id}"
    mitre_techniques = ["T1566"]  # Default
    
    if SCENARIOS_LOADED:
        all_scenarios = modules['scenarios'].list_scenarios()
        for s in all_scenarios:
            if s.get('id') == scenario_id:
                scenario_name = s.get('name', scenario_name)
                mitre_techniques = s.get('mitre_techniques', mitre_techniques)
                break
    
    event_data = {
        "event_type": "simulation_execution",
        "scenario_id": scenario_id,
        "scenario_name": scenario_name,
        "threat_level": "medium",
        "mitre_techniques": mitre_techniques,
        "details": request.json if request.json else {}
    }
    
    event_id = modules['data_lake'].store_event(event_data)
    
    return jsonify({
        "success": True,
        "event_id": event_id,
        "message": f"Simulation '{scenario_name}' executed",
        "scenario": scenario_name,
        "mitre_techniques": mitre_techniques
    })

if __name__ == '__main__':
    print("\n🌐 WEB INTERFACE: http://localhost:8080")
    print("\n🔍 TEST ENDPOINTS:")
    print("  curl http://localhost:8080/api/status")
    print("  curl http://localhost:8080/api/attack-matrix")
    print("  curl http://localhost:8080/api/attack-matrix/recommendations")
    print("  curl http://localhost:8080/api/marketplace")
    print("  curl -X POST http://localhost:8080/api/marketplace/import/market_002")
    print("  curl -X POST http://localhost:8080/api/simulate/market_001 -H 'Content-Type: application/json' -d '{\"test\": true}'")
    print("\n" + "="*60)
    
    app.run(host='0.0.0.0', port=8080, debug=True)
