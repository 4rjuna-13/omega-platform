"""
DECEPTION ENGINE API ENDPOINTS
"""

from flask import jsonify, request

def setup_deception_api(app, deception_engine):
    """Setup deception API endpoints"""
    
    @app.route('/api/deception/status', methods=['GET'])
    def get_deception_status():
        stats = deception_engine.get_deception_stats()
        return jsonify(stats)
    
    @app.route('/api/deception/start', methods=['POST'])
    def start_deception():
        data = request.get_json() or {}
        level = data.get('level', 'MEDIUM')
        result = deception_engine.start_deception_mode(level)
        return jsonify(result)
    
    @app.route('/api/deception/stop', methods=['POST'])
    def stop_deception():
        result = deception_engine.stop_deception_mode()
        return jsonify(result)
    
    @app.route('/api/deception/log', methods=['GET'])
    def get_deception_log():
        logs = deception_engine.deception_log[-50:] if deception_engine.deception_log else []
        return jsonify(logs)

