#!/usr/bin/env python3
"""
JAIDA Sovereign Hierarchy System
GC-class (General Contractors) and WD-class (Worker Drones)
with persistent registry and partition management
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pickle

class BotType(Enum):
    """Types of bots in the hierarchy"""
    GC_THREAT_MODELER = "gc_threat_modeler"
    GC_BOT_FATHER = "gc_bot_father"
    GC_DATA_ANALYST = "gc_data_analyst"
    GC_WEB_CRAWLER = "gc_web_crawler"
    
    WD_SURFACE_CRAWLER = "wd_surface_crawler"
    WD_DEEP_CRAWLER = "wd_deep_crawler"
    WD_IOC_EXTRACTOR = "wd_ioc_extractor"
    WD_REPORT_GENERATOR = "wd_report_generator"
    WD_CODE_WRITER = "wd_code_writer"

class BotStatus(Enum):
    """Bot operational status"""
    ACTIVE = "active"
    IDLE = "idle"
    ERROR = "error"
    QUARANTINED = "quarantined"
    TERMINATED = "terminated"

class PermissionLevel(Enum):
    """Authorization levels"""
    SOVEREIGN = "sovereign"      # JAI-LSD-25 level
    GC_TIER1 = "gc_tier1"        # Maximum GC privileges
    GC_TIER2 = "gc_tier2"        # Standard GC privileges
    WD_PRIVILEGED = "wd_priv"    # WD with cross-task access
    WD_STANDARD = "wd_std"       # Standard WD single-task

@dataclass
class BotMemory:
    """Persistent memory for a bot"""
    experiences: List[Dict] = None
    learned_patterns: List[Dict] = None
    performance_metrics: Dict = None
    skill_improvements: List[str] = None
    
    def __post_init__(self):
        if self.experiences is None:
            self.experiences = []
        if self.learned_patterns is None:
            self.learned_patterns = []
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.skill_improvements is None:
            self.skill_improvements = []

@dataclass
class WorkerDrone:
    """WD-class: Singular task specialist"""
    id: str
    name: str
    bot_type: BotType
    task_description: str
    commissioned_by: str  # GC ID that created this WD
    created: datetime
    status: BotStatus
    permissions: PermissionLevel
    memory: BotMemory
    last_active: datetime = None
    performance_score: float = 0.0
    
    def execute_task(self, task_data: Dict) -> Dict:
        """Execute the WD's specialized task"""
        self.last_active = datetime.now()
        
        # Base implementation - to be overridden by specific WD classes
        result = {
            "wd_id": self.id,
            "task": self.task_description,
            "timestamp": self.last_active.isoformat(),
            "status": "executed",
            "result": f"Executed {self.task_description} with data: {task_data}"
        }
        
        # Record experience
        self.memory.experiences.append({
            "timestamp": self.last_active.isoformat(),
            "task": task_data,
            "result": result
        })
        
        return result
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['bot_type'] = self.bot_type.value
        data['status'] = self.status.value
        data['permissions'] = self.permissions.value
        data['created'] = self.created.isoformat()
        if self.last_active:
            data['last_active'] = self.last_active.isoformat()
        return data

@dataclass
class GeneralContractor:
    """GC-class: Compound intelligence system"""
    id: str
    name: str
    bot_type: BotType
    description: str
    created: datetime
    status: BotStatus
    permissions: PermissionLevel
    memory: BotMemory
    worker_drones: List[str]  # List of WD IDs under this GC
    project_assignments: List[str]
    last_active: datetime = None
    authority_level: int = 1
    
    def commission_worker(self, wd_type: BotType, task: str, 
                         permissions: PermissionLevel = PermissionLevel.WD_STANDARD) -> WorkerDrone:
        """Commission a new Worker Drone"""
        wd_id = f"WD-{wd_type.value}-{uuid.uuid4().hex[:8]}"
        wd_name = f"{task.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        worker = WorkerDrone(
            id=wd_id,
            name=wd_name,
            bot_type=wd_type,
            task_description=task,
            commissioned_by=self.id,
            created=datetime.now(),
            status=BotStatus.ACTIVE,
            permissions=permissions,
            memory=BotMemory()
        )
        
        self.worker_drones.append(wd_id)
        self.last_active = datetime.now()
        
        # Record this commissioning in GC memory
        self.memory.experiences.append({
            "timestamp": self.last_active.isoformat(),
            "action": "commission_worker",
            "worker_type": wd_type.value,
            "task": task,
            "worker_id": wd_id
        })
        
        return worker
    
    def command_worker(self, wd_id: str, command: Dict) -> Dict:
        """Command a specific Worker Drone"""
        # In full implementation, would look up WD and execute command
        self.last_active = datetime.now()
        
        return {
            "gc_id": self.id,
            "wd_id": wd_id,
            "command": command,
            "timestamp": self.last_active.isoformat(),
            "status": "command_issued"
        }
    
    def analyze_project(self, project_data: Dict) -> Dict:
        """Analyze a project and determine requirements"""
        self.last_active = datetime.now()
        
        analysis = {
            "gc_id": self.id,
            "project": project_data.get("name", "unknown"),
            "timestamp": self.last_active.isoformat(),
            "analysis": {
                "complexity": "high",
                "estimated_wds": 3,
                "required_skills": ["crawling", "analysis", "reporting"],
                "recommended_approach": "Divide into specialized tasks"
            }
        }
        
        # Learn from this analysis
        self.memory.learned_patterns.append({
            "timestamp": self.last_active.isoformat(),
            "project_type": project_data.get("type", "unknown"),
            "analysis_pattern": analysis["analysis"]
        })
        
        return analysis
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['bot_type'] = self.bot_type.value
        data['status'] = self.status.value
        data['permissions'] = self.permissions.value
        data['created'] = self.created.isoformat()
        if self.last_active:
            data['last_active'] = self.last_active.isoformat()
        return data

