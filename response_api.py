"""
AUTONOMOUS RESPONSE API
"""

from flask import jsonify, request

def setup_response_api(app, response_engine):
    """Setup response API endpoints"""
    
    @app.route('/api/response/status', methods=['GET'])
    def get_response_status():
        stats = response_engine.get_response_stats()
        return jsonify(stats)
    
    @app.route('/api/response/activate', methods=['POST'])
    def activate_response():
        data = request.get_json() or {}
        level = data.get('level', 'MODERATE')
        result = response_engine.activate_response_mode(level)
        return jsonify(result)
    
    @app.route('/api/response/deactivate', methods=['POST'])
    def deactivate_response():
        result = response_engine.deactivate_response_mode()
        return jsonify(result)
    
    @app.route('/api/response/log', methods=['GET'])
    def get_response_log():
        limit = request.args.get('limit', 10, type=int)
        logs = response_engine.get_response_log(limit)
        return jsonify(logs)
    
    @app.route('/api/response/test', methods=['POST'])
    def test_response():
        result = response_engine.test_response()
        return jsonify(result)

