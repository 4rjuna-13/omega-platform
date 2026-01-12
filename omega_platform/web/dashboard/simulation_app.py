"""
Omega Platform Simulation Dashboard - Clean Final Version
"""
from flask import Flask, render_template, jsonify, request
import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

app = Flask(__name__)

# Simple dashboard class
class SimulationDashboard:
    def __init__(self):
        self.startup_time = datetime.datetime.utcnow()
        self.stats = {
            'simulations_run': 0,
            'honeypot_interactions': 142,
            'detection_rate': 87.5
        }
    
    def get_status(self):
        return {
            'status': 'active',
            'uptime': str(datetime.datetime.utcnow() - self.startup_time),
            'demo_mode': True
        }

dashboard = SimulationDashboard()

# Routes
@app.route('/')
def index():
    return render_template('dashboard.html', 
                          version='3.0.0',
                          timestamp=datetime.datetime.utcnow().isoformat())

@app.route('/api/status')
def api_status():
    return jsonify({
        'platform': 'Omega Security Platform',
        'version': '3.0.0',
        'status': 'operational',
        'demo_mode': True,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'endpoints': [
            '/api/health',
            '/api/status', 
            '/api/scenarios',
            '/api/metrics'
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'simulation_dashboard',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/api/scenarios')
def scenarios():
    return jsonify([
        {'id': 'apt', 'name': 'APT Simulation', 'difficulty': 'advanced'},
        {'id': 'ransomware', 'name': 'Ransomware Attack', 'difficulty': 'medium'},
        {'id': 'insider', 'name': 'Insider Threat', 'difficulty': 'hard'},
        {'id': 'phishing', 'name': 'Phishing Campaign', 'difficulty': 'easy'}
    ])

@app.route('/api/metrics')
def metrics():
    return jsonify({
        'detection_rate': 87.5,
        'response_time': '2.3s',
        'active_simulations': 2,
        'honeypot_interactions': dashboard.stats['honeypot_interactions'],
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/api/simulation/run', methods=['POST'])
def run_simulation():
    data = request.json
    scenario = data.get('scenario', 'apt')
    
    dashboard.stats['simulations_run'] += 1
    
    return jsonify({
        'success': True,
        'scenario': scenario,
        'simulation_id': f"sim_{int(datetime.datetime.utcnow().timestamp())}",
        'status': 'started',
        'message': f'Simulation {scenario} started successfully'
    })

def print_welcome():
    print("=" * 50)
    print("🚀 OMEGA PLATFORM DASHBOARD v3.0")
    print("=" * 50)
    print("🌐 URL: http://localhost:5000")
    print("📊 API: http://localhost:5000/api/status")
    print("❤️  Health: http://localhost:5000/api/health")
    print("=" * 50)
    print("✅ Ready - Open browser to view dashboard")
    print("=" * 50)

if __name__ == '__main__':
    print_welcome()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