class SovereignRegistry:
    """Central registry for all bots with persistent storage"""
    
    def __init__(self, registry_file: str = "sovereign_registry.json"):
        self.registry_file = registry_file
        self.gc_bots: Dict[str, GeneralContractor] = {}
        self.wd_bots: Dict[str, WorkerDrone] = {}
        self.partitions: Dict[str, List[str]] = {}  # partition_id -> list of isolated GCs
        self.hierarchy_log: List[Dict] = []
        
        self._load_registry()
    
    def _load_registry(self):
        """Load registry from disk"""
        try:
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                
                # Load GC bots
                for gc_data in data.get('gc_bots', []):
                    gc = GeneralContractor(
                        id=gc_data['id'],
                        name=gc_data['name'],
                        bot_type=BotType(gc_data['bot_type']),
                        description=gc_data['description'],
                        created=datetime.fromisoformat(gc_data['created']),
                        status=BotStatus(gc_data['status']),
                        permissions=PermissionLevel(gc_data['permissions']),
                        memory=BotMemory(**gc_data['memory']),
                        worker_drones=gc_data['worker_drones'],
                        project_assignments=gc_data['project_assignments'],
                        authority_level=gc_data.get('authority_level', 1)
                    )
                    if gc_data.get('last_active'):
                        gc.last_active = datetime.fromisoformat(gc_data['last_active'])
                    self.gc_bots[gc.id] = gc
                
                # Load WD bots
                for wd_data in data.get('wd_bots', []):
                    wd = WorkerDrone(
                        id=wd_data['id'],
                        name=wd_data['name'],
                        bot_type=BotType(wd_data['bot_type']),
                        task_description=wd_data['task_description'],
                        commissioned_by=wd_data['commissioned_by'],
                        created=datetime.fromisoformat(wd_data['created']),
                        status=BotStatus(wd_data['status']),
                        permissions=PermissionLevel(wd_data['permissions']),
                        memory=BotMemory(**wd_data['memory']),
                        performance_score=wd_data.get('performance_score', 0.0)
                    )
                    if wd_data.get('last_active'):
                        wd.last_active = datetime.fromisoformat(wd_data['last_active'])
                    self.wd_bots[wd.id] = wd
                
                self.partitions = data.get('partitions', {})
                self.hierarchy_log = data.get('hierarchy_log', [])
                
            print(f"✅ Loaded registry: {len(self.gc_bots)} GCs, {len(self.wd_bots)} WDs")
        except FileNotFoundError:
            print("⚠️ No registry found, starting fresh")
            self._initialize_default_hierarchy()
        except Exception as e:
            print(f"❌ Error loading registry: {e}")
            self._initialize_default_hierarchy()
    
    def _initialize_default_hierarchy(self):
        """Initialize with default GC bots"""
        print("🏗️ Initializing default sovereign hierarchy...")
        
        # Create Bot Father (highest authority)
        bot_father = GeneralContractor(
            id="GC-BOT-FATHER-001",
            name="Bot Father Prime",
            bot_type=BotType.GC_BOT_FATHER,
            description="Primary bot creation and management system",
            created=datetime.now(),
            status=BotStatus.ACTIVE,
            permissions=PermissionLevel.GC_TIER1,
            memory=BotMemory(),
            worker_drones=[],
            project_assignments=["bot_creation", "skill_optimization"],
            authority_level=3
        )
        self.gc_bots[bot_father.id] = bot_father
        
        # Create Threat Modeler GC
        threat_modeler = GeneralContractor(
            id="GC-THREAT-MODELER-001",
            name="Threat Modeler Alpha",
            bot_type=BotType.GC_THREAT_MODELER,
            description="Threat intelligence analysis and modeling",
            created=datetime.now(),
            status=BotStatus.ACTIVE,
            permissions=PermissionLevel.GC_TIER2,
            memory=BotMemory(),
            worker_drones=[],
            project_assignments=["threat_analysis", "risk_assessment"],
            authority_level=2
        )
        self.gc_bots[threat_modeler.id] = threat_modeler
        
        # Create Web Crawler GC
        web_crawler = GeneralContractor(
            id="GC-WEB-CRAWLER-001",
            name="Web Crawler Command",
            bot_type=BotType.GC_WEB_CRAWLER,
            description="Web data harvesting and monitoring",
            created=datetime.now(),
            status=BotStatus.ACTIVE,
            permissions=PermissionLevel.GC_TIER2,
            memory=BotMemory(),
            worker_drones=[],
            project_assignments=["data_harvesting", "ioc_monitoring"],
            authority_level=2
        )
        self.gc_bots[web_crawler.id] = web_crawler
        
        self._save_registry()
    
    def create_partition(self, partition_id: str, gc_ids: List[str], reason: str = ""):
        """Create temporary isolation between GCs"""
        self.partitions[partition_id] = gc_ids
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": "create_partition",
            "partition_id": partition_id,
            "isolated_gcs": gc_ids,
            "reason": reason
        }
        self.hierarchy_log.append(log_entry)
        
        self._save_registry()
        print(f"🔒 Partition '{partition_id}' created isolating: {gc_ids}")
        return partition_id
    
    def can_communicate(self, gc_id_1: str, gc_id_2: str) -> bool:
        """Check if two GCs can communicate across partitions"""
        for partition_id, isolated_gcs in self.partitions.items():
            if gc_id_1 in isolated_gcs and gc_id_2 in isolated_gcs:
                return False
        return True
    
    def get_gc_workers(self, gc_id: str) -> List[WorkerDrone]:
        """Get all Worker Drones under a GC"""
        gc = self.gc_bots.get(gc_id)
        if not gc:
            return []
        
        workers = []
        for wd_id in gc.worker_drones:
            if wd_id in self.wd_bots:
                workers.append(self.wd_bots[wd_id])
        
        return workers
    
    def display_hierarchy(self):
        """Display current hierarchy"""
        print("\n" + "="*60)
        print("🤖 JAIDA SOVEREIGN HIERARCHY")
        print("="*60)
        
        print("\n🏢 GENERAL CONTRACTORS:")
        for gc_id, gc in self.gc_bots.items():
            print(f"\n  📋 {gc.name} ({gc_id})")
            print(f"     Type: {gc.bot_type.value}")
            print(f"     Status: {gc.status.value}, Authority: {gc.authority_level}")
            print(f"     Workers: {len(gc.worker_drones)}, Projects: {len(gc.project_assignments)}")
            
            # Show workers
            workers = self.get_gc_workers(gc_id)
            if workers:
                print(f"     Active Workers:")
                for wd in workers[:3]:  # Show first 3
                    print(f"       • {wd.name}: {wd.task_description[:40]}...")
                if len(workers) > 3:
                    print(f"       ... and {len(workers) - 3} more")
        
        print(f"\n👷 WORKER DRONES: {len(self.wd_bots)} total")
        
        print("\n🔒 ACTIVE PARTITIONS:")
        if self.partitions:
            for partition_id, gc_ids in self.partitions.items():
                print(f"   • {partition_id}: {len(gc_ids)} GCs isolated")
        else:
            print("   ✅ No active partitions")
        
        print("\n📊 STATS:")
        print(f"   GC Bots: {len(self.gc_bots)}")
        print(f"   WD Bots: {len(self.wd_bots)}")
        print(f"   Total Experiences: {sum(len(gc.memory.experiences) for gc in self.gc_bots.values())}")
        print("="*60)
    
    def _save_registry(self):
        """Save registry to disk"""
        data = {
            "gc_bots": [gc.to_dict() for gc in self.gc_bots.values()],
            "wd_bots": [wd.to_dict() for wd in self.wd_bots.values()],
            "partitions": self.partitions,
            "hierarchy_log": self.hierarchy_log,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.registry_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def save(self):
        """Public save method"""
        self._save_registry()
        print(f"💾 Registry saved: {self.registry_file}")

# Test the hierarchy
if __name__ == "__main__":
    print("🧪 Testing Sovereign Hierarchy System...")
    
    registry = SovereignRegistry()
    
    # Display initial hierarchy
    registry.display_hierarchy()
    
    # Bot Father commissions a worker
    bot_father = registry.gc_bots["GC-BOT-FATHER-001"]
    print(f"\n🎯 {bot_father.name} commissioning a worker...")
    
    new_wd = bot_father.commission_worker(
        wd_type=BotType.WD_CODE_WRITER,
        task="Generate Python scripts for web scraping automation",
        permissions=PermissionLevel.WD_PRIVILEGED
    )
    
    # Add to registry
    registry.wd_bots[new_wd.id] = new_wd
    registry.save()
    
    # Create a partition
    registry.create_partition(
        partition_id="project_alpha",
        gc_ids=["GC-THREAT-MODELER-001", "GC-WEB-CRAWLER-001"],
        reason="Isolating sensitive threat analysis project"
    )
    
    # Display updated hierarchy
    registry.display_hierarchy()
    
    print("\n✅ Sovereign Hierarchy System ready!")
    print("🎯 Next: Integrate with existing Omega Platform components")
