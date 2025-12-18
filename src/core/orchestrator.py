#!/usr/bin/env python3
"""
🏛️ Core Orchestrator - JAIDA-OMEGA-SAIOS
"""

import sys
import os
import yaml
import sqlite3
from datetime import datetime

class SystemOrchestrator:
    """Main system orchestrator"""
    
    def __init__(self, config_path="config/system.yaml"):
        self.config = self.load_config(config_path)
        self.db_path = self.config.get('database', {}).get('path', 'data/sovereign.db')
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return {}
    
    def check_system_health(self):
        """Check health of system components"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'components': {},
            'overall_health': 'healthy'
        }
        
        # Check database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            if tables:
                health_report['components']['database'] = {
                    'status': 'healthy',
                    'details': f"{len(tables)} tables found"
                }
            else:
                health_report['components']['database'] = {
                    'status': 'degraded',
                    'details': 'No tables found'
                }
                health_report['overall_health'] = 'degraded'
                
        except Exception as e:
            health_report['components']['database'] = {
                'status': 'error',
                'details': str(e)
            }
            health_report['overall_health'] = 'error'
        
        # Check configuration
        if self.config:
            health_report['components']['configuration'] = {
                'status': 'healthy',
                'details': 'Configuration loaded successfully'
            }
        else:
            health_report['components']['configuration'] = {
                'status': 'error',
                'details': 'Failed to load configuration'
            }
            health_report['overall_health'] = 'error'
        
        return health_report
    
    def get_system_status(self):
        """Get current system status from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT component, status, last_updated, details 
                FROM system_status 
                ORDER BY last_updated DESC
            ''')
            
            status = {}
            for row in cursor.fetchall():
                component, status_val, last_updated, details = row
                status[component] = {
                    'status': status_val,
                    'last_updated': last_updated,
                    'details': details
                }
            
            conn.close()
            return status
        except Exception as e:
            print(f"Failed to get system status: {e}")
            return {}

def main():
    """Test the orchestrator"""
    print("Testing System Orchestrator...")
    
    orchestrator = SystemOrchestrator()
    health = orchestrator.check_system_health()
    
    print(f"\nSystem Health: {health['overall_health'].upper()}")
    print(f"Timestamp: {health['timestamp']}")
    
    print("\nComponent Status:")
    for component, info in health['components'].items():
        status_icon = '✅' if info['status'] == 'healthy' else '⚠️ ' if info['status'] == 'degraded' else '❌'
        print(f"  {status_icon} {component}: {info['status']}")
        if info['details']:
            print(f"      Details: {info['details']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
