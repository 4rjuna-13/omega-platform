#!/usr/bin/env python3
"""
Project Omega - Predictive Threat Model
Phase 2C: Intelligence Layer Implementation
"""

import numpy as np
import json
import pickle
from datetime import datetime
from collections import deque
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class ThreatPredictor:
    """ML-based threat prediction and anomaly detection"""
    
    def __init__(self, config_file="threat_model_config.json"):
        self.model = None
        self.scaler = StandardScaler()
        self.training_data = deque(maxlen=5000)  # Store last 5000 events
        self.threshold = 0.65  # Threat score threshold
        self.is_trained = False
        
        # Feature names for security events
        self.features = [
            'port_count', 'unusual_ports', 'http_ports', 'ssh_attempts',
            'failed_logins', 'scan_intensity', 'time_of_day', 'day_of_week',
            'connection_rate', 'packet_size_variance', 'protocol_mix'
        ]
        
        # Load or create config
        self.config = self.load_config(config_file)
        
        print(f"[THREAT PREDICTOR] Initialized with {len(self.features)} features")
        
    def load_config(self, config_file):
        """Load or create configuration"""
        default_config = {
            "model_type": "isolation_forest",
            "contamination": 0.1,
            "n_estimators": 100,
            "training_events_required": 100,
            "retrain_interval": 1000,
            "version": "1.0",
            "created": datetime.now().isoformat()
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                print(f"[THREAT PREDICTOR] Loaded config from {config_file}")
                return {**default_config, **config}
        except FileNotFoundError:
            print(f"[THREAT PREDICTOR] Creating new config")
            return default_config
    
    def save_config(self, config_file="threat_model_config.json"):
        """Save configuration"""
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"[THREAT PREDICTOR] Config saved to {config_file}")
    
    def extract_features(self, event_data):
        """
        Extract features from security event data
        event_data should be a dict with scan/network information
        """
        # Default feature vector
        features = np.zeros(len(self.features))
        
        # 1. Port analysis features
        if 'ports' in event_data:
            ports = event_data['ports']
            features[0] = len(ports)  # port_count
            features[1] = len([p for p in ports if p > 1024]) / max(len(ports), 1)  # unusual_ports ratio
            features[2] = len([p for p in ports if p in [80, 443, 8080]])  # http_ports
        
        # 2. Authentication features
        if 'auth_attempts' in event_data:
            auth = event_data['auth_attempts']
            features[3] = auth.get('ssh', 0)  # ssh_attempts
            features[4] = auth.get('failed', 0)  # failed_logins
        
        # 3. Scan intensity
        if 'scan_data' in event_data:
            scan = event_data['scan_data']
            features[5] = scan.get('intensity', 0)  # scan_intensity
            features[9] = scan.get('packet_variance', 0)  # packet_size_variance
        
        # 4. Temporal features
        now = datetime.now()
        features[6] = now.hour / 24.0  # time_of_day (normalized)
        features[7] = now.weekday() / 7.0  # day_of_week (normalized)
        
        # 5. Network features
        if 'network_stats' in event_data:
            net = event_data['network_stats']
            features[8] = net.get('connections_per_sec', 0)  # connection_rate
            features[10] = net.get('protocol_diversity', 0)  # protocol_mix
        
        return features
    
    def add_training_event(self, event_data, is_threat=False):
        """
        Add event to training data
        is_threat: True if this is a known threat event
        """
        features = self.extract_features(event_data)
        
        # Store with label if available
        event_record = {
            'features': features.tolist(),
            'timestamp': datetime.now().isoformat(),
            'is_threat': is_threat,
            'raw_data': event_data
        }
        
        self.training_data.append(event_record)
        
        # Check if we have enough data to train
        if len(self.training_data) >= self.config['training_events_required']:
            if not self.is_trained:
                self.train_model()
            elif len(self.training_data) % self.config['retrain_interval'] == 0:
                print(f"[THREAT PREDICTOR] Retraining model...")
                self.train_model()
        
        return features
    
    def train_model(self):
        """Train the anomaly detection model"""
        if len(self.training_data) < 50:
            print(f"[THREAT PREDICTOR] Need at least 50 events to train (have {len(self.training_data)})")
            return False
        
        # Extract features and labels
        X = []
        y = []
        
        for event in self.training_data:
            X.append(event['features'])
            y.append(1 if event['is_threat'] else 0)
        
        X = np.array(X)
        y = np.array(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Choose model based on config
        if self.config['model_type'] == 'isolation_forest':
            self.model = IsolationForest(
                contamination=self.config['contamination'],
                n_estimators=self.config['n_estimators'],
                random_state=42
            )
            # Isolation Forest doesn't use y for training
            self.model.fit(X_scaled)
        else:
            # Random Forest for supervised learning
            self.model = RandomForestClassifier(
                n_estimators=self.config['n_estimators'],
                random_state=42
            )
            self.model.fit(X_scaled, y)
        
        self.is_trained = True
        
        # Evaluate model
        if self.config['model_type'] == 'random_forest':
            accuracy = self.model.score(X_scaled, y)
            print(f"[THREAT PREDICTOR] Model trained. Accuracy: {accuracy:.2%}")
        else:
            print(f"[THREAT PREDICTOR] Isolation Forest trained on {len(X)} events")
        
        # Save the model
        self.save_model()
        return True
    
    def predict_threat(self, event_data):
        """
        Predict threat level for an event
        Returns: threat_score (0-1), explanation
        """
        if not self.is_trained or self.model is None:
            return 0.5, "Model not trained yet"
        
        # Extract features
        features = self.extract_features(event_data)
        features_scaled = self.scaler.transform([features])
        
        # Make prediction
        if self.config['model_type'] == 'isolation_forest':
            # Isolation Forest returns -1 for anomaly, 1 for normal
            score = self.model.decision_function(features_scaled)[0]
            # Convert to 0-1 scale (higher = more anomalous)
            threat_score = 1 / (1 + np.exp(-score * 5))
        else:
            # Random Forest returns probability
            prob = self.model.predict_proba(features_scaled)[0]
            threat_score = prob[1] if len(prob) > 1 else prob[0]
        
        # Generate explanation
        explanation = self.explain_prediction(features, threat_score)
        
        return threat_score, explanation
    
    def explain_prediction(self, features, threat_score):
        """Generate human-readable explanation"""
        explanations = []
        
        # Check each feature
        feature_values = {
            'port_count': (features[0], "High port count"),
            'unusual_ports': (features[1], "Many unusual ports"),
            'ssh_attempts': (features[3], "SSH attempts"),
            'failed_logins': (features[4], "Failed logins"),
            'scan_intensity': (features[5], "Scan intensity")
        }
        
        for name, (value, desc) in feature_values.items():
            if value > 0.7:  # High value threshold
                explanations.append(f"{desc}: {value:.2f}")
        
        if threat_score > self.threshold:
            threat_level = "HIGH"
            action = "Investigate immediately"
        elif threat_score > 0.3:
            threat_level = "MEDIUM"
            action = "Monitor closely"
        else:
            threat_level = "LOW"
            action = "Normal activity"
        
        base_explanation = f"Threat Level: {threat_level} ({threat_score:.2%}) - {action}"
        
        if explanations:
            details = "; ".join(explanations)
            return f"{base_explanation}. Key factors: {details}"
        else:
            return base_explanation
    
    def save_model(self, filename="threat_model.pkl"):
        """Save trained model to disk"""
        if self.model:
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'features': self.features,
                'config': self.config,
                'trained_at': datetime.now().isoformat(),
                'training_size': len(self.training_data)
            }
            
            with open(filename, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"[THREAT PREDICTOR] Model saved to {filename}")
            return True
        return False
    
    def load_model(self, filename="threat_model.pkl"):
        """Load trained model from disk"""
        try:
            with open(filename, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.features = model_data['features']
            self.config = model_data['config']
            self.is_trained = True
            
            print(f"[THREAT PREDICTOR] Model loaded from {filename}")
            print(f"  Trained: {model_data['trained_at']}")
            print(f"  Events: {model_data['training_size']}")
            return True
            
        except FileNotFoundError:
            print(f"[THREAT PREDICTOR] No saved model found at {filename}")
            return False
    
    def generate_sample_data(self, count=100):
        """Generate sample training data for testing"""
        print(f"[THREAT PREDICTOR] Generating {count} sample events...")
        
        for i in range(count):
            # Normal events (80%)
            if np.random.random() < 0.8:
                event = {
                    'ports': [80, 443, 22] if np.random.random() > 0.3 else [80, 443],
                    'auth_attempts': {'ssh': np.random.randint(0, 3), 'failed': 0},
                    'scan_data': {'intensity': np.random.random() * 0.3},
                    'network_stats': {'connections_per_sec': np.random.random() * 10}
                }
                self.add_training_event(event, is_threat=False)
            
            # Threat events (20%)
            else:
                event = {
                    'ports': list(range(1, 50)) + [4444, 6667, 31337],
                    'auth_attempts': {'ssh': np.random.randint(5, 20), 'failed': np.random.randint(3, 10)},
                    'scan_data': {'intensity': np.random.random() * 0.8 + 0.2},
                    'network_stats': {'connections_per_sec': np.random.random() * 50 + 30}
                }
                self.add_training_event(event, is_threat=True)
        
        print(f"[THREAT PREDICTOR] Generated {count} sample events")
        return len(self.training_data)

# Test function
def test_predictor():
    """Test the threat predictor"""
    print("=== Testing Threat Predictor ===\n")
    
    predictor = ThreatPredictor()
    
    # Generate sample data
    predictor.generate_sample_data(150)
    
    # Train model
    predictor.train_model()
    
    # Test predictions
    test_events = [
        {
            'name': 'Normal web traffic',
            'data': {
                'ports': [80, 443],
                'auth_attempts': {'ssh': 0, 'failed': 0},
                'scan_data': {'intensity': 0.1}
            }
        },
        {
            'name': 'Suspicious scan',
            'data': {
                'ports': list(range(20, 30)) + [4444, 8080],
                'auth_attempts': {'ssh': 8, 'failed': 3},
                'scan_data': {'intensity': 0.8}
            }
        },
        {
            'name': 'Brute force attempt',
            'data': {
                'ports': [22, 2222],
                'auth_attempts': {'ssh': 25, 'failed': 18},
                'scan_data': {'intensity': 0.4}
            }
        }
    ]
    
    print("\n=== Threat Predictions ===")
    for test in test_events:
        score, explanation = predictor.predict_threat(test['data'])
        print(f"\n{test['name']}:")
        print(f"  Score: {score:.2%}")
        print(f"  Assessment: {explanation}")
    
    # Save everything
    predictor.save_config()
    predictor.save_model()
    
    print(f"\n=== Test Complete ===")
    print(f"Model trained: {predictor.is_trained}")
    print(f"Training events: {len(predictor.training_data)}")
    
    return predictor

if __name__ == "__main__":
    test_predictor()
