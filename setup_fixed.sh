#!/bin/bash
# JAIDA-OMEGA-SAIOS Setup Script
# Fixed version

set -e  # Exit on error

echo "🏛️ JAIDA-OMEGA-SAIOS - Structured Setup"
echo "======================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[*]${NC} $1"; }
print_success() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

# Check prerequisites
print_status "Checking prerequisites..."

if command -v python3 &> /dev/null; then
    print_success "python3 is installed"
else
    print_error "python3 is not installed"
    exit 1
fi

if command -v sqlite3 &> /dev/null; then
    print_success "sqlite3 is installed"
else
    print_error "sqlite3 is not installed"
    exit 1
fi

# Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ $MAJOR -eq 3 ] && [ $MINOR -ge 8 ]; then
    print_success "Python $PYTHON_VERSION (>= 3.8)"
else
    print_error "Python $PYTHON_VERSION (< 3.8)"
    exit 1
fi

# Create directory structure
print_status "Creating directory structure..."
mkdir -p src/core src/autonomous src/integration src/utils
mkdir -p data config tests docs logs scripts

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
print_success "Virtual environment created"

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install pyyaml

# Initialize database
print_status "Initializing database..."
python3 << 'PYTHON_EOF'
import sqlite3
import os

db_path = 'data/sovereign.db'

# Create database with basic tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# System status table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT NOT NULL,
        status TEXT NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    )
''')

# Autonomous decisions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS autonomous_decisions (
        decision_id TEXT PRIMARY KEY,
        action TEXT NOT NULL,
        reason TEXT NOT NULL,
        confidence REAL NOT NULL,
        priority INTEGER NOT NULL,
        parameters TEXT NOT NULL,
        expected_outcome TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        executed BOOLEAN DEFAULT FALSE,
        result TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Threat intelligence table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS threat_intel (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        indicator TEXT NOT NULL,
        threat_type TEXT NOT NULL,
        confidence REAL NOT NULL,
        severity INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        context TEXT NOT NULL,
        processed BOOLEAN DEFAULT FALSE
    )
''')

# Insert initial system status
cursor.execute('''
    INSERT OR REPLACE INTO system_status (component, status, details)
    VALUES (?, ?, ?)
''', ('system', 'initializing', 'System is being initialized'))

conn.commit()
conn.close()

print(f'Database initialized at {db_path}')
PYTHON_EOF

# Create configuration files
print_status "Creating configuration files..."

# Main configuration
cat > config/system.yaml << 'CONFIG_EOF'
# JAIDA-OMEGA-SAIOS Configuration
version: "2.0-autonomous"

system:
  name: "JAIDA-OMEGA-SAIOS"
  mode: "autonomous"
  log_level: "INFO"
  
database:
  path: "data/sovereign.db"
  backup_interval: 3600
  max_backups: 10

autonomous:
  enabled: true
  decision_confidence_threshold: 0.7
  max_pending_decisions: 50
  execution_interval: 60
  learning_enabled: true

modules:
  core_orchestrator: true
  autonomous_engine: true
  bot_father: true
  web_crawler: true
  deception_tech: true
  sovereign_db: true

security:
  encryption_enabled: true
  authentication_required: false
  api_rate_limit: 100
CONFIG_EOF

# Autonomous engine configuration
cat > config/autonomous.yaml << 'AUTONOMOUS_CONFIG_EOF'
# Autonomous Decision Engine Configuration

decision_weights:
  malware:
    deploy_bots: 0.9
    isolate_threat: 0.8
    activate_honeypot: 0.6
  phishing:
    activate_honeypot: 0.8
    gather_intel: 0.7
    escalate_intel: 0.6
  ddos:
    deploy_bots: 0.9
    adapt_config: 0.7
    isolate_threat: 0.8
  zero_day:
    escalate_intel: 0.9
    gather_intel: 0.8
    counter_measure: 0.7

response_templates:
  deploy_bots:
    low: {count: 3, type: "monitor", priority: 1}
    medium: {count: 5, type: "defender", priority: 2}
    high: {count: 10, type: "defender", priority: 3}
    critical: {count: 20, type: "aggressive", priority: 5}
  
  activate_honeypot:
    low: {level: "basic", deception: "static"}
    medium: {level: "interactive", deception: "dynamic"}
    high: {level: "advanced", deception: "adaptive"}
    critical: {level: "aggressive", deception: "deceptive"}

