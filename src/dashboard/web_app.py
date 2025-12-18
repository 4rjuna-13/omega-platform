#!/usr/bin/env python3
"""
JAIDA Web Dashboard - Modern Flask Interface
"""

from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
from datetime import datetime, timedelta
import json
import os
from threading import Thread
import time

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Database connection
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('data/sovereign_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# Background data updater
class DataUpdater:
    def __init__(self):
        self.cache = {
            'stats': {},
            'alerts': [],
            'timeline': [],
            'last_updated': None
        }
        self.running = True
        
    def update_data(self):
        """Update cached data"""
        while self.running:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Get total alerts
                tables_to_try = ['working_alerts', 'enhanced_alerts', 'simple_alerts', 'alerts']
                total_alerts = 0
                active_table = None
                
                for table in tables_to_try:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        if count > 0:
                            total_alerts = count
                            active_table = table
                            break
                    except:
                        continue
                
                # Get severity breakdown
                severity_counts = {}
                if active_table:
                    cursor.execute(f"SELECT severity, COUNT(*) FROM {active_table} GROUP BY severity")
                    for row in cursor.fetchall():
                        severity_counts[row[0]] = row[1]
                
                # Get source breakdown
                source_counts = {}
                if active_table:
                    cursor.execute(f"SELECT source, COUNT(*) FROM {active_table} GROUP BY source")
                    for row in cursor.fetchall():
                        source_counts[row[0]] = row[1]
                
                # Get recent alerts
                recent_alerts = []
                if active_table:
                    cursor.execute(f"""
                        SELECT timestamp, source, severity, description, confidence
                        FROM {active_table}
                        ORDER BY timestamp DESC
                        LIMIT 50
                    """)
                    for row in cursor.fetchall():
                        recent_alerts.append({
                            'timestamp': row[0],
                            'source': row[1],
                            'severity': row[2],
                            'description': row[3],
                            'confidence': row[4]
                        })
                
                # Calculate threat level
                critical_count = severity_counts.get('CRITICAL', 0) + severity_counts.get('HIGH', 0)
                if critical_count > 10:
                    threat_level = 'CRITICAL'
                    threat_color = '#dc2626'
                elif critical_count > 5:
                    threat_level = 'HIGH'
                    threat_color = '#ea580c'
                elif critical_count > 2:
                    threat_level = 'ELEVATED'
                    threat_color = '#d97706'
                else:
                    threat_level = 'NORMAL'
                    threat_color = '#16a34a'
                
                # Update cache
                self.cache['stats'] = {
                    'total_alerts': total_alerts,
                    'severity_counts': severity_counts,
                    'source_counts': source_counts,
                    'critical_count': critical_count,
                    'threat_level': threat_level,
                    'threat_color': threat_color,
                    'active_table': active_table,
                    'last_updated': datetime.now().isoformat()
                }
                self.cache['alerts'] = recent_alerts
                self.cache['last_updated'] = datetime.now().isoformat()
                
                conn.close()
                
            except Exception as e:
                print(f"Dashboard update error: {e}")
            
            time.sleep(5)  # Update every 5 seconds
    
    def start(self):
        """Start background updater"""
        thread = Thread(target=self.update_data, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop background updater"""
        self.running = False

# Initialize data updater
updater = DataUpdater()
updater.start()

# Routes
@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    """Get system statistics"""
    return jsonify(updater.cache['stats'])

@app.route('/api/alerts')
def api_alerts():
    """Get recent alerts"""
    return jsonify(updater.cache['alerts'])

@app.route('/api/timeline')
def api_timeline():
    """Get timeline data"""
    # Generate dummy timeline for now
    timeline = []
    for i in range(24):
        hour = (datetime.now() - timedelta(hours=i)).strftime('%H:00')
        timeline.append({
            'hour': hour,
            'alerts': (updater.cache['stats'].get('total_alerts', 0) // 24) + (i % 3)
        })
    return jsonify(list(reversed(timeline)))

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_age': updater.cache.get('last_updated', 'never')
    })

# Static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    # Create required directories
    os.makedirs('src/dashboard/templates', exist_ok=True)
    os.makedirs('src/dashboard/static/css', exist_ok=True)
    os.makedirs('src/dashboard/static/js', exist_ok=True)
    
    print("🚀 Starting JAIDA Web Dashboard on http://localhost:8080")
    print("📊 Open browser to http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
