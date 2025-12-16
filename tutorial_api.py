"""
TUTORIAL ENGINE API ENDPOINTS
"""

from flask import jsonify, request

def setup_tutorial_api(app, tutorial_engine, socketio=None):
    """Setup tutorial API endpoints"""
    
    @app.route('/api/tutorial/status', methods=['GET'])
    def get_tutorial_status():
        status = tutorial_engine.get_tutorial_status()
        return jsonify(status)
    
    @app.route('/api/tutorial/start', methods=['POST'])
    def start_tutorial():
        data = request.get_json() or {}
        tutorial_id = data.get('tutorial', 'welcome')
        result = tutorial_engine.start_tutorial(tutorial_id)
        return jsonify(result)
    
    @app.route('/api/tutorial/complete-step', methods=['POST'])
    def complete_tutorial_step():
        data = request.get_json() or {}
        tutorial_id = data.get('tutorial')
        step_id = data.get('step')
        
        if not tutorial_id or not step_id:
            return jsonify({"status": "error", "message": "Missing tutorial or step ID"})
        
        result = tutorial_engine.complete_step(tutorial_id, step_id)
        return jsonify(result)
    
    @app.route('/api/tutorial/sandbox/activate', methods=['POST'])
    def activate_sandbox():
        result = tutorial_engine.activate_sandbox_mode()
        return jsonify(result)
    
    @app.route('/api/tutorial/sandbox/deactivate', methods=['POST'])
    def deactivate_sandbox():
        result = tutorial_engine.deactivate_sandbox_mode()
        return jsonify(result)
    
    @app.route('/api/tutorial/recommended', methods=['GET'])
    def get_recommended():
        recommended = tutorial_engine.get_recommended_tutorial()
        return jsonify({"recommended": recommended})
    
    @app.route('/api/tutorial/list', methods=['GET'])
    def list_tutorials():
        tutorials = tutorial_engine.tutorials
        simplified = {}
        for tid, t in tutorials.items():
            simplified[tid] = {
                "title": t["title"],
                "description": t["description"],
                "difficulty": t["difficulty"],
                "estimated_time": t["estimated_time"]
            }
        return jsonify(simplified)
    
    # WebSocket events (only if socketio is provided)
    if socketio:
        @socketio.on('request_tutorial_status')
        def handle_tutorial_status():
            status = tutorial_engine.get_tutorial_status()
            socketio.emit('tutorial_status', status)
        
        @socketio.on('start_tutorial')
        def handle_start_tutorial(data):
            tutorial_id = data.get('tutorial', 'welcome')
            result = tutorial_engine.start_tutorial(tutorial_id)
            socketio.emit('tutorial_start_result', result)
        
        @socketio.on('complete_tutorial_step')
        def handle_complete_step(data):
            tutorial_id = data.get('tutorial')
            step_id = data.get('step')
            if tutorial_id and step_id:
                result = tutorial_engine.complete_step(tutorial_id, step_id)
                socketio.emit('step_completed', result)

