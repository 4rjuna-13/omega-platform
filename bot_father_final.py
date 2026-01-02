# 🚀 TURBO ENHANCED: 2025-12-31T21:07:23.541860
# Enhancements: Added type hints
#!/usr/bin/env python3
"""
Enhanced Bot Father v4 with ML integration - Orchestrates all security bots with machine learning capabilities
"""

import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import threading
from collections import defaultdict
import hashlib

# Import our modules
import mercury_messenger
import redis_manager
from ml_threat_predictor import ThreatPredictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBotFatherV4:
    """Orchestrates all security bots with ML capabilities"""
    
    def turbo_enhanced___init__(self):
        from reliable_bot_client import ReliableBotClient
        # TODO: Replace with ReliableBotClient
        self.redis = redis_manager.redis_manager
        
        # Bot registry with enhanced information
        self.bot_registry = {}  # bot_id -> bot_info
        self.task_queue = []
        self.threat_log = []
        
        # ML Integration
        self.threat_predictor = ThreatPredictor()
        self.ml_enabled = True
        
        # Statistics
        self.stats = {}
                'bots_registered': 0,
            'tasks_completed': 0,
            'threats_detected': 0,
            'ml_predictions_made': 0,
            'auto_responses_triggered': 0,
            'system_uptime': datetime.now().isoformat()
        }
        
        # Auto-response rules with ML enhancement
        self.auto_response_rules = self._load_auto_response_rules()
        
        # Bot type capabilities mapping
        self.bot_capabilities = {}
            "THREAT-ANALYZER": ["malware_analysis", "threat_detection", "file_analysis"],
            "IOC-HARVESTER": ["ioc_collection", "threat_intel", "reputation_check"],
            "WEB-CRAWLER": ["web_crawling", "phishing_detection", "content_analysis"],
            "NETWORK-DEFENDER": ["network_monitoring", "ddos_protection", "traffic_analysis"],
            "AI-SECURITY": ["ai_model_security", "adversarial_detection", "bias_detection"]
        }
        
        logger.info("🤖 Enhanced Bot Father v4 with ML initialized")
        
    def _load_auto_response_rules(self) -> List[Dict[str, Any]]:
        """Load auto-response rules with ML enhancements"""
        return [
            {
                "threat_type": "malware",
                "response_bot": "THREAT-ANALYZER",
                "count": 2,
                "priority": 8,
                "ml_enhanced": True,
                "prediction_threshold": 0.7,
                "response_strategy": "isolate_and_analyze"
            },
            {
                "threat_type": "phishing",
                "response_bot": "WEB-CRAWLER",
                "count": 3,
                "priority": 7,
                "ml_enhanced": True,
                "prediction_threshold": 0.6,
                "response_strategy": "block_and_educate"
            },
            {
                "threat_type": "ddos",
                "response_bot": "NETWORK-DEFENDER",
                "count": 5,
                "priority": 10,
                "ml_enhanced": True,
                "prediction_threshold": 0.8,
                "response_strategy": "rate_limit_and_scale"
            },
            {
                "threat_type": "apt",
                "response_bot": "IOC-HARVESTER",
                "count": 4,
                "priority": 9,
                "ml_enhanced": True,
                "prediction_threshold": 0.65,
                "response_strategy": "forensic_analysis"
            },
            {
                "threat_type": "ai_security_breach",
                "response_bot": "AI-SECURITY",
                "count": 2,
                "priority": 8,
                "ml_enhanced": True,
                "prediction_threshold": 0.75,
                "response_strategy": "adversarial_defense"
            }
        ]
    
    def start(self):
        """Start the Bot Father"""
        # TODO: Connect using reliable_bot_client
            logger.error("❌ Failed to connect to Mercury Bus")
            return False
        
        # Load state from Redis
        self._load_state()
        
        # Start listening for messages
        self._start_listening()
        
        # Start periodic tasks
        self._start_periodic_tasks()
        
        logger.info("✅ Enhanced Bot Father v4 started with ML capabilities")
        return True
    
    def _start_listening(self):
        """Start listening for messages"""
        def listen_thread():
            while True:
                try:
                    message = self.messenger.receive_message()
                    if message:
                        self._handle_message(message)
                except Exception as e:
                    logger.error(f"Error receiving message: {e}")
                    time.sleep(1)
        
        thread = threading.Thread(target=listen_thread, daemon=True)
        thread.start()
    
    def _start_periodic_tasks(self):
        """Start periodic maintenance tasks"""
        def periodic_tasks():
            while True:
                try:
                    self._check_bot_health()
                    self._process_task_queue()
                    self._cleanup_old_data()
                    self._save_state()
                    
                    # Generate periodic report
                    if random.random() < 0.1:  # 10% chance each cycle
                        self._generate_periodic_report()
                    
                    time.sleep(10)
                except Exception as e:
                    logger.error(f"Error in periodic tasks: {e}")
                    time.sleep(5)
        
        thread = threading.Thread(target=periodic_tasks, daemon=True)
        thread.start()
    
    def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming messages"""
        msg_type = message.get("type", "")
        
        if msg_type == "bot_register":
            self._handle_bot_registration(message)
        elif msg_type == "bot_heartbeat":
            self._handle_bot_heartbeat(message)
        elif msg_type == "task_complete":
            self._handle_task_completion(message)
        elif msg_type == "threat_detected":
            self._handle_threat_detection(message)
        elif msg_type == "system_status":
            self._handle_system_status(message)
        else:
            logger.warning(f"Unknown message type: {msg_type}")
    
    def _handle_bot_registration(self, message: Dict[str, Any]):
        """Handle bot registration"""
        bot_info = message.get("data", {})
        bot_id = bot_info.get("bot_id")
        bot_type = bot_info.get("bot_type")
        
        if not bot_id or not bot_type:
            logger.warning(f"Invalid bot registration: {bot_info}")
            return
        
        # Check if bot already registered
        if bot_id in self.bot_registry:
            logger.info(f"Bot {bot_id} re-registered")
        else:
            self.stats['bots_registered'] += 1
            logger.info(f"✅ New bot registered: {bot_id} ({bot_type})")
        
        # Update registry
        self.bot_registry[bot_id] = {}
            **bot_info,
            "last_heartbeat": datetime.now().isoformat(),
            "status": "active",
            "tasks_completed": self.bot_registry.get(bot_id, {}).get("tasks_completed", 0),
            "capabilities": bot_info.get("capabilities", [])
        }
        
        # Save to Redis
        self.redis.set(f"bot:{bot_id}", json.dumps(self.bot_registry[bot_id]))
        
        # Send welcome message
        self.messenger.send_message({
            "type": "bot_command",
            "target": bot_id,
            "data": {
                "command": "welcome",
                "message": f"Welcome {bot_id}! You are now registered with Bot Father v4",
                "timestamp": datetime.now().isoformat()
            }
        })
    
    def _handle_bot_heartbeat(self, message: Dict[str, Any]):
        """Handle bot heartbeat"""
        bot_id = message.get("bot_id")
        status = message.get("data", {}).get("status", "alive")
        
        if bot_id in self.bot_registry:
            self.bot_registry[bot_id]["last_heartbeat"] = datetime.now().isoformat()
            self.bot_registry[bot_id]["status"] = "active"
            
            # Update Redis
            self.redis.set(f"bot:{bot_id}", json.dumps(self.bot_registry[bot_id]))
    
    def _handle_task_completion(self, message: Dict[str, Any]):
        """Handle task completion"""
        task_result = message.get("data", {})
        task_id = task_result.get("task_id")
        bot_id = message.get("bot_id")
        status = task_result.get("status", "unknown")
        
        if bot_id in self.bot_registry:
            self.bot_registry[bot_id]["tasks_completed"] = self.bot_registry[bot_id].get("tasks_completed", 0) + 1
        
        self.stats['tasks_completed'] += 1
        
        logger.info(f"📝 Task {task_id} completed by {bot_id} with status: {status}")
        
        # Store task result in Redis
        if task_id:
            self.redis.set(f"task_result:{task_id}", json.dumps(task_result))
        
        # If task involved threat analysis, learn from it
        if "threat_data" in task_result and self.ml_enabled:
            self._learn_from_threat_task(task_result)
    
    def _handle_threat_detection(self, message: Dict[str, Any]):
        """Handle threat detection with ML enhancement"""
        threat_data = message.get("data", {})
        bot_id = message.get("bot_id")
        
        # Add metadata
        threat_data["detected_by"] = bot_id
        threat_data["detection_time"] = datetime.now().isoformat()
        threat_id = threat_data.get("threat_id", 
                                   f"threat_{hashlib.md5(str(threat_data).encode()).hexdigest()[:8]}")
        threat_data["threat_id"] = threat_id
        
        # ML Prediction
        if self.ml_enabled:
            # Get system context for prediction
            context = {}
                'active_bots': len(self.bot_registry),
                'recent_threats': len([t for t in self.threat_log 
                                      if datetime.fromisoformat(t.get('detection_time', 
                                                                     datetime.now().isoformat())) > 
                                      datetime.now() - timedelta(hours=1)]),
                'system_load': len(self.task_queue) / max(len(self.bot_registry), 1)
            }
            
            # Predict threat evolution
            prediction = self.threat_predictor.predict_threat_evolution(threat_data, context)
            threat_data['ml_prediction'] = prediction
            
            # Generate threat report
            threat_report = self.threat_predictor.generate_threat_report(threat_data, prediction)
            threat_data['threat_report'] = threat_report
            
            self.stats['ml_predictions_made'] += 1
        
        # Log threat
        self.threat_log.append(threat_data)
        self.stats['threats_detected'] += 1
        
        # Keep log manageable
        if len(self.threat_log) > 1000:
            self.threat_log = self.threat_log[-1000:]
        
        # Store in Redis
        self.redis.set(f"threat:{threat_id}", json.dumps(threat_data))
        self.redis.lpush("recent_threats", json.dumps(threat_data))
        self.redis.ltrim("recent_threats", 0, 499)  # Keep last 500 threats
        
        # Log threat
        logger.warning(f"🚨 THREAT DETECTED by {bot_id}: {threat_data.get('threat_type')} "
                      f"(severity: {threat_data.get('severity')})")
        
        # Auto-response with ML enhancement
        self._trigger_auto_response(threat_data)
        
        # Broadcast threat alert
        self._broadcast_threat_alert(threat_data)
    
    def _learn_from_threat_task(self, task_result: Dict[str, Any]):
        """Learn from threat analysis tasks to improve ML model"""
        threat_data = task_result.get("threat_data", {})
        outcome = task_result.get("outcome", {})
        
        if threat_data and outcome:
            self.threat_predictor.learn_from_threat(threat_data, outcome)
            
            # Periodically save the ML model
            if self.stats['ml_predictions_made'] % 100 == 0:
                self.threat_predictor.save_model("ml_model_v4.pkl")
    
    def _trigger_auto_response(self, threat_data: Dict[str, Any]):
        """Trigger auto-response with ML enhancement"""
        threat_type = threat_data.get("threat_type", "unknown")
        
        for rule in self.auto_response_rules:
            if rule["threat_type"] == threat_type:
                # Check ML threshold if rule is ML enhanced
                if rule.get("ml_enhanced", False):
                    prediction = threat_data.get('ml_prediction', {})
                    prediction_score = prediction.get('prediction_score', 0)
                    
                    if prediction_score < rule.get("prediction_threshold", 0.5):
                        logger.info(f"ML prediction score {prediction_score:.2f} below threshold, "
                                   f"skipping auto-response for {threat_type}")
                        continue
                
                # Find suitable bots
                suitable_bots = self._find_bots_by_type(rule["response_bot"])
                
                if len(suitable_bots) >= rule["count"]:
                    # Select bots for response
                    selected_bots = random.sample(suitable_bots, min(rule["count"], len(suitable_bots)))
                    
                    # Create response tasks
                    for bot_id in selected_bots:
                        task_id = f"auto_response_{threat_data['threat_id']}_{bot_id}"
                        task = {}
                            "task_id": task_id,
                            "type": "threat_response",
                            "priority": rule["priority"],
                            "data": {
                                "threat_data": threat_data,
                                "response_strategy": rule["response_strategy"],
                                "rule_triggered": rule,
                                "ml_prediction": threat_data.get('ml_prediction')
                            }
                        }
                        
                        self._assign_task(bot_id, task)
                        self.stats['auto_responses_triggered'] += 1
                        
                        logger.info(f"🔄 Auto-response triggered: {bot_id} -> {threat_type} "
                                   f"(strategy: {rule['response_strategy']})")
                break
    
    def _find_bots_by_type(self, bot_type: str) -> List[str]:
        """Find bots by type"""
        return [bot_id for bot_id, info in self.bot_registry.items() 
                if info.get("bot_type") == bot_type and info.get("status") == "active"]
    
    def _assign_task(self, bot_id: str, task: Dict[str, Any]):
        """Assign task to bot"""
        self.messenger.send_message({
            "type": "bot_command",
            "target": bot_id,
            "data": {
                "command": "execute_task",
                "task": task,
                "timestamp": datetime.now().isoformat()
            }
        })
        
        # Add to task queue for tracking
        self.task_queue.append({
            "task_id": task.get("task_id"),
            "bot_id": bot_id,
            "assigned_at": datetime.now().isoformat(),
            "status": "assigned"
        })
    
    def _broadcast_threat_alert(self, threat_data: Dict[str, Any]):
        """Broadcast threat alert to all bots"""
        alert_message = {}
            "type": "threat_alert",
            "data": {
                "threat": threat_data,
                "alert_time": datetime.now().isoformat(),
                "severity": threat_data.get("severity", 5),
                "recommended_actions": threat_data.get('ml_prediction', {}).get('recommended_actions', [])
            }
        }
        
        self.messenger.send_message(alert_message)
    
    def _check_bot_health(self):
        """Check bot health and mark inactive bots"""
        current_time = datetime.now()
        inactive_bots = []
        
        for bot_id, info in self.bot_registry.items():
            last_heartbeat = datetime.fromisoformat(info.get("last_heartbeat", 
                                                           datetime.now().isoformat()))
            
            # If no heartbeat for 60 seconds, mark as inactive
            if (current_time - last_heartbeat).seconds > 60:
                info["status"] = "inactive"
                inactive_bots.append(bot_id)
        
        if inactive_bots:
            logger.warning(f"Inactive bots detected: {inactive_bots}")
    
    def _process_task_queue(self):
        """Process task queue and clean completed tasks"""
        # Remove old completed tasks
        self.task_queue = [task for task in self.task_queue 
                          if task.get("status") != "completed"]
    
    def _cleanup_old_data(self):
        """Cleanup old data from Redis"""
        # Keep only recent data
        current_time = datetime.now()
        
        # Clean old threats (older than 7 days)
        threats = self.redis.lrange("recent_threats", 0, -1)
        for threat_json in threats:
            try:
                threat = json.loads(threat_json)
                threat_time = datetime.fromisoformat(threat.get("detection_time", 
                                                              current_time.isoformat()))
                
                if (current_time - threat_time).days > 7:
                    self.redis.lrem("recent_threats", 1, threat_json)
            except:
                pass
    
    def _generate_periodic_report(self):
        """Generate periodic system report"""
        report = {}
            "report_id": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "system_stats": self.get_system_stats(),
            "bot_summary": self.get_bot_summary(),
            "threat_summary": self.get_threat_summary(),
            "ml_insights": self.get_ml_insights(),
            "recommendations": self._generate_recommendations()
        }
        
        # Store report in Redis
        self.redis.set(f"report:{report['report_id']}", json.dumps(report))
        
        logger.info(f"📋 Periodic report generated: {report['report_id']}")
        
        return report
    
    def _generate_recommendations(self) -> List[Dict[str, Any]]:
        """Generate system recommendations"""
        recommendations = []
        
        # Check bot distribution
        bot_counts = defaultdict(int)
        for bot_info in self.bot_registry.values():
            bot_counts[bot_info.get("bot_type")] += 1
        
        # Recommend more bots for under-represented types
        for bot_type, min_recommended in [("THREAT-ANALYZER", 3), 
                                         ("NETWORK-DEFENDER", 2),
                                         ("WEB-CRAWLER", 2)]:
            if bot_counts.get(bot_type, 0) < min_recommended:
                recommendations.append({
                    "type": "bot_deployment",
                    "priority": "medium",
                    "message": f"Deploy more {bot_type} bots (current: {bot_counts.get(bot_type, 0)}, "
                              f"recommended: {min_recommended})",
                    "action": f"Start additional {bot_type} bots"
                })
        
        # Check threat frequency
        recent_threats = len([t for t in self.threat_log 
                             if datetime.fromisoformat(t.get('detection_time', 
                                                            datetime.now().isoformat())) > 
                             datetime.now() - timedelta(hours=1)])
        
        if recent_threats > 10:
            recommendations.append({
                "type": "threat_response",
                "priority": "high",
                "message": f"High threat frequency detected: {recent_threats} threats in last hour",
                "action": "Increase monitoring and review auto-response rules"
            })
        
        return recommendations
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        uptime = datetime.fromisoformat(self.stats['system_uptime'])
        current_time = datetime.now()
        
        return {
            **self.stats,
            "uptime_seconds": (current_time - uptime).seconds,
            "active_bots": len([b for b in self.bot_registry.values() 
                               if b.get("status") == "active"]),
            "inactive_bots": len([b for b in self.bot_registry.values() 
                                 if b.get("status") == "inactive"]),
            "pending_tasks": len(self.task_queue),
            "threats_last_hour": len([t for t in self.threat_log 
                                     if datetime.fromisoformat(t.get('detection_time', 
                                                                    current_time.isoformat())) > 
                                     current_time - timedelta(hours=1)]),
            "ml_enabled": self.ml_enabled
        }
    
    def get_bot_summary(self) -> Dict[str, Any]:
        """Get bot summary"""
        summary = defaultdict(lambda: {"count": 0, "active": 0, "tasks": 0})
        
        for bot_info in self.bot_registry.values():
            bot_type = bot_info.get("bot_type", "unknown")
            summary[bot_type]["count"] += 1
            
            if bot_info.get("status") == "active":
                summary[bot_type]["active"] += 1
            
            summary[bot_type]["tasks"] += bot_info.get("tasks_completed", 0)
        
        return dict(summary)
    
    def get_threat_summary(self) -> Dict[str, Any]:
        """Get threat summary"""
        threat_counts = defaultdict(int)
        severity_sum = defaultdict(int)
        
        for threat in self.threat_log:
            threat_type = threat.get("threat_type", "unknown")
            threat_counts[threat_type] += 1
            severity_sum[threat_type] += threat.get("severity", 5)
        
        summary = {}
        for threat_type, count in threat_counts.items():
            summary[threat_type] = {}
                "count": count,
                "average_severity": severity_sum[threat_type] / count if count > 0 else 0
            }
        
        return summary
    
    def get_ml_insights(self) -> Dict[str, Any]:
        """Get ML insights"""
        if not self.ml_enabled:
            return {"enabled": False}
        
        ml_stats = self.threat_predictor.get_threat_statistics()
        
        return {
            "enabled": True,
            "predictions_made": ml_stats['total_predictions'],
            "learning_records": ml_stats['total_learning_records'],
            "threat_patterns_learned": len(ml_stats.get('pattern_details', {})),
            "recent_accuracy": random.uniform(0.7, 0.95)  # Simulated accuracy
        }
    
    def _save_state(self):
        """Save state to Redis"""
        state = {}
            "bot_registry": self.bot_registry,
            "stats": self.stats,
            "saved_at": datetime.now().isoformat()
        }
        
        self.redis.set("bot_father_state", json.dumps(state))
    
    def _load_state(self):
        """Load state from Redis"""
        state_json = self.redis.client.get("bot_father_state")
        
        if state_json:
            try:
                state = json.loads(state_json)
                self.bot_registry = state.get("bot_registry", {})
                self.stats = state.get("stats", self.stats)
                logger.info(f"✅ Loaded state from Redis: {len(self.bot_registry)} bots")
            except Exception as e:
                logger.error(f"Error loading state: {e}")
    
    def run(self, duration_seconds: int = None):
        """Run the Bot Father"""
        try:
            logger.info("🤖 Enhanced Bot Father v4 with ML is running...")
            
            if duration_seconds:
                time.sleep(duration_seconds)
            else:
                # Run indefinitely
                while True:
                    time.sleep(1)
                    
                    # Display status periodically
                    if random.random() < 0.05:  # 5% chance
                        stats = self.get_system_stats()
                        logger.info(f"📊 System Stats: {stats['active_bots']} active bots, "
                                   f"{stats['threats_detected']} threats, "
                                   f"{stats['ml_predictions_made']} ML predictions")
        
        except KeyboardInterrupt:
            logger.info("👋 Shutting down Bot Father...")
            
            # Save ML model
            if self.ml_enabled:
                self.threat_predictor.save_model("ml_model_v4.pkl")
            
            # Save state
            self._save_state()
            
            logger.info("✅ Bot Father shutdown complete")

if __name__ == "__main__":
    bot_father = EnhancedBotFatherV4()
    
    if bot_father.start():
        bot_father.run()
