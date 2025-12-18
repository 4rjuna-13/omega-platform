#!/usr/bin/env python3
"""
OMEGA Purple Team Component
Combined red/blue team simulation and exercises
"""

import json
import time
import uuid
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional
import threading
import queue
from collections import defaultdict

class TeamRole(Enum):
    """Purple team roles"""
    RED_TEAM = "red_team"      # Attack simulation
    BLUE_TEAM = "blue_team"    # Defense and detection
    PURPLE_TEAM = "purple_team" # Combined operations
    OBSERVER = "observer"      # Monitoring and analysis

class ExercisePhase(Enum):
    """Purple team exercise phases"""
    PLANNING = "planning"
    RECONNAISSANCE = "reconnaissance"
    EXPLOITATION = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    DEFENSE = "defense"
    DETECTION = "detection"
    RESPONSE = "response"
    RECOVERY = "recovery"
    DEBRIEF = "debrief"

class Technique(Enum):
    """Attack and defense techniques"""
    # Red Team Techniques
    PHISHING = "T1566"
    EXPLOIT_PUBLIC_APP = "T1190"
    EXTERNAL_REMOTE_SERVICES = "T1133"
    VALID_ACCOUNTS = "T1078"
    COMMAND_AND_SCRIPTING = "T1059"
    LATERAL_MOVEMENT = "T1021"
    DATA_EXFILTRATION = "TA0010"
    
    # Blue Team Techniques
    LOGGING = "T1562.001"
    DETECTION_RULES = "T1562.006"
    ENDPOINT_PROTECTION = "T1548"
    NETWORK_SEGMENTATION = "T1560"
    THREAT_HUNTING = "T1595"
    INCIDENT_RESPONSE = "T1590"

