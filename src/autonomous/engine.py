#!/usr/bin/env python3
"""
🤖 Autonomous Decision Engine
"""

import json
import sqlite3
import hashlib
import yaml
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

class ThreatLevel(Enum):
    NORMAL = 0
    SUSPICIOUS = 1
    MALICIOUS = 2
    CRITICAL = 3

class ActionType(Enum):
    DEPLOY_BOTS = "deploy_bots"
    ACTIVATE_HONEYPOT = "activate_honeypot"
    ESCALATE_INTEL = "escalate_intelligence"
    GATHER_INTEL = "gather_intelligence"

@dataclass
class ThreatIndicator:
    id: str
    source: str
    indicator: str
    threat_type: str
    confidence: float
    severity: ThreatLevel
    timestamp: str
    context: dict
    
    def __post_init__(self):
        if not self.id:
            indicator_hash = hashlib.sha256(
                f"{self.source}:{self.indicator}:{self.timestamp}".encode()
            ).hexdigest()[:16]
            self.id = f"threat_{indicator_hash}"

@dataclass
class Decision:
    decision_id: str
    action: ActionType
    reason: str
    confidence: float
    priority: int
    parameters: dict
    expected_outcome: str
    timestamp: str

class AutonomousEngine:
    """Core autonomous decision engine"""
    
    def __init__(self, config_path="config/autonomous.yaml", db_path="data/sovereign.db"):
        self.config = self.load_config(config_path)
        self.db_path = db_path
    
    def load_config(self, config_path):
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return {}
    
    def analyze_threat(self, threat: ThreatIndicator) -> dict:
        """Analyze threat and return assessment"""
        try:
            # Calculate threat score
            base_score = threat.severity.value * 25
            confidence_adjustment = threat.confidence * 20 * 1.2
            
            # Adjust for recency
            recency_factor = self._calculate_recency_factor(threat.timestamp)
            
            threat_score = base_score + confidence_adjustment + recency_factor
            
            # Determine response level
            if threat_score >= 80:
                response_level = "critical"
            elif threat_score >= 60:
                response_level = "high"
            elif threat_score >= 40:
                response_level = "medium"
            elif threat_score >= 20:
                response_level = "low"
            else:
                response_level = "normal"
            
            return {
                "threat_score": min(threat_score, 100),
                "response_level": response_level,
                "confidence": threat.confidence,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error analyzing threat: {e}")
            return {
                "threat_score": 0,
                "response_level": "normal",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _calculate_recency_factor(self, timestamp: str) -> float:
        """Calculate recency factor for threat"""
        try:
            threat_time = datetime.fromisoformat(timestamp)
            now = datetime.now()
            hours_diff = (now - threat_time).total_seconds() / 3600
            
            # Exponential decay over 24 hours
            recency_factor = 10 * (2 ** (-hours_diff / 12))
            return min(recency_factor, 10)
        except:
            return 5.0
    
    def make_decision(self, threat: ThreatIndicator) -> list:
        """Make autonomous decisions for a threat"""
        try:
            # Analyze threat
            analysis = self.analyze_threat(threat)
            
            # Generate decisions
            decisions = []
            
            # Primary decision
            primary_action = self._determine_primary_action(threat, analysis)
            decisions.append(self._create_decision(
                action=primary_action,
                threat=threat,
                analysis=analysis,
                priority=1
            ))
            
            # Intelligence gathering decision
            decisions.append(self._create_decision(
                action=ActionType.GATHER_INTEL,
                threat=threat,
                analysis=analysis,
                priority=2
            ))
            
            print(f"Generated {len(decisions)} decisions for threat {threat.id}")
            return decisions
            
        except Exception as e:
            print(f"Error making decisions: {e}")
            return []
    
    def _determine_primary_action(self, threat: ThreatIndicator, analysis: dict) -> ActionType:
        """Determine primary action"""
        response_level = analysis["response_level"]
        
        if response_level in ["critical", "high"]:
            return ActionType.DEPLOY_BOTS
        elif response_level == "medium":
            return ActionType.ACTIVATE_HONEYPOT
        else:
            return ActionType.GATHER_INTEL
    
    def _create_decision(self, action: ActionType, threat: ThreatIndicator, 
                        analysis: dict, priority: int) -> Decision:
        """Create a structured decision object"""
        # Generate decision ID
        decision_hash = hashlib.sha256(
            f"{action.value}:{threat.id}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        decision_id = f"dec_{decision_hash}"
        
        # Get parameters
        parameters = self._get_action_parameters(action, analysis["response_level"])
        
        # Generate reason
        reason = self._generate_reason(action, threat, analysis)
        
        # Calculate confidence
        confidence = min(analysis["confidence"] * 1.2, 0.95)
        
        # Expected outcome
        expected_outcome = self._get_expected_outcome(action)
        
        return Decision(
            decision_id=decision_id,
            action=action,
            reason=reason,
            confidence=confidence,
            priority=priority,
            parameters=parameters,
            expected_outcome=expected_outcome,
            timestamp=datetime.now().isoformat()
        )
    
    def _get_action_parameters(self, action: ActionType, response_level: str) -> dict:
        """Get parameters for action"""
        if action == ActionType.DEPLOY_BOTS:
            return {
                "bot_count": 5,
                "bot_type": "defender",
                "deployment_strategy": "adaptive"
            }
        elif action == ActionType.ACTIVATE_HONEYPOT:
            return {
                "honeypot_level": "interactive",
                "deception_type": "dynamic"
            }
        else:
            return {"intensity": response_level}
    
    def _generate_reason(self, action: ActionType, threat: ThreatIndicator, 
                        analysis: dict) -> str:
        """Generate human-readable reason for decision"""
        reasons = {
            ActionType.DEPLOY_BOTS: 
                f"Deploying bots against {threat.threat_type} threat",
            ActionType.ACTIVATE_HONEYPOT: 
                f"Activating deception against {threat.threat_type}",
            ActionType.GATHER_INTEL:
                f"Gathering intelligence on {threat.threat_type}"
        }
        return reasons.get(action, "Security measure")
    
    def _get_expected_outcome(self, action: ActionType) -> str:
        """Get expected outcome for action"""
        outcomes = {
            ActionType.DEPLOY_BOTS: "Neutralize threat",
            ActionType.ACTIVATE_HONEYPOT: "Gather intelligence",
            ActionType.GATHER_INTEL: "Expand knowledge"
        }
        return outcomes.get(action, "Improve security")

def test_engine():
    """Test the autonomous engine"""
    print("Testing Autonomous Engine...")
    
    engine = AutonomousEngine()
    
    # Create test threat
    test_threat = ThreatIndicator(
        id="test_threat_001",
        source="test",
        indicator="test_malware",
        threat_type="malware",
        confidence=0.85,
        severity=ThreatLevel.CRITICAL,
        timestamp=datetime.now().isoformat(),
        context={"test": True}
    )
    
    # Make decisions
    decisions = engine.make_decision(test_threat)
    
    print(f"Generated {len(decisions)} decisions:")
    for decision in decisions:
        print(f"  • {decision.action.value} (confidence: {decision.confidence:.2%})")
    
    return decisions

if __name__ == "__main__":
    test_engine()
