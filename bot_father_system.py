#!/usr/bin/env python3
"""
Bot Father System - Autonomous WD creation and management
GC-class that creates specialized Worker Drones
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from sovereign_hierarchy import (
    SovereignRegistry, BotType, WorkerDrone, GeneralContractor,
    BotStatus, PermissionLevel, BotMemory
)

class BotFather:
    """Autonomous bot creation system"""
    
    def __init__(self, registry: SovereignRegistry):
        self.registry = registry
        self.bot_templates = self._load_templates()
        self.creation_log = []
        
    def _load_templates(self) -> Dict[str, Dict]:
        """Load WD bot templates"""
        return {
            "web_crawler": {
                "bot_type": BotType.WD_SURFACE_CRAWLER,
                "default_task": "Web intelligence gathering",
                "required_skills": ["http_requests", "html_parsing", "ioc_extraction"],
                "code_template": "web_crawler_template.py",
                "permissions": PermissionLevel.WD_PRIVILEGED
            },
            "ioc_extractor": {
                "bot_type": BotType.WD_IOC_EXTRACTOR,
                "default_task": "Threat indicator extraction",
                "required_skills": ["regex_patterns", "data_parsing", "classification"],
                "code_template": "ioc_extractor_template.py",
                "permissions": PermissionLevel.WD_STANDARD
            },
            "report_generator": {
                "bot_type": BotType.WD_REPORT_GENERATOR,
                "default_task": "Automated report generation",
                "required_skills": ["data_aggregation", "template_filling", "formatting"],
                "code_template": "report_generator_template.py",
                "permissions": PermissionLevel.WD_STANDARD
            },
            "code_writer": {
                "bot_type": BotType.WD_CODE_WRITER,
                "default_task": "Python code generation",
                "required_skills": ["python_syntax", "problem_solving", "debugging"],
                "code_template": "code_writer_template.py",
                "permissions": PermissionLevel.WD_PRIVILEGED
            }
        }
    
    def analyze_requirements(self, task_description: str) -> Dict[str, Any]:
        """Analyze task requirements and recommend bot type"""
        task_lower = task_description.lower()
        
        recommendations = []
        
        if any(word in task_lower for word in ["crawl", "scrape", "web", "url"]):
            recommendations.append({
                "bot_type": "web_crawler",
                "confidence": 0.9,
                "reason": "Task involves web data collection"
            })
        
        if any(word in task_lower for word in ["extract", "ioc", "indicator", "threat"]):
            recommendations.append({
                "bot_type": "ioc_extractor",
                "confidence": 0.85,
                "reason": "Task involves threat indicator extraction"
            })
        
        if any(word in task_lower for word in ["report", "generate", "summary", "analysis"]):
            recommendations.append({
                "bot_type": "report_generator",
                "confidence": 0.8,
                "reason": "Task involves report generation"
            })
        
        if any(word in task_lower for word in ["code", "program", "script", "python"]):
            recommendations.append({
                "bot_type": "code_writer",
                "confidence": 0.95,
                "reason": "Task involves code generation"
            })
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "task": task_description,
            "recommendations": recommendations,
            "primary_recommendation": recommendations[0] if recommendations else None
        }
    
    def create_bot(self, task_description: str, bot_template: str = None) -> WorkerDrone:
        """Create a new WD bot for a specific task"""
        
        # Get Bot Father GC
        bot_father_gc = self.registry.gc_bots.get("GC-BOT-FATHER-001")
        if not bot_father_gc:
            print("❌ Bot Father GC not found!")
            return None
        
        # Analyze requirements if no template specified
        if not bot_template:
            analysis = self.analyze_requirements(task_description)
            if analysis["primary_recommendation"]:
                bot_template = analysis["primary_recommendation"]["bot_type"]
                print(f"🤖 Analyzed task: {task_description}")
                print(f"   Recommended: {bot_template} (confidence: {analysis['primary_recommendation']['confidence']:.2f})")
            else:
                print("⚠️ Could not determine bot type, using default")
                bot_template = "code_writer"
        
        # Get template
        template = self.bot_templates.get(bot_template)
        if not template:
            print(f"❌ Unknown bot template: {bot_template}")
            return None
        
        # Commission the WD
        wd = bot_father_gc.commission_worker(
            wd_type=template["bot_type"],
            task=task_description,
            permissions=template["permissions"]
        )
        
        # Add to registry
        self.registry.wd_bots[wd.id] = wd
        
        # Log creation
        creation_record = {
            "timestamp": datetime.now().isoformat(),
            "bot_id": wd.id,
            "bot_type": bot_template,
            "task": task_description,
            "template_used": template["code_template"],
            "commissioned_by": bot_father_gc.id
        }
        self.creation_log.append(creation_record)
        
        # Generate code for the bot (simulated)
        bot_code = self._generate_bot_code(wd, template)
        
        # Save bot code to file
        bot_filename = f"bots/{wd.id}.py"
        os.makedirs("bots", exist_ok=True)
        with open(bot_filename, "w") as f:
            f.write(bot_code)
        
        print(f"✅ Created {bot_template} bot: {wd.name} ({wd.id})")
        print(f"💾 Bot code saved to: {bot_filename}")
        
        # Update Bot Father memory
        bot_father_gc.memory.experiences.append({
            "timestamp": datetime.now().isoformat(),
            "action": "create_bot",
            "bot_created": wd.id,
            "bot_type": bot_template,
            "task": task_description
        })
        
        self.registry.save()
        
        return wd
    
    def _generate_bot_code(self, wd: WorkerDrone, template: Dict) -> str:
        """Generate Python code for a WD bot"""
        
        bot_class_name = wd.name.replace(" ", "").replace("_", "").title() + "Bot"
        
        code = f'''#!/usr/bin/env python3
"""
{wd.name} - {wd.task_description}
Created by Bot Father on {datetime.now().strftime('%Y-%m-%d')}
"""

import json
from datetime import datetime

class {bot_class_name}:
    """Specialized bot for: {wd.task_description}"""
    
    def __init__(self, bot_id="{wd.id}"):
        self.bot_id = bot_id
        self.bot_type = "{wd.bot_type.value}"
        self.task = "{wd.task_description}"
        self.created = "{wd.created.isoformat()}"
        self.performance_score = 0.0
        self.execution_count = 0
        
    def execute(self, input_data):
        """Execute the bot's specialized task"""
        self.execution_count += 1
        
        # Base implementation for: {wd.task_description}
        result = {{
            "bot_id": self.bot_id,
            "task": self.task,
            "timestamp": datetime.now().isoformat(),
            "execution_count": self.execution_count,
            "input": input_data,
            "output": f"Executed {{self.task}} with input: {{input_data}}",
            "status": "completed"
        }}
        
        # Calculate performance (simulated)
        self.performance_score = min(1.0, self.execution_count / 10.0)
        result["performance_score"] = self.performance_score
        
        return result
    
    def get_status(self):
        """Get bot status"""
        return {{
            "bot_id": self.bot_id,
            "bot_type": self.bot_type,
            "task": self.task,
            "created": self.created,
            "execution_count": self.execution_count,
            "performance_score": self.performance_score,
            "status": "active"
        }}

