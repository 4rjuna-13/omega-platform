#!/usr/bin/env python3
"""
Simple JAIDA Dashboard
"""

from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def get_stats():
    """Get system stats"""
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    
    stats = {
        'total_alerts': 0,
        'severity_counts': {},
        'source_counts': {},
        'recent_alerts': [],
        'threat_level': 'NORMAL',
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Try working_alerts table
        cursor.execute("SELECT COUNT(*) FROM working_alerts")
        stats['total_alerts'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT severity, COUNT(*) FROM working_alerts GROUP BY severity")
        for row in cursor.fetchall():
            stats['severity_counts'][row[0]] = row[1]
        
        cursor.execute("SELECT source, COUNT(*) FROM working_alerts GROUP BY source")
        for row in cursor.fetchall():
            stats['source_counts'][row[0]] = row[1]
        
        cursor.execute("SELECT timestamp, source, severity, description FROM working_alerts ORDER BY timestamp DESC LIMIT 10")
        stats['recent_alerts'] = [
            {'timestamp': r[0], 'source': r[1], 'severity': r[2], 'description': r[3]}
            for r in cursor.fetchall()
        ]
    except:
        # Table might not exist yet
        pass
    
    conn.close()
    
    # Calculate threat level
    critical = stats['severity_counts'].get('CRITICAL', 0) + stats['severity_counts'].get('HIGH', 0)
    if critical > 5:
        stats['threat_level'] = 'CRITICAL'
    elif critical > 2:
        stats['threat_level'] = 'HIGH'
    else:
        stats['threat_level'] = 'NORMAL'
    
    return stats

@app.route('/')
def index():
    """Main page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>JAIDA Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #0f172a; color: white; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #1e293b; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; }
            .threat-level { font-size: 24px; font-weight: bold; padding: 10px; border-radius: 5px; text-align: center; }
            .critical { background: #dc2626; }
            .high { background: #ea580c; }
            .normal { background: #16a34a; }
            table { width: 100%; border-collapse: collapse; background: #1e293b; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #334155; }
            th { background: #0f172a; }
        </style>
        <script>
            async function loadData() {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                // Update stats
                document.getElementById('totalAlerts').textContent = data.total_alerts;
                document.getElementById('criticalCount').textContent = 
                    (data.severity_counts.CRITICAL || 0) + (data.severity_counts.HIGH || 0);
                document.getElementById('dataSources').textContent = Object.keys(data.source_counts).length;
                
                // Update threat level
                const threatEl = document.getElementById('threatLevel');
                threatEl.textContent = data.threat_level;
                threatEl.className = 'threat-level ' + data.threat_level.toLowerCase();
                
                // Update table
                const tbody = document.getElementById('alertsBody');
                tbody.innerHTML = '';
                data.recent_alerts.forEach(alert => {
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td>${alert.timestamp.slice(11, 19)}</td>
                        <td>${alert.source}</td>
                        <td>${alert.severity}</td>
                        <td>${alert.description}</td>
                    `;
                });
                
                document.getElementById('lastUpdated').textContent = 
                    'Last updated: ' + new Date().toLocaleTimeString();
            }
            
            // Load data immediately and every 5 seconds
            loadData();
            setInterval(loadData, 5000);
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏛️ JAIDA-OMEGA-SAIOS Dashboard</h1>
                <p>Real-time threat intelligence monitoring</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Alerts</h3>
                    <div id="totalAlerts" style="font-size: 36px; font-weight: bold;">0</div>
                </div>
                
                <div class="stat-card">
                    <h3>Critical Alerts</h3>
                    <div id="criticalCount" style="font-size: 36px; font-weight: bold; color: #dc2626;">0</div>
                </div>
                
                <div class="stat-card">
                    <h3>Data Sources</h3>
                    <div id="dataSources" style="font-size: 36px; font-weight: bold;">0</div>
                </div>
                
                <div class="stat-card">
                    <h3>Threat Level</h3>
                    <div id="threatLevel" class="threat-level normal">NORMAL</div>
                </div>
            </div>
            
            <h2>Recent Alerts</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Source</th>
                        <th>Severity</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody id="alertsBody">
                    <!-- Alerts will be inserted here -->
                </tbody>
            </table>
            
            <div style="margin-top: 20px; text-align: center; color: #94a3b8;">
                <div id="lastUpdated">Loading...</div>
                <div>Auto-refreshes every 5 seconds</div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/api/stats')
def api_stats():
    """API endpoint for stats"""
    return jsonify(get_stats())

if __name__ == '__main__':
    print("🚀 Starting JAIDA Dashboard on http://localhost:8080")
    print("📊 Open browser to http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)
