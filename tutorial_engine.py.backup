"""
TUTORIAL ENGINE - Phase 2G
Project Omega - Interactive Learning & Safe Sandbox
Makes advanced security concepts accessible to everyone
"""

import json
import time
import logging
from datetime import datetime
from flask import jsonify, request
import threading
import os

class TutorialEngine:
    def __init__(self, omega_server):
        self.server = omega_server
        self.is_active = False
        self.current_tutorial = None
        self.tutorial_progress = {}
        self.user_level = "BEGINNER"  # BEGINNER, INTERMEDIATE, ADVANCED
        self.sandbox_mode = False
        
        # Tutorial database
        self.tutorials = {
            "welcome": {
                "id": "welcome",
                "title": "Welcome to Project Omega",
                "description": "Your first 15 minutes with the ultimate security platform",
                "estimated_time": 5,
                "difficulty": "BEGINNER",
                "steps": [
                    {
                        "id": "welcome_1",
                        "title": "System Overview",
                        "content": "Project Omega is a complete security platform that evolves from monitoring to autonomous defense. This tutorial will guide you through its core capabilities.",
                        "action": "none",
                        "duration": 30
                    },
                    {
                        "id": "welcome_2",
                        "title": "Dashboard Tour",
                        "content": "The main dashboard shows real-time metrics: CPU, memory, threat level, and active modules. Try hovering over different sections.",
                        "action": "hover_dashboard",
                        "duration": 45
                    },
                    {
                        "id": "welcome_3",
                        "title": "Your First Command",
                        "content": "Try typing 'system status' in the command input below to check Omega's current status.",
                        "action": "command:system status",
                        "duration": 60
                    }
                ],
                "completion_reward": "Omega Novice Badge"
            },
            
            "defense_basics": {
                "id": "defense_basics",
                "title": "Defensive Security Basics",
                "description": "Learn monitoring, threat detection, and system defense",
                "estimated_time": 10,
                "difficulty": "BEGINNER",
                "steps": [
                    {
                        "id": "defense_1",
                        "title": "Understanding Threats",
                        "content": "Threats come in many forms: malware, brute force attacks, data theft. Omega uses ML to predict threat levels in real-time.",
                        "action": "view_threat_panel",
                        "duration": 40
                    },
                    {
                        "id": "defense_2",
                        "title": "Simulate a Threat",
                        "content": "Click the 'Simulate Threat' button to see how Omega detects and responds to security incidents.",
                        "action": "click:simulate_threat",
                        "duration": 60
                    },
                    {
                        "id": "defense_3",
                        "title": "Network Scanning",
                        "content": "Network scans help discover vulnerabilities. Try starting a network scan to see the process.",
                        "action": "click:start_scan",
                        "duration": 75
                    }
                ],
                "completion_reward": "Defense Apprentice Badge",
                "requires": ["welcome"]
            },
            
            "deception_101": {
                "id": "deception_101",
                "title": "Deception Engine Fundamentals",
                "description": "Learn how honeypots trap and analyze attackers",
                "estimated_time": 15,
                "difficulty": "INTERMEDIATE",
                "steps": [
                    {
                        "id": "deception_1",
                        "title": "What are Honeypots?",
                        "content": "Honeypots are fake services that attract attackers. They help us study attack patterns without risking real systems.",
                        "action": "view_deception_panel",
                        "duration": 45
                    },
                    {
                        "id": "deception_2",
                        "title": "Deploy Your First Honeypot",
                        "content": "Type 'deception start low' to deploy a basic web honeypot on port 8088.",
                        "action": "command:deception start low",
                        "duration": 90
                    },
                    {
                        "id": "deception_3",
                        "title": "Test the Honeypot",
                        "content": "In a new terminal, run: curl http://localhost:8088/ or simply visit it in your browser.",
                        "action": "test_honeypot",
                        "duration": 120
                    },
                    {
                        "id": "deception_4",
                        "title": "Analyze Results",
                        "content": "Check the deception logs to see the connection attempt. This is how we learn about attackers.",
                        "action": "view_deception_logs",
                        "duration": 60
                    }
                ],
                "completion_reward": "Deception Specialist Badge",
                "requires": ["defense_basics"]
            },
            
            "autonomous_response": {
                "id": "autonomous_response",
                "title": "Autonomous Response System",
                "description": "Learn how Omega automatically responds to threats",
                "estimated_time": 12,
                "difficulty": "INTERMEDIATE",
                "steps": [
                    {
                        "id": "response_1",
                        "title": "Automated Defense",
                        "content": "Omega can automatically block attackers, isolate networks, and alert administrators.",
                        "action": "view_response_panel",
                        "duration": 40
                    },
                    {
                        "id": "response_2",
                        "title": "Activate Response System",
                        "content": "Type 'response activate moderate' to enable autonomous threat response.",
                        "action": "command:response activate moderate",
                        "duration": 60
                    },
                    {
                        "id": "response_3",
                        "title": "Trigger Automated Defense",
                        "content": "With deception active and response enabled, connect to a honeypot. Watch the autonomous response trigger!",
                        "action": "trigger_auto_response",
                        "duration": 120
                    }
                ],
                "completion_reward": "Response Operator Badge",
                "requires": ["deception_101"]
            },
            
            "sandbox_lab": {
                "id": "sandbox_lab",
                "title": "Safe Sandbox Laboratory",
                "description": "Experiment with security concepts in a risk-free environment",
                "estimated_time": 20,
                "difficulty": "ADVANCED",
                "steps": [
                    {
                        "id": "sandbox_1",
                        "title": "Enter Sandbox Mode",
                        "content": "Sandbox mode creates an isolated environment where all actions are simulated and safe.",
                        "action": "activate_sandbox",
                        "duration": 30
                    },
                    {
                        "id": "sandbox_2",
                        "title": "Attack Simulation",
                        "content": "In sandbox mode, try aggressive commands without risk. Test 'response activate aggressive' followed by various attack simulations.",
                        "action": "sandbox_experiment",
                        "duration": 180
                    },
                    {
                        "id": "sandbox_3",
                        "title": "Scenario Training",
                        "content": "Try the 'Data Breach Response' scenario to practice real-world incident handling.",
                        "action": "start_scenario:data_breach",
                        "duration": 240
                    }
                ],
                "completion_reward": "Sandbox Master Badge",
                "requires": ["autonomous_response"]
            }
        }
        
        # Training scenarios (safe simulations)
        self.scenarios = {
            "data_breach": {
                "name": "Data Breach Response",
                "description": "Practice responding to a simulated data exfiltration attempt",
                "steps": 5,
                "safe_commands": [
                    "response activate aggressive",
                    "deception start high", 
                    "system lockdown simulate",
                    "forensic capture start",
                    "incident report generate"
                ]
            },
            "ransomware": {
                "name": "Ransomware Containment",
                "description": "Learn to contain and recover from ransomware attacks",
                "steps": 6,
                "safe_commands": [
                    "isolate network segment 192.168.1.0/24",
                    "initiate backup emergency",
                    "malware scan full",
                    "restore from backup 2025-12-15",
                    "post incident review"
                ]
            }
        }
        
        # User achievements
        self.achievements = {
            "omega_novice": {"name": "Omega Novice", "description": "Completed welcome tutorial", "icon": "🎓"},
            "defense_apprentice": {"name": "Defense Apprentice", "description": "Mastered defensive basics", "icon": "🛡️"},
            "deception_specialist": {"name": "Deception Specialist", "description": "Expert in honeypot deployment", "icon": "🕵️"},
            "response_operator": {"name": "Response Operator", "description": "Skilled in autonomous response", "icon": "🤖"},
            "sandbox_master": {"name": "Sandbox Master", "description": "Mastered safe experimentation", "icon": "🧪"},
            "quick_learner": {"name": "Quick Learner", "description": "Completed 3 tutorials in under 30 minutes", "icon": "⚡"}
        }
        
        self.setup_logging()
        print("[TUTORIAL] Tutorial Engine initialized")
    
    def setup_logging(self):
        """Setup tutorial logging"""
        os.makedirs('tutorial_engine/logs', exist_ok=True)
        self.logger = logging.getLogger('tutorial_engine')
        handler = logging.FileHandler('tutorial_engine/logs/tutorial.log')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def start_tutorial(self, tutorial_id):
        """Start a specific tutorial"""
        if tutorial_id not in self.tutorials:
            return {"status": "error", "message": f"Tutorial '{tutorial_id}' not found"}
        
        tutorial = self.tutorials[tutorial_id]
        
        # Check prerequisites
        if "requires" in tutorial:
            for req in tutorial["requires"]:
                if req not in self.tutorial_progress or not self.tutorial_progress[req].get("completed"):
                    return {"status": "error", "message": f"Complete '{req}' tutorial first"}
        
        self.current_tutorial = tutorial
        self.is_active = True
        
        # Initialize progress
        if tutorial_id not in self.tutorial_progress:
            self.tutorial_progress[tutorial_id] = {
                "started": datetime.now().isoformat(),
                "current_step": 0,
                "completed_steps": [],
                "completed": False
            }
        
        self.logger.info(f"Started tutorial: {tutorial['title']}")
        
        # Send WebSocket update
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('tutorial_started', {
                'tutorial_id': tutorial_id,
                'title': tutorial['title'],
                'step_count': len(tutorial['steps']),
                'timestamp': datetime.now().isoformat()
            })
        
        # Send first step details
        first_step = tutorial['steps'][0]
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('tutorial_step_active', {
                'step_id': first_step['id'],
                'title': first_step['title'],
                'content': first_step['content'],
                'action': first_step.get('action', 'none'),
                'timestamp': datetime.now().isoformat()
            })
        
        return {
            "status": "success",
            "message": f"Started tutorial: {tutorial['title']}",
            "tutorial": tutorial,
            "current_step": 0
        }
    
    def complete_step(self, tutorial_id, step_id):
        """Mark a tutorial step as completed"""
        if tutorial_id not in self.tutorial_progress:
            return {"status": "error", "message": "Tutorial not in progress"}
        
        if step_id not in self.tutorial_progress[tutorial_id]["completed_steps"]:
            self.tutorial_progress[tutorial_id]["completed_steps"].append(step_id)
            
            # Check if all steps completed
            tutorial = self.tutorials[tutorial_id]
            if len(self.tutorial_progress[tutorial_id]["completed_steps"]) >= len(tutorial["steps"]):
                return self.complete_tutorial(tutorial_id)
            
            self.logger.info(f"Completed step: {step_id} in tutorial: {tutorial_id}")
            
            # Move to next step
            current_step_index = len(self.tutorial_progress[tutorial_id]["completed_steps"])
            if current_step_index < len(tutorial["steps"]):
                next_step = tutorial["steps"][current_step_index]
                if hasattr(self.server, 'socketio'):
                    self.server.socketio.emit('tutorial_step_active', {
                        'step_id': next_step['id'],
                        'title': next_step['title'],
                        'content': next_step['content'],
                        'action': next_step.get('action', 'none'),
                        'timestamp': datetime.now().isoformat()
                    })
            
            if hasattr(self.server, 'socketio'):
                self.server.socketio.emit('tutorial_progress', {
                    'tutorial_id': tutorial_id,
                    'step_id': step_id,
                    'completed_steps': len(self.tutorial_progress[tutorial_id]["completed_steps"]),
                    'total_steps': len(tutorial["steps"]),
                    'timestamp': datetime.now().isoformat()
                })
        
        return {"status": "success", "step_completed": step_id}
    
    def complete_tutorial(self, tutorial_id):
        """Mark a tutorial as completed"""
        if tutorial_id in self.tutorial_progress:
            self.tutorial_progress[tutorial_id]["completed"] = True
            self.tutorial_progress[tutorial_id]["completed_at"] = datetime.now().isoformat()
            
            # Award achievement
            reward = self.tutorials[tutorial_id].get("completion_reward", "")
            
            self.logger.info(f"Completed tutorial: {tutorial_id} - Reward: {reward}")
            
            if hasattr(self.server, 'socketio'):
                self.server.socketio.emit('tutorial_completed', {
                    'tutorial_id': tutorial_id,
                    'title': self.tutorials[tutorial_id]["title"],
                    'reward': reward,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check for Quick Learner achievement
            self.check_achievements()
            
            return {"status": "success", "tutorial_completed": tutorial_id, "reward": reward}
        
        return {"status": "error", "message": "Tutorial not found in progress"}
    
    def check_achievements(self):
        """Check and award achievements"""
        completed_count = sum(1 for t in self.tutorial_progress.values() if isinstance(t, dict) and t.get("completed"))
        
        # Quick Learner achievement
        if completed_count >= 3:
            achievement_key = "quick_learner"
            if "_achievements" not in self.tutorial_progress:
                self.tutorial_progress["_achievements"] = {}
            
            if achievement_key not in self.tutorial_progress["_achievements"]:
                self.tutorial_progress["_achievements"][achievement_key] = {
                    "awarded": datetime.now().isoformat()
                }
                
                if hasattr(self.server, 'socketio'):
                    self.server.socketio.emit('achievement_unlocked', {
                        'achievement': self.achievements[achievement_key],
                        'timestamp': datetime.now().isoformat()
                    })
    
    def activate_sandbox_mode(self):
        """Activate safe sandbox environment"""
        self.sandbox_mode = True
        self.logger.info("Sandbox mode activated - all commands are safe simulations")
        
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('sandbox_activated', {
                'status': 'active',
                'message': '🧪 SANDBOX MODE ACTIVATED - Safe experimentation enabled',
                'timestamp': datetime.now().isoformat()
            })
        
        return {"status": "success", "message": "Sandbox mode activated"}
    
    def deactivate_sandbox_mode(self):
        """Deactivate sandbox mode"""
        self.sandbox_mode = False
        self.logger.info("Sandbox mode deactivated")
        
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('sandbox_deactivated', {
                'status': 'inactive',
                'message': 'Sandbox mode deactivated',
                'timestamp': datetime.now().isoformat()
            })
        
        return {"status": "success", "message": "Sandbox mode deactivated"}
    
    def is_sandbox_command(self, command):
        """Check if command is safe for sandbox mode"""
        safe_commands = [
            "response activate", "response deactivate", "response status",
            "deception start", "deception stop", "deception status",
            "system status", "help", "tutorial"
        ]
        
        for safe_cmd in safe_commands:
            if command.startswith(safe_cmd):
                return True
        
        # Check scenario commands
        if self.sandbox_mode:
            for scenario in self.scenarios.values():
                for safe_cmd in scenario["safe_commands"]:
                    if command.startswith(safe_cmd):
                        return True
        
        return False
    
    def process_sandbox_command(self, command):
        """Process a command in sandbox mode (simulated safe execution)"""
        if not self.sandbox_mode:
            return {"status": "error", "message": "Sandbox mode not active"}
        
        # Simulate command execution
        simulation_result = {
            "command": command,
            "status": "simulated",
            "message": f"[SANDBOX] Simulated execution: {command}",
            "output": "This action was simulated in sandbox mode. No real system changes were made.",
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"Sandbox command: {command}")
        
        if hasattr(self.server, 'socketio'):
            self.server.socketio.emit('sandbox_command', simulation_result)
        
        return simulation_result
    
    def get_tutorial_status(self):
        """Get current tutorial status"""
        return {
            "active": self.is_active,
            "current_tutorial": self.current_tutorial["id"] if self.current_tutorial else None,
            "sandbox_mode": self.sandbox_mode,
            "user_level": self.user_level,
            "progress": self.tutorial_progress,
            "available_tutorials": list(self.tutorials.keys())
        }
    
    def get_recommended_tutorial(self):
        """Get recommended tutorial based on user progress"""
        completed = [t for t, p in self.tutorial_progress.items() if isinstance(p, dict) and p.get("completed")]
        
        for tutorial_id, tutorial in self.tutorials.items():
            if tutorial_id in completed:
                continue
            
            # Check prerequisites
            if "requires" in tutorial:
                prereq_met = all(req in completed for req in tutorial["requires"])
                if not prereq_met:
                    continue
            
            return tutorial_id
        
        return None