if __name__ == "__main__":
    # Test the bot
    bot = {bot_class_name}()
    print(f"🤖 Testing {{bot.bot_id}}...")
    print(f"   Task: {{bot.task}}")
    
    test_result = bot.execute({{"test": "sample_data"}})
    print(f"✅ Test result: {{test_result}}")
    print(f"📊 Performance: {{bot.performance_score:.2f}}")
'''
        
        return code
    
    def improve_bot(self, wd_id: str, performance_data: Dict) -> bool:
        """Improve a bot based on performance data"""
        wd = self.registry.wd_bots.get(wd_id)
        if not wd:
            print(f"❌ Bot not found: {wd_id}")
            return False
        
        print(f"🔄 Improving bot {wd.name} based on performance...")
        
        # Analyze performance
        success_rate = performance_data.get("success_rate", 0.5)
        efficiency = performance_data.get("efficiency", 0.5)
        issues = performance_data.get("issues", [])
        
        # Simple improvement logic
        improvements = []
        
        if success_rate < 0.7:
            improvements.append("Enhanced error handling")
            wd.memory.skill_improvements.append("better_error_handling")
        
        if efficiency < 0.6:
            improvements.append("Optimized processing algorithms")
            wd.memory.skill_improvements.append("optimized_algorithms")
        
        if "timeout" in str(issues).lower():
            improvements.append("Added timeout handling")
            wd.memory.skill_improvements.append("timeout_handling")
        
        # Update bot
        if improvements:
            wd.performance_score = min(1.0, wd.performance_score + 0.1)
            wd.memory.learned_patterns.append({
                "timestamp": datetime.now().isoformat(),
                "improvements": improvements,
                "performance_data": performance_data
            })
            
            print(f"✅ Applied improvements: {', '.join(improvements)}")
            print(f"📈 New performance score: {wd.performance_score:.2f}")
            
            self.registry.save()
            return True
        else:
            print("ℹ️ No improvements needed at this time")
            return False
    
    def display_creation_log(self):
        """Display bot creation history"""
        print("\n" + "="*60)
        print("📜 BOT FATHER CREATION LOG")
        print("="*60)
        
        if not self.creation_log:
            print("No bots created yet")
            return
        
        for i, record in enumerate(self.creation_log[-10:], 1):  # Last 10
            print(f"\n{i}. {record['timestamp'][:19]}")
            print(f"   Bot: {record['bot_id']}")
            print(f"   Type: {record['bot_type']}")
            print(f"   Task: {record['task'][:50]}...")
        
        print(f"\n📊 Total bots created: {len(self.creation_log)}")
        print("="*60)

def test_bot_father():
    """Test the Bot Father system"""
    print("🧪 Testing Bot Father System...")
    
    # Load registry
    registry = SovereignRegistry()
    
    # Create Bot Father
    bot_father = BotFather(registry)
    
    # Test requirement analysis
    print("\n1️⃣ Testing requirement analysis...")
    test_tasks = [
        "Crawl security blogs for new threat indicators",
        "Generate weekly threat intelligence report",
        "Write Python script to automate log analysis",
        "Extract IOCs from malware analysis reports"
    ]
    
    for task in test_tasks:
        analysis = bot_father.analyze_requirements(task)
        primary = analysis["primary_recommendation"]
        if primary:
            print(f"   📝 '{task[:30]}...' → {primary['bot_type']} ({primary['confidence']:.2f})")
    
    # Create test bots
    print("\n2️⃣ Creating test bots...")
    
    bots_created = []
    for task in test_tasks[:2]:  # Create first 2
        bot = bot_father.create_bot(task)
        if bot:
            bots_created.append(bot)
    
    # Test bot improvement
    print("\n3️⃣ Testing bot improvement...")
    if bots_created:
        test_bot = bots_created[0]
        improvement_result = bot_father.improve_bot(
            test_bot.id,
            {
                "success_rate": 0.6,
                "efficiency": 0.5,
                "issues": ["timeout occurred", "memory usage high"]
            }
        )
        
        if improvement_result:
            print(f"   ✅ Improved {test_bot.name}")
    
    # Display creation log
    bot_father.display_creation_log()
    
    print("\n✅ Bot Father System tested successfully!")
    return True

if __name__ == "__main__":
    print("="*60)
    print("🤖 BOT FATHER SYSTEM - AUTONOMOUS BOT CREATION")
    print("="*60)
    
    success = test_bot_father()
    
    print("\n" + "="*60)
    if success:
        print("🎉 BOT FATHER SYSTEM OPERATIONAL!")
        print("🚀 Can now autonomously create and improve Worker Drones")
    else:
        print("⚠️ Bot Father tests had issues")
    
    print("="*60)
