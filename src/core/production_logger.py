#!/usr/bin/env python3
"""
Production-ready logging and monitoring for JAIDA-Omega-SAIOS
"""

import logging
import logging.handlers
import json
import time
from datetime import datetime
from typing import Dict, Any
import threading
from queue import Queue
import prometheus_client
from prometheus_client import Counter, Gauge, Histogram, start_http_server

class MetricsCollector:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    """Prometheus metrics collector"""
    
    def __init__(self, port=9090):
        self.port = port
        
        # Define metrics
        self.alerts_received = Counter(
            'jaida_alerts_received_total',
            'Total alerts received',
            ['source', 'severity']
        )
        
        self.alerts_processed = Counter(
            'jaida_alerts_processed_total',
            'Total alerts processed'
        )
        
        self.threat_level = Gauge(
            'jaida_threat_level',
            'Current threat level',
            ['level']
        )
        
        self.processing_time = Histogram(
            'jaida_alert_processing_seconds',
            'Alert processing time',
            buckets=[0.1, 0.5, 1, 2, 5]
        )
        
        self.queue_size = Gauge(
            'jaida_queue_size',
            'Alert queue size'
        )
        
        self.errors_total = Counter(
            'jaida_errors_total',
            'Total errors',
            ['component']
        )
        
        # Start metrics server in background
        threading.Thread(
            target=start_http_server,
            args=(self.port,),
            daemon=True
        ).start()
        
        print(f"📊 Metrics server started on port {self.port}")
    
    def record_alert(self, source: str, severity: str):
        """Record received alert"""
        self.alerts_received.labels(source=source, severity=severity).inc()
    
    def record_processing(self, processing_time: float):
        """Record alert processing"""
        self.alerts_processed.inc()
        self.processing_time.observe(processing_time)
    
    def set_threat_level(self, level: str):
        """Set current threat level"""
        # Clear all labels first
        for lbl in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            self.threat_level.labels(level=lbl).set(0)
        self.threat_level.labels(level=level).set(1)
    
    def set_queue_size(self, size: int):
        """Set queue size"""
        self.queue_size.set(size)
    
    def record_error(self, component: str):
        """Record error"""
        self.errors_total.labels(component=component).inc()

class ProductionLogger:
    """Production-ready logging system"""
    
    def __init__(self, name="JAIDA", log_file="logs/jaida.log", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create logs directory if it doesn't exist
        from pathlib import Path
        Path(log_file).parent.mkdir(exist_ok=True)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # JSON formatter for structured logging
        json_formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"module": "%(name)s", "message": "%(message)s", '
            '"data": %(data)s}',
            datefmt="%Y-%m-%dT%H:%M:%SZ"
        )
        
        # Simple formatter for console
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(json_formatter)
        console_handler.setFormatter(simple_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Add custom field for structured data
        old_factory = logging.getLogRecordFactory()
        
        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            record.data = "{}"
            return record
        
        logging.setLogRecordFactory(record_factory)
        
        print(f"📝 Logger initialized: {log_file}")
    
    def _prepare_data(self, data: Dict = None) -> str:
        """Prepare data for JSON logging"""
        if data is None:
            data = {}
        
        # Add common fields
        data.update({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "pid": threading.get_ident()
        })
        
        return json.dumps(data)
    
    def info(self, message: str, data: Dict = None):
        """Log info message with structured data"""
        extra = {'data': self._prepare_data(data)}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, data: Dict = None):
        """Log warning with structured data"""
        extra = {'data': self._prepare_data(data)}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, data: Dict = None):
        """Log error with structured data"""
        extra = {'data': self._prepare_data(data)}
        self.logger.error(message, extra=extra)
    
    def critical(self, message: str, data: Dict = None):
        """Log critical error with structured data"""
        extra = {'data': self._prepare_data(data)}
        self.logger.critical(message, extra=extra)

class AlertQueue:
    """Thread-safe alert queue with metrics"""
    
    def __init__(self, max_size=1000):
        self.queue = Queue(maxsize=max_size)
        self.metrics = MetricsCollector()
        self.processing = False
    
    def put_alert(self, alert: Dict):
        """Add alert to queue"""
        try:
            self.queue.put(alert, timeout=5)
            self.metrics.record_alert(
                alert.get('source', 'unknown'),
                alert.get('severity', 'UNKNOWN')
            )
            self.metrics.set_queue_size(self.queue.qsize())
            return True
        except:
            self.metrics.record_error('queue')
            return False
    
    def process_alerts(self, callback):
        """Process alerts from queue"""
        self.processing = True
        
        while self.processing:
            try:
                alert = self.queue.get(timeout=1)
                start_time = time.time()
                
                # Process alert
                callback(alert)
                
                # Record metrics
                processing_time = time.time() - start_time
                self.metrics.record_processing(processing_time)
                self.metrics.set_queue_size(self.queue.qsize())
                
                self.queue.task_done()
            except:
                continue
    
    def stop(self):
        """Stop processing"""
        self.processing = False

# Global instances
logger = ProductionLogger()
metrics = MetricsCollector()
alert_queue = AlertQueue()

if __name__ == "__main__":
    # Test the logging and metrics system
    logger.info("System started", {"component": "init", "version": "1.0"})
    
    # Simulate some alerts
    test_alerts = [
        {"source": "SIEM", "severity": "HIGH", "message": "Failed login"},
        {"source": "EDR", "severity": "MEDIUM", "message": "Suspicious process"},
        {"source": "Firewall", "severity": "LOW", "message": "Port scan"}
    ]
    
    for alert in test_alerts:
        alert_queue.put_alert(alert)
        logger.info("Alert received", alert)
    
    metrics.set_threat_level("MEDIUM")
    
    logger.info("Test completed", {"alerts_processed": len(test_alerts)})
    
    print("\n✅ Production logging and monitoring system test complete!")
    print(f"📊 Metrics available at: http://localhost:{metrics.port}")
    print(f"📝 Logs written to: logs/jaida.log")
