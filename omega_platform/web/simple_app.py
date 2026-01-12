"""
Simple Omega Platform Web Interface
"""
from flask import Flask, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "Omega Platform v4.5",
        "message": "Enhanced platform running"
    })

@app.route('/api/status')
def status():
    return jsonify({
        "version": "4.5",
        "modules": ["MITRE ATT&CK", "Scenario Manager"],
        "status": "operational"
    })

if __name__ == '__main__':
    print("Starting Omega Platform on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