class Exercise:
    """Purple team exercise"""
    
    def __init__(self, exercise_id: str, name: str, scenario: str):
        self.exercise_id = exercise_id
        self.name = name
        self.scenario = scenario
        self.created = datetime.now()
        self.status = "planned"
        self.phases = {}
        self.teams = {
            TeamRole.RED_TEAM: {"members": [], "actions": []},
            TeamRole.BLUE_TEAM: {"members": [], "actions": []},
            TeamRole.PURPLE_TEAM: {"members": [], "actions": []}
        }
        self.findings = []
        self.metrics = defaultdict(int)
        self.events = queue.Queue()
        
        # Initialize phases
        self._initialize_phases()
    
    def _initialize_phases(self):
        """Initialize exercise phases"""
        for phase in ExercisePhase:
            self.phases[phase.value] = {
                "status": "pending",
                "start_time": None,
                "end_time": None,
                "duration": None,
                "activities": []
            }
    
    def add_team_member(self, member_name: str, role: TeamRole, expertise: List[str]) -> Dict:
        """Add team member to exercise"""
        member = {
            "member_id": f"MEMBER-{str(uuid.uuid4())[:8]}",
            "name": member_name,
            "role": role.value,
            "expertise": expertise,
            "joined": datetime.now().isoformat(),
            "actions_taken": 0,
            "findings_reported": 0
        }
        
        self.teams[role]["members"].append(member)
        self._log_event("team_member_added", {
            "member": member_name,
            "role": role.value,
            "expertise": expertise
        })
        
        return member
    
    def start_phase(self, phase: ExercisePhase) -> bool:
        """Start an exercise phase"""
        if self.phases[phase.value]["status"] != "pending":
            return False
        
        self.phases[phase.value]["status"] = "active"
        self.phases[phase.value]["start_time"] = datetime.now().isoformat()
        
        self._log_event("phase_started", {
            "phase": phase.value,
            "exercise": self.name
        })
        
        return True
    
    def complete_phase(self, phase: ExercisePhase) -> bool:
        """Complete an exercise phase"""
        if self.phases[phase.value]["status"] != "active":
            return False
        
        self.phases[phase.value]["status"] = "completed"
        self.phases[phase.value]["end_time"] = datetime.now().isoformat()
        
        # Calculate duration
        start_time = datetime.fromisoformat(self.phases[phase.value]["start_time"])
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.phases[phase.value]["duration"] = duration
        
        self._log_event("phase_completed", {
            "phase": phase.value,
            "duration": duration
        })
        
        return True
    
    def record_red_team_action(self, action_name: str, technique: Technique, 
                              target: str, success: bool, details: str = "") -> Dict:
        """Record red team action"""
        action = {
            "action_id": f"RED-{str(uuid.uuid4())[:8]}",
            "name": action_name,
            "technique": technique.value,
            "technique_name": technique.name,
            "target": target,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        self.teams[TeamRole.RED_TEAM]["actions"].append(action)
        self.metrics["red_team_actions"] += 1
        
        if success:
            self.metrics["successful_attacks"] += 1
            event_type = "attack_successful"
        else:
            self.metrics["failed_attacks"] += 1
            event_type = "attack_failed"
        
        self._log_event(event_type, {
            "action": action_name,
            "technique": technique.name,
            "target": target,
            "success": success
        })
        
        return action
    
    def record_blue_team_action(self, action_name: str, technique: Technique,
                               detection: bool, response: bool, details: str = "") -> Dict:
        """Record blue team action"""
        action = {
            "action_id": f"BLUE-{str(uuid.uuid4())[:8]}",
            "name": action_name,
            "technique": technique.value,
            "technique_name": technique.name,
            "detection": detection,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        self.teams[TeamRole.BLUE_TEAM]["actions"].append(action)
        self.metrics["blue_team_actions"] += 1
        
        if detection:
            self.metrics["detections"] += 1
        
        if response:
            self.metrics["responses"] += 1
        
        event_data = {
            "action": action_name,
            "technique": technique.name,
            "detection": detection,
            "response": response
        }
        
        self._log_event("defense_action", event_data)
        
        return action
    
    def add_finding(self, finding_type: str, severity: str, 
                   description: str, recommended_action: str) -> Dict:
        """Add finding from exercise"""
        finding = {
            "finding_id": f"FIND-{str(uuid.uuid4())[:8]}",
            "type": finding_type,
            "severity": severity,
            "description": description,
            "recommended_action": recommended_action,
            "reported_by": self._get_active_member(),
            "timestamp": datetime.now().isoformat(),
            "status": "open"
        }
        
        self.findings.append(finding)
        self.metrics["findings"] += 1
        
        if severity in ["high", "critical"]:
            self.metrics["critical_findings"] += 1
        
        self._log_event("finding_added", {
            "type": finding_type,
            "severity": severity,
            "description": description[:50] + "..." if len(description) > 50 else description
        })
        
        return finding
    
    def _get_active_member(self) -> str:
        """Get random active member for attribution"""
        all_members = []
        for team in self.teams.values():
            all_members.extend(team["members"])
        
        if all_members:
            return random.choice(all_members)["name"]
        return "System"
    
    def _log_event(self, event_type: str, data: Dict) -> None:
        """Log exercise event"""
        event = {
            "event_id": f"EVENT-{str(uuid.uuid4())[:8]}",
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "exercise_phase": self._get_current_phase()
        }
        
        self.events.put(event)
    
    def _get_current_phase(self) -> str:
        """Get current active phase"""
        for phase, data in self.phases.items():
            if data["status"] == "active":
                return phase
        return "planning"
    
    def generate_metrics(self) -> Dict:
        """Generate exercise metrics"""
        # Calculate detection rate
        total_attacks = self.metrics.get("successful_attacks", 0) + self.metrics.get("failed_attacks", 0)
        detection_rate = 0
        if total_attacks > 0:
            detection_rate = (self.metrics.get("detections", 0) / total_attacks) * 100
        
        # Calculate response effectiveness
        response_rate = 0
        if self.metrics.get("detections", 0) > 0:
            response_rate = (self.metrics.get("responses", 0) / self.metrics.get("detections", 0)) * 100
        
        # Time metrics
        completed_phases = [p for p in self.phases.values() if p["status"] == "completed"]
        total_duration = sum(p["duration"] or 0 for p in completed_phases)
        
        return {
            "exercise_duration_seconds": total_duration,
            "team_metrics": {
                "red_team_actions": self.metrics.get("red_team_actions", 0),
                "blue_team_actions": self.metrics.get("blue_team_actions", 0),
                "successful_attacks": self.metrics.get("successful_attacks", 0),
                "failed_attacks": self.metrics.get("failed_attacks", 0)
            },
            "defense_metrics": {
                "detections": self.metrics.get("detections", 0),
                "detection_rate_percent": round(detection_rate, 2),
                "responses": self.metrics.get("responses", 0),
                "response_rate_percent": round(response_rate, 2)
            },
            "findings_metrics": {
                "total_findings": self.metrics.get("findings", 0),
                "critical_findings": self.metrics.get("critical_findings", 0),
                "findings_by_severity": self._count_findings_by_severity()
            },
            "team_members": sum(len(team["members"]) for team in self.teams.values())
        }
    
    def _count_findings_by_severity(self) -> Dict:
        """Count findings by severity"""
        severity_counts = defaultdict(int)
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1
        return dict(severity_counts)
    
    def generate_report(self) -> Dict:
        """Generate comprehensive exercise report"""
        metrics = self.generate_metrics()
        
        # Get recent events
        recent_events = []
        while not self.events.empty() and len(recent_events) < 10:
            recent_events.append(self.events.get())
        
        return {
            "exercise_id": self.exercise_id,
            "name": self.name,
            "scenario": self.scenario,
            "status": self.status,
            "created": self.created.isoformat(),
            "duration_hours": round(metrics["exercise_duration_seconds"] / 3600, 2),
            "phases": self.phases,
            "metrics": metrics,
            "findings": self.findings[:10],  # Top 10 findings
            "recent_events": recent_events,
            "recommendations": self._generate_recommendations(metrics),
            "lessons_learned": self._generate_lessons_learned()
        }
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        # Detection rate recommendations
        if metrics["defense_metrics"]["detection_rate_percent"] < 50:
            recommendations.append("Improve detection capabilities - current rate is below 50%")
        
        # Response rate recommendations
        if metrics["defense_metrics"]["response_rate_percent"] < 70:
            recommendations.append("Enhance response procedures - response rate needs improvement")
        
        # Critical findings recommendations
        if metrics["findings_metrics"]["critical_findings"] > 0:
            recommendations.append(f"Immediately address {metrics['findings_metrics']['critical_findings']} critical findings")
        
        # Always include these
        recommendations.extend([
            "Conduct regular purple team exercises",
            "Update incident response playbooks",
            "Enhance security awareness training",
            "Implement continuous security monitoring"
        ])
        
        return recommendations
    
    def _generate_lessons_learned(self) -> List[str]:
        """Generate lessons learned from exercise"""
        lessons = []
        
        # Analyze team actions
        red_success_rate = 0
        if self.metrics.get("red_team_actions", 0) > 0:
            red_success_rate = (self.metrics.get("successful_attacks", 0) / self.metrics.get("red_team_actions", 0)) * 100
        
        if red_success_rate > 70:
            lessons.append("Red team demonstrated high effectiveness - defensive measures need strengthening")
        else:
            lessons.append("Blue team defenses were effective against most attacks")
        
        # Add lessons based on findings
        if self.findings:
            critical_findings = [f for f in self.findings if f["severity"] in ["high", "critical"]]
            if critical_findings:
                lessons.append(f"Identified {len(critical_findings)} critical areas needing immediate attention")
        
        # Team collaboration lessons
        purple_members = len(self.teams[TeamRole.PURPLE_TEAM]["members"])
        if purple_members > 0:
            lessons.append("Purple team collaboration improved exercise outcomes")
        else:
            lessons.append("Consider adding dedicated purple team members for better collaboration")
        
        return lessons

class PurpleTeamManager:
    """OMEGA Purple Team Manager"""
    
    def __init__(self):
        self.name = "OMEGA Purple Team"
        self.version = "1.0.0"
        self.exercises = {}
        self.scenarios = self._load_scenarios()
        self.active_exercises = set()
    
    def _load_scenarios(self) -> Dict:
        """Load exercise scenarios"""
        return {
            "phishing_campaign": {
                "name": "Phishing Campaign Response",
                "description": "Simulate and respond to sophisticated phishing campaign",
                "duration_hours": 4,
                "objectives": [
                    "Test email security controls",
                    "Validate user awareness training",
                    "Exercise incident response procedures",
                    "Test threat hunting capabilities"
                ]
            },
            "ransomware_attack": {
                "name": "Ransomware Attack Simulation",
                "description": "Simulate ransomware attack and recovery procedures",
                "duration_hours": 6,
                "objectives": [
                    "Test endpoint protection effectiveness",
                    "Validate backup and recovery procedures",
                    "Exercise crisis communications",
                    "Test legal and compliance response"
                ]
            },
            "supply_chain_compromise": {
                "
cat > omega_purple_team.py << 'EOF'
#!/usr/bin/env python3
"""
OMEGA Purple Team Component
Combined red/blue team simulation and exercises
"""

import json
import time
import uuid
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional
import threading
import queue
from collections import defaultdict

class TeamRole(Enum):
    """Purple team roles"""
    RED_TEAM = "red_team"      # Attack simulation
    BLUE_TEAM = "blue_team"    # Defense and detection
    PURPLE_TEAM = "purple_team" # Combined operations
    OBSERVER = "observer"      # Monitoring and analysis

class ExercisePhase(Enum):
    """Purple team exercise phases"""
    PLANNING = "planning"
    RECONNAISSANCE = "reconnaissance"
    EXPLOITATION = "exploitation"
    POST_EXPLOITATION = "post_exploitation"
    DEFENSE = "defense"
    DETECTION = "detection"
    RESPONSE = "response"
    RECOVERY = "recovery"
    DEBRIEF = "debrief"

class Technique(Enum):
    """Attack and defense techniques"""
    # Red Team Techniques
    PHISHING = "T1566"
    EXPLOIT_PUBLIC_APP = "T1190"
    EXTERNAL_REMOTE_SERVICES = "T1133"
    VALID_ACCOUNTS = "T1078"
    COMMAND_AND_SCRIPTING = "T1059"
    LATERAL_MOVEMENT = "T1021"
    DATA_EXFILTRATION = "TA0010"
    
    # Blue Team Techniques
    LOGGING = "T1562.001"
    DETECTION_RULES = "T1562.006"
    ENDPOINT_PROTECTION = "T1548"
    NETWORK_SEGMENTATION = "T1560"
    THREAT_HUNTING = "T1595"
    INCIDENT_RESPONSE = "T1590"

class Exercise:
    """Purple team exercise"""
    
    def __init__(self, exercise_id: str, name: str, scenario: str):
        self.exercise_id = exercise_id
        self.name = name
        self.scenario = scenario
        self.created = datetime.now()
        self.status = "planned"
        self.phases = {}
        self.teams = {
            TeamRole.RED_TEAM: {"members": [], "actions": []},
            TeamRole.BLUE_TEAM: {"members": [], "actions": []},
            TeamRole.PURPLE_TEAM: {"members": [], "actions": []}
        }
        self.findings = []
        self.metrics = defaultdict(int)
        self.events = queue.Queue()
        
        # Initialize phases
        self._initialize_phases()
    
    def _initialize_phases(self):
        """Initialize exercise phases"""
        for phase in ExercisePhase:
            self.phases[phase.value] = {
                "status": "pending",
                "start_time": None,
                "end_time": None,
                "duration": None,
                "activities": []
            }
    
    def add_team_member(self, member_name: str, role: TeamRole, expertise: List[str]) -> Dict:
        """Add team member to exercise"""
        member = {
            "member_id": f"MEMBER-{str(uuid.uuid4())[:8]}",
            "name": member_name,
            "role": role.value,
            "expertise": expertise,
            "joined": datetime.now().isoformat(),
            "actions_taken": 0,
            "findings_reported": 0
        }
        
        self.teams[role]["members"].append(member)
        self._log_event("team_member_added", {
            "member": member_name,
            "role": role.value,
            "expertise": expertise
        })
        
        return member
    
    def start_phase(self, phase: ExercisePhase) -> bool:
        """Start an exercise phase"""
        if self.phases[phase.value]["status"] != "pending":
            return False
        
        self.phases[phase.value]["status"] = "active"
        self.phases[phase.value]["start_time"] = datetime.now().isoformat()
        
        self._log_event("phase_started", {
            "phase": phase.value,
            "exercise": self.name
        })
        
        return True
    
    def complete_phase(self, phase: ExercisePhase) -> bool:
        """Complete an exercise phase"""
        if self.phases[phase.value]["status"] != "active":
            return False
        
        self.phases[phase.value]["status"] = "completed"
        self.phases[phase.value]["end_time"] = datetime.now().isoformat()
        
        # Calculate duration
        start_time = datetime.fromisoformat(self.phases[phase.value]["start_time"])
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.phases[phase.value]["duration"] = duration
        
        self._log_event("phase_completed", {
            "phase": phase.value,
            "duration": duration
        })
        
        return True
    
    def record_red_team_action(self, action_name: str, technique: Technique, 
                              target: str, success: bool, details: str = "") -> Dict:
        """Record red team action"""
        action = {
            "action_id": f"RED-{str(uuid.uuid4())[:8]}",
            "name": action_name,
            "technique": technique.value,
            "technique_name": technique.name,
            "target": target,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        self.teams[TeamRole.RED_TEAM]["actions"].append(action)
        self.metrics["red_team_actions"] += 1
        
        if success:
            self.metrics["successful_attacks"] += 1
            event_type = "attack_successful"
        else:
            self.metrics["failed_attacks"] += 1
            event_type = "attack_failed"
        
        self._log_event(event_type, {
            "action": action_name,
            "technique": technique.name,
            "target": target,
            "success": success
        })
        
        return action
    
    def record_blue_team_action(self, action_name: str, technique: Technique,
                               detection: bool, response: bool, details: str = "") -> Dict:
        """Record blue team action"""
        action = {
            "action_id": f"BLUE-{str(uuid.uuid4())[:8]}",
            "name": action_name,
            "technique": technique.value,
            "technique_name": technique.name,
            "detection": detection,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        self.teams[TeamRole.BLUE_TEAM]["actions"].append(action)
        self.metrics["blue_team_actions"] += 1
        
        if detection:
            self.metrics["detections"] += 1
        
        if response:
            self.metrics["responses"] += 1
        
        event_data = {
            "action": action_name,
            "technique": technique.name,
            "detection": detection,
            "response": response
        }
        
        self._log_event("defense_action", event_data)
        
        return action
    
    def add_finding(self, finding_type: str, severity: str, 
                   description: str, recommended_action: str) -> Dict:
        """Add finding from exercise"""
        finding = {
            "finding_id": f"FIND-{str(uuid.uuid4())[:8]}",
            "type": finding_type,
            "severity": severity,
            "description": description,
            "recommended_action": recommended_action,
            "reported_by": self._get_active_member(),
            "timestamp": datetime.now().isoformat(),
            "status": "open"
        }
        
        self.findings.append(finding)
        self.metrics["findings"] += 1
        
        if severity in ["high", "critical"]:
            self.metrics["critical_findings"] += 1
        
        self._log_event("finding_added", {
            "type": finding_type,
            "severity": severity,
            "description": description[:50] + "..." if len(description) > 50 else description
        })
        
        return finding
    
    def _get_active_member(self) -> str:
        """Get random active member for attribution"""
        all_members = []
        for team in self.teams.values():
            all_members.extend(team["members"])
        
        if all_members:
            return random.choice(all_members)["name"]
        return "System"
    
    def _log_event(self, event_type: str, data: Dict) -> None:
        """Log exercise event"""
        event = {
            "event_id": f"EVENT-{str(uuid.uuid4())[:8]}",
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "exercise_phase": self._get_current_phase()
        }
        
        self.events.put(event)
    
    def _get_current_phase(self) -> str:
        """Get current active phase"""
        for phase, data in self.phases.items():
            if data["status"] == "active":
                return phase
        return "planning"
    
    def generate_metrics(self) -> Dict:
        """Generate exercise metrics"""
        # Calculate detection rate
        total_attacks = self.metrics.get("successful_attacks", 0) + self.metrics.get("failed_attacks", 0)
        detection_rate = 0
        if total_attacks > 0:
            detection_rate = (self.metrics.get("detections", 0) / total_attacks) * 100
        
        # Calculate response effectiveness
        response_rate = 0
        if self.metrics.get("detections", 0) > 0:
            response_rate = (self.metrics.get("responses", 0) / self.metrics.get("detections", 0)) * 100
        
        # Time metrics
        completed_phases = [p for p in self.phases.values() if p["status"] == "completed"]
        total_duration = sum(p["duration"] or 0 for p in completed_phases)
        
        return {
            "exercise_duration_seconds": total_duration,
            "team_metrics": {
                "red_team_actions": self.metrics.get("red_team_actions", 0),
                "blue_team_actions": self.metrics.get("blue_team_actions", 0),
                "successful_attacks": self.metrics.get("successful_attacks", 0),
                "failed_attacks": self.metrics.get("failed_attacks", 0)
            },
            "defense_metrics": {
                "detections": self.metrics.get("detections", 0),
                "detection_rate_percent": round(detection_rate, 2),
                "responses": self.metrics.get("responses", 0),
                "response_rate_percent": round(response_rate, 2)
            },
            "findings_metrics": {
                "total_findings": self.metrics.get("findings", 0),
                "critical_findings": self.metrics.get("critical_findings", 0),
                "findings_by_severity": self._count_findings_by_severity()
            },
            "team_members": sum(len(team["members"]) for team in self.teams.values())
        }
    
    def _count_findings_by_severity(self) -> Dict:
        """Count findings by severity"""
        severity_counts = defaultdict(int)
        for finding in self.findings:
            severity_counts[finding["severity"]] += 1
        return dict(severity_counts)
    
    def generate_report(self) -> Dict:
        """Generate comprehensive exercise report"""
        metrics = self.generate_metrics()
        
        # Get recent events
        recent_events = []
        while not self.events.empty() and len(recent_events) < 10:
            recent_events.append(self.events.get())
        
        return {
            "exercise_id": self.exercise_id,
            "name": self.name,
            "scenario": self.scenario,
            "status": self.status,
            "created": self.created.isoformat(),
            "duration_hours": round(metrics["exercise_duration_seconds"] / 3600, 2),
            "phases": self.phases,
            "metrics": metrics,
            "findings": self.findings[:10],  # Top 10 findings
            "recent_events": recent_events,
            "recommendations": self._generate_recommendations(metrics),
            "lessons_learned": self._generate_lessons_learned()
        }
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        # Detection rate recommendations
        if metrics["defense_metrics"]["detection_rate_percent"] < 50:
            recommendations.append("Improve detection capabilities - current rate is below 50%")
        
        # Response rate recommendations
        if metrics["defense_metrics"]["response_rate_percent"] < 70:
            recommendations.append("Enhance response procedures - response rate needs improvement")
        
        # Critical findings recommendations
        if metrics["findings_metrics"]["critical_findings"] > 0:
            recommendations.append(f"Immediately address {metrics['findings_metrics']['critical_findings']} critical findings")
        
        # Always include these
        recommendations.extend([
            "Conduct regular purple team exercises",
            "Update incident response playbooks",
            "Enhance security awareness training",
            "Implement continuous security monitoring"
        ])
        
        return recommendations
    
    def _generate_lessons_learned(self) -> List[str]:
        """Generate lessons learned from exercise"""
        lessons = []
        
        # Analyze team actions
        red_success_rate = 0
        if self.metrics.get("red_team_actions", 0) > 0:
            red_success_rate = (self.metrics.get("successful_attacks", 0) / self.metrics.get("red_team_actions", 0)) * 100
        
        if red_success_rate > 70:
            lessons.append("Red team demonstrated high effectiveness - defensive measures need strengthening")
        else:
            lessons.append("Blue team defenses were effective against most attacks")
        
        # Add lessons based on findings
        if self.findings:
            critical_findings = [f for f in self.findings if f["severity"] in ["high", "critical"]]
            if critical_findings:
                lessons.append(f"Identified {len(critical_findings)} critical areas needing immediate attention")
        
        # Team collaboration lessons
        purple_members = len(self.teams[TeamRole.PURPLE_TEAM]["members"])
        if purple_members > 0:
            lessons.append("Purple team collaboration improved exercise outcomes")
        else:
            lessons.append("Consider adding dedicated purple team members for better collaboration")
        
        return lessons

class PurpleTeamManager:
    """OMEGA Purple Team Manager"""
    
    def __init__(self):
        self.name = "OMEGA Purple Team"
        self.version = "1.0.0"
        self.exercises = {}
        self.scenarios = self._load_scenarios()
        self.active_exercises = set()
    
    def _load_scenarios(self) -> Dict:
        """Load exercise scenarios"""
        return {
            "phishing_campaign": {
                "name": "Phishing Campaign Response",
                "description": "Simulate and respond to sophisticated phishing campaign",
                "duration_hours": 4,
                "objectives": [
                    "Test email security controls",
                    "Validate user awareness training",
                    "Exercise incident response procedures",
                    "Test threat hunting capabilities"
                ]
            },
            "ransomware_attack": {
                "name": "Ransomware Attack Simulation",
                "description": "Simulate ransomware attack and recovery procedures",
                "duration_hours": 6,
                "objectives": [
                    "Test endpoint protection effectiveness",
                    "Validate backup and recovery procedures",
                    "Exercise crisis communications",
                    "Test legal and compliance response"
                ]
            },
            "supply_chain_compromise": {
                "name": "Supply Chain Compromise",
                "description": "Simulate supply chain attack targeting third-party software",
                "duration_hours": 8,
                "objectives": [
                    "Test vendor risk management",
                    "Validate software supply chain security",
                    "Exercise third-party incident response",
                    "Test network segmentation effectiveness"
                ]
            }
        }
    
    def create_exercise(self, name: str, scenario_key: str = None) -> Exercise:
        """Create new purple team exercise"""
        exercise_id = f"EX-{str(uuid.uuid4())[:8]}"
        
        if scenario_key and scenario_key in self.scenarios:
            scenario = self.scenarios[scenario_key]["description"]
        else:
            scenario = "Custom purple team exercise"
        
        exercise = Exercise(exercise_id, name, scenario)
        self.exercises[exercise_id] = exercise
        self.active_exercises.add(exercise_id)
        
        print(f"✅ Created purple team exercise: {name} ({exercise_id})")
        
        # Auto-add some team members
        self._seed_exercise_teams(exercise)
        
        return exercise
    
    def _seed_exercise_teams(self, exercise: Exercise) -> None:
        """Seed exercise with initial team members"""
        # Add red team members
        exercise.add_team_member("Red Operator Alpha", TeamRole.RED_TEAM, 
                                ["exploitation", "lateral_movement", "exfiltration"])
        exercise.add_team_member("Red Operator Beta", TeamRole.RED_TEAM,
                                ["phishing", "social_engineering", "initial_access"])
        
        # Add blue team members
        exercise.add_team_member("Blue Defender Prime", TeamRole.BLUE_TEAM,
                                ["detection", "incident_response", "forensics"])
        exercise.add_team_member("Blue Analyst One", TeamRole.BLUE_TEAM,
                                ["threat_hunting", "log_analysis", "malware_analysis"])
        
        # Add purple team members
        exercise.add_team_member("Purple Coordinator", TeamRole.PURPLE_TEAM,
                                ["coordination", "analysis", "debriefing"])
    
    def run_exercise_simulation(self, exercise_id: str) -> Dict:
        """Run automated exercise simulation"""
        if exercise_id not in self.exercises:
            raise ValueError(f"Exercise {exercise_id} not found")
        
        exercise = self.exercises[exercise_id]
        
        print(f"🚀 Starting exercise simulation: {exercise.name}")
        
        # Run through phases
        phases = [
            (ExercisePhase.PLANNING, 60),
            (ExercisePhase.RECONNAISSANCE, 120),
            (ExercisePhase.EXPLOITATION, 180),
            (ExercisePhase.DEFENSE, 150),
            (ExercisePhase.DETECTION, 120),
            (ExercisePhase.RESPONSE, 180),
            (ExercisePhase.DEBRIEF, 90)
        ]
        
        results = []
        
        for phase, duration in phases:
            print(f"   ⏳ Starting phase: {phase.value}")
            exercise.start_phase(phase)
            
            # Simulate phase activities
            phase_result = self._simulate_phase_activities(exercise, phase)
            results.append(phase_result)
            
            # Complete phase
            time.sleep(0.5)  # Simulate time passing
            exercise.complete_phase(phase)
            print(f"   ✅ Completed phase: {phase.value}")
        
        # Generate report
        report = exercise.generate_report()
        exercise.status = "completed"
        self.active_exercises.discard(exercise_id)
        
        print(f"🎉 Exercise simulation completed: {exercise.name}")
        print(f"   Findings: {report['metrics']['findings_metrics']['total_findings']}")
        print(f"   Detection rate: {report['metrics']['defense_metrics']['detection_rate_percent']}%")
        
        return {
            "exercise_id": exercise_id,
            "name": exercise.name,
            "simulation_complete": True,
            "report": report,
            "phase_results": results
        }
    
    def _simulate_phase_activities(self, exercise: Exercise, phase: ExercisePhase) -> Dict:
        """Simulate activities for a phase"""
        activities = []
        
        if phase == ExercisePhase.RECONNAISSANCE:
            # Red team reconnaissance
            exercise.record_red_team_action(
                "Network Scanning",
                Technique.EXTERNAL_REMOTE_SERVICES,
                "External Network",
                success=True,
                details="Performed port scanning and service enumeration"
            )
            activities.append("network_scanning")
        
        elif phase == ExercisePhase.EXPLOITATION:
            # Red team exploitation
            exercise.record_red_team_action(
                "Phishing Campaign",
                Technique.PHISHING,
                "User Email",
                success=random.choice([True, False]),
                details="Sent phishing emails with malicious attachments"
            )
            activities.append("phishing_campaign")
            
            # Blue team detection
            exercise.record_blue_team_action(
                "Email Filtering",
                Technique.DETECTION_RULES,
                detection=True,
                response=True,
                details="Blocked phishing emails using advanced filtering"
            )
            activities.append("email_filtering")
        
        elif phase == ExercisePhase.DETECTION:
            # Blue team detection actions
            exercise.record_blue_team_action(
                "Threat Hunting",
                Technique.THREAT_HUNTING,
                detection=True,
                response=False,
                details="Proactive threat hunting for suspicious activities"
            )
            activities.append("threat_hunting")
        
        elif phase == ExercisePhase.RESPONSE:
            # Incident response
            exercise.record_blue_team_action(
                "Incident Containment",
                Technique.INCIDENT_RESPONSE,
                detection=True,
                response=True,
                details="Contained affected systems and began investigation"
            )
            activities.append("incident_containment")
            
            # Add findings
            exercise.add_finding(
                "Security Control Gap",
                "high",
                "Email security controls need improvement for advanced phishing",
                "Implement DMARC, DKIM, and SPF; enhance user training"
            )
            activities.append("finding_documented")
        
        return {
            "phase": phase.value,
            "activities": activities,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict:
        """Get purple team manager status"""
        return {
            "component": self.name,
            "version": self.version,
            "status": "operational",
            "total_exercises": len(self.exercises),
            "active_exercises": len(self.active_exercises),
            "available_scenarios": len(self.scenarios),
            "capabilities": [
                "Automated exercise simulation",
                "Red/Blue team coordination",
                "Real-time metrics tracking",
                "Comprehensive reporting",
                "Lessons learned generation"
            ]
        }

def test_purple_team():
    """Test the OMEGA Purple Team component"""
    print("🧪 Testing OMEGA Purple Team...")
    
    try:
        # Initialize purple team manager
        manager = PurpleTeamManager()
        print("   ✅ Purple Team Manager initialized")
        
        # Create an exercise
        exercise = manager.create_exercise(
            "Test Ransomware Response",
            scenario_key="ransomware_attack"
        )
        
        print(f"   📋 Exercise created: {exercise.name}")
        print(f"   👥 Team members: {sum(len(team['members']) for team in exercise.teams.values())}")
        
        # Run simulation
        print("\n   🚀 Running exercise simulation...")
        simulation = manager.run_exercise_simulation(exercise.exercise_id)
        
        report = simulation["report"]
        
        print(f"\n   📊 Exercise Results:")
        print(f"      Duration: {report['duration_hours']} hours")
        print(f"      Red team actions: {report['metrics']['team_metrics']['red_team_actions']}")
        print(f"      Blue team actions: {report['metrics']['team_metrics']['blue_team_actions']}")
        print(f"      Findings: {report['metrics']['findings_metrics']['total_findings']}")
        print(f"      Detection rate: {report['metrics']['defense_metrics']['detection_rate_percent']}%")
        
        # Show recommendations
        print(f"\n   🎯 Recommendations:")
        for i, rec in enumerate(report['recommendations'][:3], 1):
            print(f"      {i}. {rec}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_purple_team()
    if success:
        print("\n✅ OMEGA Purple Team test passed!")
    else:
        print("\n❌ OMEGA Purple Team test failed!")