threat_scoring:
  severity_weights:
    suspicious: 0.3
    malicious: 0.6
    critical: 0.9
  
  confidence_multiplier: 1.2
  recency_decay_hours: 24
AUTONOMOUS_CONFIG_EOF

print_success "Configuration files created"

# Create Python package files
print_status "Creating Python package files..."
touch src/__init__.py
touch src/core/__init__.py
touch src/autonomous/__init__.py
touch src/integration/__init__.py
touch src/utils/__init__.py

# Create core orchestrator
cat > src/core/orchestrator.py << 'ORCHESTRATOR_EOF'
#!/usr/bin/env python3
"""
🏛️ Core Orchestrator - JAIDA-OMEGA-SAIOS
"""

import sys
import os
import yaml
import sqlite3
from datetime import datetime

class SystemOrchestrator:
    """Main system orchestrator"""
    
    def __init__(self, config_path="config/system.yaml"):
        self.config = self.load_config(config_path)
        self.db_path = self.config.get('database', {}).get('path', 'data/sovereign.db')
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return {}
    
    def check_system_health(self):
        """Check health of system components"""
        health_report = {
            'timestamp': datetime.now().isoformat(),
            'components': {},
            'overall_health': 'healthy'
        }
        
        # Check database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            if tables:
                health_report['components']['database'] = {
                    'status': 'healthy',
                    'details': f"{len(tables)} tables found"
                }
            else:
                health_report['components']['database'] = {
                    'status': 'degraded',
                    'details': 'No tables found'
                }
                health_report['overall_health'] = 'degraded'
                
        except Exception as e:
            health_report['components']['database'] = {
                'status': 'error',
                'details': str(e)
            }
            health_report['overall_health'] = 'error'
        
        # Check configuration
        if self.config:
            health_report['components']['configuration'] = {
                'status': 'healthy',
                'details': 'Configuration loaded successfully'
            }
        else:
            health_report['components']['configuration'] = {
                'status': 'error',
                'details': 'Failed to load configuration'
            }
            health_report['overall_health'] = 'error'
        
        return health_report
    
    def get_system_status(self):
        """Get current system status from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT component, status, last_updated, details 
                FROM system_status 
                ORDER BY last_updated DESC
            ''')
            
            status = {}
            for row in cursor.fetchall():
                component, status_val, last_updated, details = row
                status[component] = {
                    'status': status_val,
                    'last_updated': last_updated,
                    'details': details
                }
            
            conn.close()
            return status
        except Exception as e:
            print(f"Failed to get system status: {e}")
            return {}

def main():
    """Test the orchestrator"""
    print("Testing System Orchestrator...")
    
    orchestrator = SystemOrchestrator()
    health = orchestrator.check_system_health()
    
    print(f"\nSystem Health: {health['overall_health'].upper()}")
    print(f"Timestamp: {health['timestamp']}")
    
    print("\nComponent Status:")
    for component, info in health['components'].items():
        status_icon = '✅' if info['status'] == 'healthy' else '⚠️ ' if info['status'] == 'degraded' else '❌'
        print(f"  {status_icon} {component}: {info['status']}")
        if info['details']:
            print(f"      Details: {info['details']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
ORCHESTRATOR_EOF

chmod +x src/core/orchestrator.py

# Create autonomous engine
cat > src/autonomous/engine.py << 'ENGINE_EOF'
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
ENGINE_EOF

chmod +x src/autonomous/engine.py

# Create main entry point
cat > jaida.py << 'MAIN_EOF'
#!/usr/bin/env python3
"""
🏛️ JAIDA-OMEGA-SAIOS Main Entry Point
"""

import sys
import os
import argparse

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                  🏛️ JAIDA-OMEGA-SAIOS                   ║
    ║            Autonomous Cybersecurity Platform             ║
    ║                     v2.0 - Structured                    ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def command_status():
    """Display system status"""
    print_banner()
    
    # Add src to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from core.orchestrator import SystemOrchestrator
        
        orchestrator = SystemOrchestrator()
        health = orchestrator.check_system_health()
        status = orchestrator.get_system_status()
        
        print("\n" + "="*70)
        print("📊 SYSTEM STATUS REPORT")
        print("="*70)
        
        print(f"\nOverall Health: {health['overall_health'].upper()}")
        
        print("\n🔧 Component Health:")
        for component, info in health['components'].items():
            status_icon = '✅' if info['status'] == 'healthy' else '⚠️ ' if info['status'] == 'degraded' else '❌'
            print(f"  {status_icon} {component}: {info['status']}")
        
        print("\n📈 System Status:")
        for component, info in status.items():
            status_icon = '✅' if info['status'] == 'running' else '⚠️ ' if info['status'] == 'degraded' else '❌'
            print(f"  {status_icon} {component}: {info['status']}")
            if info['details']:
                print(f"      Details: {info['details']}")
        
        print("\n" + "="*70)
        return 0
        
    except ImportError as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure you ran ./setup.sh first")
        return 1

def command_test():
    """Test system components"""
    print_banner()
    print("\n🧪 Testing system components...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        # Test orchestrator
        print("\n1. Testing Orchestrator...")
        from core.orchestrator import main as test_orchestrator
        test_orchestrator()
        
        # Test autonomous engine
        print("\n2. Testing Autonomous Engine...")
        from autonomous.engine import test_engine
        test_engine()
        
        print("\n✅ All tests completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1

def command_demo():
    """Run demonstration"""
    print_banner()
    print("\n🎬 JAIDA-OMEGA-SAIOS Demonstration")
    print("="*70)
    
    steps = [
        ("System Status", command_status),
        ("System Test", command_test)
    ]
    
    for i, (step_name, step_func) in enumerate(steps, 1):
        print(f"\n{i}. {step_name}")
        print("-"*40)
        step_func()
    
    print("\n" + "="*70)
    print("🎉 Demonstration completed!")
    print("="*70)
    return 0

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="JAIDA-OMEGA-SAIOS - Autonomous Cybersecurity Platform"
    )
    
    parser.add_argument(
        'command',
        choices=['status', 'test', 'demo', 'help'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    try:
        if args.command == 'status':
            return command_status()
        elif args.command == 'test':
            return command_test()
        elif args.command == 'demo':
            return command_demo()
        elif args.command == 'help':
            print_help()
            return 0
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

def print_help():
    """Print help information"""
    print_banner()
    print("""
