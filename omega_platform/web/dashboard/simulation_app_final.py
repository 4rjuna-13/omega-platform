"""
Omega Platform Simulation Dashboard - Final Version
Modern web interface for threat simulation management
"""
from flask import Flask, render_template, jsonify, request
import json
import sys
import os
import datetime

# Add parent directory to path to import omega_platform modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

app = Flask(__name__)

# Import Omega Platform modules
try:
    from omega_platform.core.engine import OmegaEngine
    from omega_platform.core.config_loader import load_config
    PLATFORM_AVAILABLE = True
except ImportError as e:
    PLATFORM_AVAILABLE = False
    print(f"ℹ️  Running in demo mode: {e}")

class SimulationDashboard:
    """Manages simulation dashboard functionality"""
    
    def __init__(self):
        self.engine = None
        self.startup_time = datetime.datetime.utcnow()
        
        if PLATFORM_AVAILABLE:
            self.initialize_platform()
    
    def initialize_platform(self):
        """Initialize connection to Omega Platform"""
        try:
            # Try to load config
            config = {"environment": "development", "demo_mode": True}
            try:
                config = load_config("config/defaults.yaml", "development")
            except Exception as e:
                print(f"⚠️  Using default config: {e}")
            
            self.engine = OmegaEngine(config)
            print("✅ Dashboard initialized (Demo Mode)")
        except Exception as e:
            print(f"⚠️  Platform initialization failed: {e}")
            self.engine = None
    
    def get_simulation_status(self):
        """Get current simulation status"""
        return {
            'status': 'active',
            'active_scenarios': 2,
            'available_scenarios': ['APT_Simulation', 'Ransomware_Attack', 'Insider_Threat'],
            'honeypots_targeted': 3,
            'events_processed': 142,
            'demo_data': True,
            'uptime': str(datetime.datetime.utcnow() - self.startup_time)
        }
    
    def get_deception_status(self):
        """Get current deception honeypot status"""
        return {
            'active_honeypots': 4,
            'honeypots': [
                {'id': 'web_hp_1', 'type': 'web', 'status': 'active', 'interactions': 12},
                {'id': 'ssh_hp_1', 'type': 'ssh', 'status': 'active', 'interactions': 8},
                {'id': 'db_hp_1', 'type': 'database', 'status': 'active', 'interactions': 5},
                {'id': 'win_hp_1', 'type': 'windows', 'status': 'inactive', 'interactions': 0}
            ],
            'total_interactions': 25,
            'detected_attacks': 3,
            'demo_data': True
        }
    
    def run_simulation_scenario(self, scenario_name):
        """Run a specific simulation scenario"""
        return {
            'success': True,
            'scenario': scenario_name,
            'status': 'started',
            'simulation_id': f"sim_{int(datetime.datetime.utcnow().timestamp())}",
            'steps_executed': 0,
            'honeypots_targeted': 2,
            'demo_data': True,
            'start_time': datetime.datetime.utcnow().isoformat() + 'Z',
            'estimated_completion': (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).isoformat() + 'Z'
        }

# Initialize dashboard
dashboard = SimulationDashboard()

# Flask Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard_enhanced.html',
                          platform_available=PLATFORM_AVAILABLE,
                          version='3.0.0')

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    return jsonify({
        'platform': 'Omega Security Platform',
        'version': '3.0.0',
        'phase': 3,
        'modules': {
            'simulation': dashboard.get_simulation_status(),
            'deception': dashboard.get_deception_status()
        },
        'demo_mode': True,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'dashboard_uptime': str(datetime.datetime.utcnow() - dashboard.startup_time)
    })

