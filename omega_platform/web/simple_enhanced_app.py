"""
SIMPLE Enhanced Omega Platform Web App
"""
from flask import Flask, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)

print("=== Starting SIMPLE Enhanced Omega Platform ===")

# SIMPLE IN-MEMORY DATA LAKE (no imports needed)
class SimpleDataLake:
    def __init__(self):
        self.events = []
        # Add sample events
        self.events.append({
            "event_id": "event_001",
            "timestamp": datetime.now().isoformat() + "Z",
            "event_type": "simulation_start",
            "scenario_id": "phishing_001",
            "scenario_name": "Basic Phishing Test",
            "threat_level": "medium",
            "mitre_techniques": ["T1566"]
        })
    
    def store_event(self, event_data):
        event_id = f"event_{len(self.events) + 1:03d}"
        event_data["event_id"] = event_id
        event_data["timestamp"] = datetime.now().isoformat() + "Z"
        self.events.append(event_data)
        return event_id
    
    def get_all_events(self):
        return self.events
    
    def get_stats(self):
        return {
            "total_events": len(self.events),
            "latest_event": self.events[-1] if self.events else None
        }

# Initialize simple data lake
data_lake = SimpleDataLake()
print("✅ Simple Data Lake initialized")

@app.route('/')
def home():
    return jsonify({
        "platform": "Omega Platform v4.5",
        "status": "SIMPLE ENHANCED VERSION",
        "message": "No import dependencies"
    })

@app.route('/api/status')
def status():
    return jsonify({
        "version": "4.5",
        "data_lake_events": len(data_lake.events),
        "status": "operational"
    })

@app.route('/api/data-lake/events')
def get_events():
    limit = request.args.get('limit', default=10, type=int)
    events = data_lake.events[-limit:] if data_lake.events else []
    return jsonify({
        "events": events,
        "count": len(events),
        "total": len(data_lake.events)
    })

@app.route('/api/data-lake/stats')
def get_datalake_stats():
    return jsonify(data_lake.get_stats())

@app.route('/api/simulate/<scenario_id>', methods=['POST'])
def run_simulation(scenario_id):
    event_data = {
        "event_type": "simulation_execution",
        "scenario_id": scenario_id,
        "scenario_name": f"Scenario {scenario_id}",
        "threat_level": "medium",
        "mitre_techniques": ["T1566"],
        "details": request.json if request.json else {}
    }
    
    event_id = data_lake.store_event(event_data)
    
    return jsonify({
        "success": True,
        "message": f"Simulation '{scenario_id}' executed",
        "event_id": event_id
    })

if __name__ == '__main__':
    print("\n🚀 SIMPLE ENHANCED OMEGA PLATFORM")
    print("📡 http://localhost:8080")
    print("\nEndpoints:")
    print("  GET  /api/data-lake/events")
    print("  GET  /api/data-lake/stats")
    print("  POST /api/simulate/<id>")
    print("\n" + "="*40)
    
    app.run(host='0.0.0.0', port=8080, debug=True)