📋 AVAILABLE COMMANDS:

  status      - Display comprehensive system status
  test        - Test system components
  demo        - Run comprehensive demonstration
  help        - Show this help message

🎯 EXAMPLES:

  ./jaida.py status
  ./jaida.py test
  ./jaida.py demo

📁 PROJECT STRUCTURE:

  src/              - Source code
    core/           - Core orchestrator
    autonomous/     - Autonomous decision engine
  
  data/             - Database and persistent data
  config/           - Configuration files
  tests/            - Test files
  docs/             - Documentation
  logs/             - System logs
""")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print_help()
    else:
        sys.exit(main())
MAIN_EOF

chmod +x jaida.py

# Create quick test
cat > test_quick.sh << 'TEST_EOF'
#!/bin/bash
# Quick test script

echo "🧪 Quick System Test"
echo "==================="

echo "1. Checking files..."
if [ -f "jaida.py" ]; then
    echo "✅ jaida.py found"
else
    echo "❌ jaida.py missing"
    exit 1
fi

echo "2. Checking database..."
if [ -f "data/sovereign.db" ]; then
    echo "✅ Database found"
else
    echo "❌ Database missing"
    exit 1
fi

echo "3. Checking configuration..."
if [ -f "config/system.yaml" ]; then
    echo "✅ Configuration found"
else
    echo "❌ Configuration missing"
    exit 1
fi

echo "4. Testing Python import..."
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from core.orchestrator import SystemOrchestrator
    print('✅ Python imports working')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

echo ""
echo "✅ Quick test passed!"
echo ""
echo "📋 Next: ./jaida.py status"
TEST_EOF

chmod +x test_quick.sh

print_success "Fixed setup script created!"
print_success "All files created successfully!"

echo ""
echo "📋 To complete setup:"
echo "   1. Run the fixed setup: ./setup_fixed.sh"
echo "   2. Test the system: ./test_quick.sh"
echo "   3. Check status: ./jaida.py status"
echo ""
echo "Note: This creates a clean, working version without heredoc issues."
