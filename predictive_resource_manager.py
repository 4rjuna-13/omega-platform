#!/usr/bin/env python3
"""
Predictive Resource Management with ML-like pattern detection
"""

import os
import sys
import json
import time
import psutil
import numpy as np
from datetime import datetime, timedelta
from collections import deque
from pathlib import Path
import sqlite3

class PredictiveResourceManager:
    def __init__(self, history_size=1000):
        self.history_size = history_size
        self.home = Path.home()
        self.data_dir = self.home / ".context" / "predictive_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Resource history
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.disk_history = deque(maxlen=history_size)
        self.io_history = deque(maxlen=history_size)
        
        # Pattern database
        self.pattern_db = self.data_dir / "resource_patterns.db"
        self.init_pattern_database()
        
        # Load existing patterns
        self.load_patterns()
    
    def init_pattern_database(self):
        """Initialize pattern database"""
        conn = sqlite3.connect(self.pattern_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS resource_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT NOT NULL,
            pattern_data TEXT NOT NULL,
            confidence REAL DEFAULT 0.0,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            occurrences INTEGER DEFAULT 1
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            resource_type TEXT NOT NULL,
            predicted_value REAL,
            actual_value REAL,
            accuracy REAL,
            prediction_horizon INTEGER
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_metrics(self):
        """Collect current resource metrics"""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "percent": psutil.cpu_percent(interval=1),
                "per_core": psutil.cpu_percent(interval=1, percpu=True)
            },
            "memory": {
                "percent": psutil.virtual_memory().percent,
                "available": psutil.virtual_memory().available,
                "used": psutil.virtual_memory().used
            },
            "disk": {
                "percent": psutil.disk_usage('/').percent,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free
            },
            "io": {
                "read_bytes": psutil.disk_io_counters().read_bytes,
                "write_bytes": psutil.disk_io_counters().write_bytes
            },
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }
        
        # Add to history
        self.cpu_history.append(metrics["cpu"]["percent"])
        self.memory_history.append(metrics["memory"]["percent"])
        self.disk_history.append(metrics["disk"]["percent"])
        self.io_history.append(metrics["io"]["read_bytes"] + metrics["io"]["write_bytes"])
        
        return metrics
    
    def detect_patterns(self, window_size=10):
        """Detect patterns in resource usage"""
        patterns = []
        
        if len(self.cpu_history) >= window_size * 2:
            # Convert to numpy for analysis
            cpu_data = np.array(list(self.cpu_history)[-window_size*2:])
            mem_data = np.array(list(self.memory_history)[-window_size*2:])
            
            # Detect trends
            cpu_trend = self.calculate_trend(cpu_data[-window_size:])
            mem_trend = self.calculate_trend(mem_data[-window_size:])
            
            # Detect periodicity
            cpu_periodic = self.detect_periodicity(cpu_data)
            mem_periodic = self.detect_periodicity(mem_data)
            
            # Detect spikes
            cpu_spikes = self.detect_spikes(cpu_data)
            mem_spikes = self.detect_spikes(mem_data)
            
            patterns.extend([
                {"type": "cpu_trend", "value": cpu_trend, "data": cpu_data.tolist()},
                {"type": "memory_trend", "value": mem_trend, "data": mem_data.tolist()},
                {"type": "cpu_periodicity", "value": cpu_periodic, "data": cpu_data.tolist()},
                {"type": "memory_periodicity", "value": mem_periodic, "data": mem_data.tolist()},
                {"type": "cpu_spikes", "value": len(cpu_spikes), "data": cpu_spikes},
                {"type": "memory_spikes", "value": len(mem_spikes), "data": mem_spikes}
            ])
        
        return patterns
    
    def calculate_trend(self, data):
        """Calculate linear trend"""
        if len(data) < 2:
            return 0
        
        x = np.arange(len(data))
        slope, _ = np.polyfit(x, data, 1)
        return slope
    
    def detect_periodicity(self, data, max_lag=20):
        """Detect periodicity using autocorrelation"""
        if len(data) < max_lag * 2:
            return None
        
        # Simple autocorrelation
        correlations = []
        for lag in range(1, max_lag + 1):
            if lag < len(data):
                correlation = np.corrcoef(data[:-lag], data[lag:])[0, 1]
                correlations.append((lag, abs(correlation)))
        
        # Find lag with highest correlation
        if correlations:
            correlations.sort(key=lambda x: x[1], reverse=True)
            best_lag, best_corr = correlations[0]
            
            if best_corr > 0.7:  # Strong correlation threshold
                return {"period": best_lag, "confidence": best_corr}
        
        return None
    
    def detect_spikes(self, data, threshold_std=2.5):
        """Detect statistical spikes"""
        if len(data) < 10:
            return []
        
        mean = np.mean(data)
        std = np.std(data)
        
        spikes = []
        for i, value in enumerate(data):
            if abs(value - mean) > threshold_std * std:
                spikes.append({
                    "index": i,
                    "value": value,
                    "deviation": (value - mean) / std
                })
        
        return spikes
    
    def predict_resource_usage(self, horizon=5):
        """Predict future resource usage"""
        predictions = {}
        
        if len(self.cpu_history) >= 20:
            # Simple moving average prediction
            cpu_pred = self.predict_using_sma(list(self.cpu_history), horizon)
            mem_pred = self.predict_using_sma(list(self.memory_history), horizon)
            disk_pred = self.predict_using_sma(list(self.disk_history), horizon)
            
            predictions = {
                "cpu": cpu_pred,
                "memory": mem_pred,
                "disk": disk_pred,
                "horizon": horizon,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save prediction for later accuracy evaluation
            self.save_prediction(predictions)
        
        return predictions
    
    def predict_using_sma(self, data, horizon, window=5):
        """Predict using simple moving average"""
        if len(data) < window:
            return {"current": data[-1] if data else 0, "predicted": None}
        
        recent = data[-window:]
        current = recent[-1]
        sma = sum(recent) / len(recent)
        
        # Simple trend-based prediction
        trend = self.calculate_trend(np.array(recent))
        predicted = current + (trend * horizon)
        
        return {
            "current": current,
            "sma": sma,
            "trend": trend,
            "predicted": max(0, min(100, predicted)),  # Clamp to 0-100%
            "window": window,
            "confidence": 1.0 / (1.0 + abs(trend))  # Higher confidence for stable trends
        }
    
    def save_prediction(self, prediction):
        """Save prediction to database"""
        conn = sqlite3.connect(self.pattern_db)
        cursor = conn.cursor()
        
        for resource_type, pred_data in prediction.items():
            if resource_type in ["cpu", "memory", "disk"] and isinstance(pred_data, dict):
                cursor.execute('''
                INSERT INTO predictions 
                (timestamp, resource_type, predicted_value, prediction_horizon)
                VALUES (?, ?, ?, ?)
                ''', (
                    prediction["timestamp"],
                    resource_type,
                    pred_data.get("predicted"),
                    prediction.get("horizon", 5)
                ))
        
        conn.commit()
        conn.close()
    
    def evaluate_prediction_accuracy(self):
        """Evaluate accuracy of past predictions"""
        conn = sqlite3.connect(self.pattern_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM predictions 
        WHERE actual_value IS NULL 
        AND timestamp < datetime('now', '-5 minutes')
        ORDER BY timestamp DESC
        LIMIT 50
        ''')
        
        old_predictions = cursor.fetchall()
        
        evaluations = []
        for pred in old_predictions:
            pred_id, timestamp, resource_type, predicted, actual, accuracy, horizon = pred
            
            # Get actual value from history (approximate)
            actual_value = self.get_actual_value_at_time(resource_type, timestamp, horizon)
            
            if actual_value is not None:
                # Calculate accuracy
                if predicted is not None:
                    error = abs(predicted - actual_value)
                    accuracy_score = max(0, 1 - error / 100)  # Normalized accuracy
                    
                    # Update prediction with actual value
                    cursor.execute('''
                    UPDATE predictions 
                    SET actual_value = ?, accuracy = ?
                    WHERE id = ?
                    ''', (actual_value, accuracy_score, pred_id))
                    
                    evaluations.append({
                        "prediction_id": pred_id,
                        "resource": resource_type,
                        "predicted": predicted,
                        "actual": actual_value,
                        "accuracy": accuracy_score,
                        "error": error
                    })
        
        conn.commit()
        conn.close()
        
        return evaluations
    
    def get_actual_value_at_time(self, resource_type, timestamp_str, horizon):
        """Get actual resource value at prediction time + horizon"""
        # This is a simplified version - in production, you'd query stored metrics
        # For now, we'll use current history
        if resource_type == "cpu" and self.cpu_history:
            idx = min(horizon, len(self.cpu_history) - 1)
            return list(self.cpu_history)[-idx-1] if idx >= 0 else None
        elif resource_type == "memory" and self.memory_history:
            idx = min(horizon, len(self.memory_history) - 1)
            return list(self.memory_history)[-idx-1] if idx >= 0 else None
        
        return None
    
    def generate_recommendations(self, predictions, patterns):
        """Generate actionable recommendations"""
        recommendations = []
        
        # CPU recommendations
        cpu_pred = predictions.get("cpu", {})
        if cpu_pred.get("predicted", 0) > 80:
            recommendations.append({
                "priority": "high",
                "resource": "cpu",
                "issue": f"CPU predicted to reach {cpu_pred['predicted']:.1f}%",
                "action": "Consider limiting background processes",
                "command": "ps aux --sort=-%cpu | head -5"
            })
        
        # Memory recommendations
        mem_pred = predictions.get("memory", {})
        if mem_pred.get("predicted", 0) > 85:
            recommendations.append({
                "priority": "high",
                "resource": "memory",
                "issue": f"Memory predicted to reach {mem_pred['predicted']:.1f}%",
                "action": "Clear memory caches",
                "command": "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches"
            })
        
        # Disk recommendations
        disk_pred = predictions.get("disk", {})
        if disk_pred.get("predicted", 0) > 90:
            recommendations.append({
                "priority": "critical",
                "resource": "disk",
                "issue": f"Disk space predicted to reach {disk_pred['predicted']:.1f}%",
                "action": "Clean temporary files immediately",
                "command": "organize --clean-temp --aggressive"
            })
        
        # Pattern-based recommendations
        for pattern in patterns:
            if pattern["type"] == "cpu_spikes" and pattern["value"] > 3:
                recommendations.append({
                    "priority": "medium",
                    "resource": "cpu",
                    "issue": f"Detected {pattern['value']} CPU spikes recently",
                    "action": "Investigate spike patterns",
                    "command": "system-notifier add 'cpu' 'CPU spike pattern detected' 'medium'"
                })
        
        return recommendations
    
    def load_patterns(self):
        """Load learned patterns from database"""
        conn = sqlite3.connect(self.pattern_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT pattern_type, pattern_data, confidence, occurrences 
        FROM resource_patterns 
        ORDER BY last_seen DESC
        LIMIT 20
        ''')
        
        self.learned_patterns = []
        for row in cursor.fetchall():
            pattern_type, pattern_data, confidence, occurrences = row
            try:
                data = json.loads(pattern_data)
                self.learned_patterns.append({
                    "type": pattern_type,
                    "data": data,
                    "confidence": confidence,
                    "occurrences": occurrences
                })
            except:
                pass
        
        conn.close()
    
    def run_analysis_cycle(self):
        """Run one complete analysis cycle"""
        # Collect current metrics
        metrics = self.collect_metrics()
        
        # Detect patterns
        patterns = self.detect_patterns()
        
        # Predict future usage
        predictions = self.predict_resource_usage(horizon=10)
        
        # Evaluate past predictions
        evaluations = self.evaluate_prediction_accuracy()
        
        # Generate recommendations
        recommendations = self.generate_recommendations(predictions, patterns)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "current_metrics": metrics,
            "detected_patterns": patterns,
            "predictions": predictions,
            "evaluations": evaluations[:5],  # Limit to 5 most recent
            "recommendations": recommendations
        }

def start_predictive_manager(interval=60):
    """Start predictive resource manager"""
    manager = PredictiveResourceManager()
    
    print("🧠 Starting Predictive Resource Manager")
    print(f"📊 Analysis interval: {interval} seconds")
    print("=" * 50)
    
    while True:
        try:
            result = manager.run_analysis_cycle()
            
            # Display critical information
            current_cpu = result["current_metrics"]["cpu"]["percent"]
            current_mem = result["current_metrics"]["memory"]["percent"]
            current_disk = result["current_metrics"]["disk"]["percent"]
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] CPU: {current_cpu:.1f}% | "
                  f"Mem: {current_mem:.1f}% | Disk: {current_disk:.1f}%")
            
            # Show recommendations if any
            if result["recommendations"]:
                print("💡 Recommendations:")
                for rec in result["recommendations"]:
                    print(f"  • [{rec['priority'].upper()}] {rec['issue']}")
            
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Predictive manager stopped by user")
            break
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        start_predictive_manager()
    else:
        manager = PredictiveResourceManager()
        result = manager.run_analysis_cycle()
        
        print(json.dumps(result, indent=2))