@app.route('/api/simulation/scenarios')
def get_scenarios():
    """Get available simulation scenarios"""
    scenarios = [
        {'id': 'apt_sim', 'name': 'APT Simulation', 'difficulty': 'advanced', 'duration': '2h'},
        {'id': 'ransomware_sim', 'name': 'Ransomware Attack', 'difficulty': 'medium', 'duration': '45m'},
        {'id': 'insider_sim', 'name': 'Insider Threat', 'difficulty': 'hard', 'duration': '1.5h'},
        {'id': 'phishing_sim', 'name': 'Phishing Campaign', 'difficulty': 'easy', 'duration': '30m'},
        {'id': 'ddos_sim', 'name': 'DDoS Attack', 'difficulty': 'medium', 'duration': '1h'},
        {'id': 'malware_sim', 'name': 'Malware Propagation', 'difficulty': 'hard', 'duration': '1.5h'}
    ]
    return jsonify(scenarios)

@app.route('/api/simulation/run', methods=['POST'])
def run_simulation():
    """Run a simulation scenario"""
    data = request.json
    scenario_id = data.get('scenario_id', 'apt_sim')
    
    result = dashboard.run_simulation_scenario(scenario_id)
    return jsonify(result)

@app.route('/api/deception/honeypots')
def get_honeypots():
    """Get deception honeypot status"""
    return jsonify(dashboard.get_deception_status())

@app.route('/api/simulation/active')
def get_active_simulations():
    """Get active simulations"""
    return jsonify({
        'active': [
            {'id': 'sim_001', 'scenario': 'APT Simulation', 'progress': 65, 'started': '10:30', 'estimated_completion': '12:00'},
            {'id': 'sim_002', 'scenario': 'Ransomware Attack', 'progress': 30, 'started': '11:15', 'estimated_completion': '12:00'}
        ],
        'queued': [
            {'id': 'sim_003', 'scenario': 'Phishing Campaign', 'scheduled': '14:00'}
        ],
        'completed_today': 3,
        'demo_data': True
    })

@app.route('/api/metrics')
def get_metrics():
    """Get performance metrics"""
    return jsonify({
        'detection_rate': 87.5,
        'response_time': '2.3s',
        'false_positives': 2,
        'true_positives': 18,
        'simulations_completed': 15,
        'honeypot_interactions': 142,
        'avg_threat_score': 7.2,
        'demo_data': True,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'omega_simulation_dashboard',
        'version': '3.0.0',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'uptime': str(datetime.datetime.utcnow() - dashboard.startup_time)
    })

@app.route('/api/system/info')
def system_info():
    """System information endpoint"""
    return jsonify({
        'platform': 'Omega Security Platform',
        'version': '3.0.0',
        'dashboard_version': '1.0.0',
        'environment': 'development',
        'phase': 3,
        'python_version': sys.version.split()[0],
        'demo_mode': True,
        'startup_time': dashboard.startup_time.isoformat() + 'Z',
        'features': [
            'threat_simulation',
            'honeypot_monitoring',
            'real_time_metrics',
            'api_first_design',
            'demo_mode'
        ]
    })

def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🚀 OMEGA PLATFORM SIMULATION DASHBOARD v3.0")
    print("=" * 60)
    print("🌐 Dashboard:  http://localhost:5000")
    print("📊 API Status: http://localhost:5000/api/status")
    print("❤️  Health:     http://localhost:5000/api/health")
    print("=" * 60)
    print("📋 Available API Endpoints:")
    print("   GET  /api/status            - System status")
    print("   GET  /api/health            - Health check")
    print("   GET  /api/system/info       - System information")
    print("   GET  /api/simulation/scenarios - 6 attack scenarios")
    print("   POST /api/simulation/run    - Run simulation")
    print("   GET  /api/simulation/active - Active simulations")
    print("   GET  /api/deception/honeypots - Honeypot status")
    print("   GET  /api/metrics           - Performance metrics")
    print("=" * 60)
    print("⚡ Mode: DEMO (Fully functional with simulated data)")
    print("💡 Tip: Open the dashboard in your browser")
    print("=" * 60)
    print("Press Ctrl+C to stop")
    print("=" * 60)

if __name__ == '__main__':
    print_welcome()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
