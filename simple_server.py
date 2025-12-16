#!/usr/bin/env python3
"""
Simple Omega Command Center Server
"""

from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

print("\n" + "="*60)
print("   SIMPLE OMEGA COMMAND CENTER")
print("="*60)

@app.route('/')
def index():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Serving main page")
    return render_template('simple_command_center.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"\n🚀 Server: http://localhost:8080")
    print("💡 Open in browser and click 'Advanced Mode' button")
    print("-" * 60)
    app.run(host='0.0.0.0', port=8080, debug=False)
