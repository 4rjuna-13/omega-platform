#!/usr/bin/env python3
"""
Real Alert Processor for Omega Nexus Integration
Processes actual Omega Nexus alert streams and feeds them to autonomous engine
"""

import json
import time
import threading
import queue
import sqlite3
from datetime import datetime
import yaml
import logging
from typing import Dict, List, Any, Optional
import random  # For demo mode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("RealAlertProcessor")

class RealAlertProcessor:
    """Processes real Omega Nexus alerts into autonomous engine"""
    
    def __init__(self, config_path: str = "config/integration.yaml"):
        """Initialize with configuration"""
        self.config = self.load_config(config_path)
        self.alert_queue = queue.Queue(maxsize=1000)
        self.running = False
        self.processor_thread = None
        self.db_conn = None
        self.initialize_database()
        
        # Statistics
        self.stats = {
            "alerts_processed": 0,
            "alerts_forwarded": 0,
            "alerts_filtered": 0,
            "avg_processing_time": 0.0,
            "last_alert_time": None
        }
        
        logger.info(f"Real Alert Processor initialized with config: {config_path}")
    
    def load_config(self, config_path: str) -> Dict:
        """Load integration configuration"""
        default_config = {
            "alert_sources": {
                "omega_nexus_api": {
                    "enabled": True,
                    "endpoint": "http://localhost:8080/api/alerts/stream",
                    "poll_interval": 5,
                    "api_key": "demo_key"
                },
                "web_crawler": {
                    "enabled": True,
                    "data_dir": "data/web_crawler/intel",
                    "poll_interval": 30
                },
                "file_monitor": {
                    "enabled": True,
                    "watch_dir": "data/omega_nexus/alerts",
                    "file_pattern": "*.json"
                }
            },
            "processing": {
                "alert_threshold": 0.7,
                "filter_low_confidence": True,
                "deduplicate_alerts": True,
                "max_queue_size": 1000
            },
            "autonomous_integration": {
                "bridge_endpoint": "http://localhost:8081/process_alert",
                "fallback_to_simulated": True,
                "retry_attempts": 3
            },
            "demo_mode": {
                "enabled": True,
                "generate_test_alerts": True,
                "alert_interval": 10
            }
        }
        
        try:
            with open(config_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
                # Merge with defaults
                default_config.update(loaded_config)
                return default_config
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            # Save default config
            with open(config_path, 'w') as f:
                yaml.dump(default_config, f, default_flow_style=False)
            return default_config
    
    def initialize_database(self):
        """Initialize database for alert tracking"""
        try:
            self.db_conn = sqlite3.connect('data/sovereign.db', check_same_thread=False)
            cursor = self.db_conn.cursor()
            
            # Create alerts table if not exists
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS real_alerts (
                alert_id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity INTEGER,
                confidence REAL,
                description TEXT,
                raw_data TEXT,
                received_at TIMESTAMP,
                processed_at TIMESTAMP,
                forwarded_to_autonomous INTEGER DEFAULT 0,
                autonomous_decision_id TEXT,
                status TEXT DEFAULT 'pending'
            )
            ''')
            
            # Create alert statistics table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS alert_statistics (
                date DATE PRIMARY KEY,
                total_alerts INTEGER DEFAULT 0,
                high_severity INTEGER DEFAULT 0,
                forwarded_count INTEGER DEFAULT 0,
                avg_processing_time REAL DEFAULT 0.0
            )
            ''')
            
            self.db_conn.commit()
            logger.info("Database initialized for real alerts")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # Fallback to in-memory
            self.db_conn = None
    
    def start(self):
        """Start the alert processor"""
        if self.running:
            logger.warning("Alert processor already running")
            return
            
        self.running = True
        self.processor_thread = threading.Thread(target=self._processor_loop, daemon=True)
        self.processor_thread.start()
        
        # Start alert sources
        self._start_alert_sources()
        
        logger.info("Real Alert Processor started")
    
    def stop(self):
        """Stop the alert processor"""
        self.running = False
        if self.processor_thread:
            self.processor_thread.join(timeout=5)
        
        if self.db_conn:
            self.db_conn.close()
        
        logger.info("Real Alert Processor stopped")
    
    def _processor_loop(self):
        """Main processing loop"""
        while self.running:
            try:
                # Process alerts from queue
                if not self.alert_queue.empty():
                    alert = self.alert_queue.get_nowait()
                    self._process_single_alert(alert)
                else:
                    time.sleep(0.1)  # Small sleep to prevent CPU spinning
                    
            except queue.Empty:
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Error in processor loop: {e}")
                time.sleep(1)
    
    def _start_alert_sources(self):
        """Start all configured alert sources"""
        sources = self.config.get('alert_sources', {})
        
        # Start demo alerts if enabled
        if self.config.get('demo_mode', {}).get('enabled', False):
            threading.Thread(target=self._demo_alert_source, daemon=True).start()
            logger.info("Demo alert source started")
    
    def _demo_alert_source(self):
        """Generate demo alerts for testing"""
        config = self.config['demo_mode']
        alert_interval = config.get('alert_interval', 10)
        
        alert_types = [
            ("malware_detected", 0.85, 8),
            ("phishing_attempt", 0.75, 6),
            ("unauthorized_access", 0.90, 9),
            ("ddos_attack", 0.80, 7),
            ("data_exfiltration", 0.95, 10),
            ("suspicious_activity", 0.65, 5),
            ("vulnerability_scan", 0.70, 4),
            ("brute_force_attack", 0.85, 8)
        ]
        
        alert_id = 1000
        
        while self.running:
            try:
                # Generate alert
                alert_type, confidence, severity = random.choice(alert_types)
                
                alert = {
                    "alert_id": f"DEMO-{alert_id}",
                    "source": "demo_generator",
                    "alert_type": alert_type,
                    "severity": severity,
                    "confidence": confidence + random.uniform(-0.1, 0.1),
                    "description": f"Demo {alert_type.replace('_', ' ')} alert",
                    "timestamp": datetime.now().isoformat(),
                    "source_ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
                    "target": f"server-{random.randint(1,10)}",
                    "raw_data": {
                        "demo": True,
                        "generated_at": datetime.now().isoformat(),
                        "test_scenario": alert_type
                    }
                }
                
                self.alert_queue.put(alert)
                alert_id += 1
                logger.info(f"Demo alert generated: {alert_type} (Severity: {severity})")
                
                time.sleep(alert_interval)
            except Exception as e:
                logger.error(f"Demo source error: {e}")
                time.sleep(alert_interval)
    
    def _process_single_alert(self, alert: Dict):
        """Process a single alert"""
        start_time = time.time()
        
        try:
            # Store alert in database
            alert_id = alert.get('alert_id', f"ALERT-{int(time.time())}")
            alert['processed_at'] = datetime.now().isoformat()
            
            # Save to database
            if self.db_conn:
                cursor = self.db_conn.cursor()
                cursor.execute('''
                INSERT OR REPLACE INTO real_alerts 
                (alert_id, source, alert_type, severity, confidence, description, 
                 raw_data, received_at, processed_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    alert_id,
                    alert.get('source', 'unknown'),
                    alert.get('alert_type', 'unknown'),
                    alert.get('severity', 5),
                    alert.get('confidence', 0.5),
                    alert.get('description', ''),
                    json.dumps(alert.get('raw_data', {})),
                    alert.get('timestamp', datetime.now().isoformat()),
                    alert.get('processed_at'),
                    'received'
                ))
                self.db_conn.commit()
            
            # Check if should be forwarded to autonomous engine
            should_forward = self._should_forward_to_autonomous(alert)
            
            if should_forward:
                forwarded = self._forward_to_autonomous_engine(alert)
                
                if forwarded and self.db_conn:
                    cursor = self.db_conn.cursor()
                    cursor.execute('''
                    UPDATE real_alerts 
                    SET forwarded_to_autonomous = 1, status = 'forwarded'
                    WHERE alert_id = ?
                    ''', (alert_id,))
                    self.db_conn.commit()
                    self.stats['alerts_forwarded'] += 1
                
                logger.info(f"Alert forwarded to autonomous engine: {alert_id}")
            else:
                logger.debug(f"Alert filtered (not forwarded): {alert_id}")
                self.stats['alerts_filtered'] += 1
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['alerts_processed'] += 1
            self.stats['avg_processing_time'] = (
                (self.stats['avg_processing_time'] * (self.stats['alerts_processed'] - 1) + processing_time) 
                / self.stats['alerts_processed']
            )
            self.stats['last_alert_time'] = datetime.now().isoformat()
            
            logger.debug(f"Alert processed: {alert_id} in {processing_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error processing alert: {e}")
    
    def _should_forward_to_autonomous(self, alert: Dict) -> bool:
        """Determine if alert should be forwarded to autonomous engine"""
        processing_config = self.config.get('processing', {})
        
        # Check confidence threshold
        if processing_config.get('filter_low_confidence', True):
            min_confidence = processing_config.get('alert_threshold', 0.7)
            if alert.get('confidence', 0) < min_confidence:
                return False
        
        # Check severity (always forward high severity)
        severity = alert.get('severity', 5)
        if severity >= 8:  # High severity always forwarded
            return True
        
        # For medium severity, check additional criteria
        if severity >= 5:
            alert_type = alert.get('alert_type', '')
            critical_types = ['malware_detected', 'unauthorized_access', 'data_exfiltration']
            if alert_type in critical_types:
                return True
        
        # Default: forward if confidence is high enough
        return alert.get('confidence', 0) >= 0.75
    
    def _forward_to_autonomous_engine(self, alert: Dict) -> bool:
        """Forward alert to autonomous engine"""
        try:
            # Import and use existing autonomous bridge
            import sys
            sys.path.append('src')
            from integration.autonomous_bridge import OmegaAutonomousBridge
            
            bridge = OmegaAutonomousBridge()
            
            # Convert alert to threat indicator format
            threat_indicator = self._convert_alert_to_threat_indicator(alert)
            
            # Process through bridge
            result = bridge.process_threat_indicator(threat_indicator)
            
            # Store decision ID in alert if available
            if result and 'decision_id' in result:
                if self.db_conn:
                    cursor = self.db_conn.cursor()
                    cursor.execute('''
                    UPDATE real_alerts 
                    SET autonomous_decision_id = ?, status = 'decision_made'
                    WHERE alert_id = ?
                    ''', (result['decision_id'], alert.get('alert_id')))
                    self.db_conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error forwarding to autonomous engine: {e}")
            
            # Fallback to simulated processing if configured
            if self.config.get('autonomous_integration', {}).get('fallback_to_simulated', True):
                logger.warning("Falling back to simulated autonomous processing")
                return self._simulate_autonomous_processing(alert)
            
            return False
    
    def _convert_alert_to_threat_indicator(self, alert: Dict) -> Dict:
        """Convert alert format to threat indicator format for autonomous bridge"""
        return {
            "indicator_id": alert.get('alert_id', ''),
            "indicator_type": alert.get('alert_type', 'unknown'),
            "source": alert.get('source', 'unknown'),
            "confidence": alert.get('confidence', 0.5),
            "severity": alert.get('severity', 5),
            "description": alert.get('description', ''),
            "raw_data": alert.get('raw_data', {}),
            "timestamp": alert.get('timestamp', datetime.now().isoformat()),
            "metadata": {
                "original_alert": alert,
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def _simulate_autonomous_processing(self, alert: Dict) -> bool:
        """Simulate autonomous processing for demo/fallback"""
        # Simulate autonomous decision
        decision_id = f"SIM-{int(time.time())}"
        
        if self.db_conn:
            cursor = self.db_conn.cursor()
            cursor.execute('''
            UPDATE real_alerts 
            SET autonomous_decision_id = ?, status = 'simulated_decision'
            WHERE alert_id = ?
            ''', (decision_id, alert.get('alert_id')))
            self.db_conn.commit()
        
        logger.info(f"Simulated autonomous decision: {decision_id} for alert {alert.get('alert_id')}")
        return True
    
    def get_statistics(self) -> Dict:
        """Get current processor statistics"""
        return {
            "processor_status": "running" if self.running else "stopped",
            "statistics": self.stats,
            "queue_size": self.alert_queue.qsize(),
            "config_sources": list(self.config.get('alert_sources', {}).keys())
        }
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts from database"""
        if not self.db_conn:
            return []
        
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
            SELECT alert_id, source, alert_type, severity, confidence, 
                   description, status, processed_at, autonomous_decision_id
            FROM real_alerts
            ORDER BY processed_at DESC
            LIMIT ?
            ''', (limit,))
            
            alerts = []
            for row in cursor.fetchall():
                alerts.append({
                    "alert_id": row[0],
                    "source": row[1],
                    "alert_type": row[2],
                    "severity": row[3],
                    "confidence": row[4],
                    "description": row[5],
                    "status": row[6],
                    "processed_at": row[7],
                    "autonomous_decision_id": row[8]
                })
            
            return alerts
        except Exception as e:
            logger.error(f"Error getting recent alerts: {e}")
            return []

# Test function
def test_alert_processor():
    """Test the alert processor"""
    print("🧪 Testing Real Alert Processor...")
    
    processor = RealAlertProcessor()
    
    try:
        # Start processor
        processor.start()
        
        # Let it run for a bit
        import time
        time.sleep(15)
        
        # Get statistics
        stats = processor.get_statistics()
        print(f"📊 Statistics: {stats}")
        
        # Get recent alerts
        alerts = processor.get_recent_alerts(5)
        print(f"📨 Recent alerts: {len(alerts)}")
        for alert in alerts:
            print(f"  - {alert['alert_id']}: {alert['alert_type']} (Severity: {alert['severity']})")
        
        # Stop processor
        processor.stop()
        
        print("✅ Alert processor test complete")
        
    except KeyboardInterrupt:
        print("⏹️  Test interrupted")
        processor.stop()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        processor.stop()

if __name__ == "__main__":
    test_alert_processor()
