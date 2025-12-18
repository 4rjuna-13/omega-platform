#!/bin/bash
# JAIDA-OMEGA-SAIOS Setup Script
# Proper structured setup

set -e  # Exit on error

echo "🏛️ JAIDA-OMEGA-SAIOS - Structured Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

check_prerequisite() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

check_prerequisite python3
check_prerequisite sqlite3

# Check Python version without bc
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Python version: $PYTHON_VERSION"

# Simple Python version check
if [[ "$PYTHON_VERSION" =~ ^3\.[0-9]+$ ]]; then
    MAJOR=3
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ $MINOR -ge 8 ]; then
        print_success "Python $PYTHON_VERSION (>= 3.8)"
    else
        print_error "Python $PYTHON_VERSION (< 3.8)"
        echo "Python 3.8 or higher is required"
        exit 1
    fi
else
    print_error "Invalid Python version format: $PYTHON_VERSION"
    exit 1
fi

# Create directory structure
print_status "Creating directory structure..."
mkdir -p src/core src/autonomous src/integration src/utils
mkdir -p data config tests docs logs scripts

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install pyyaml

# Initialize database
print_status "Initializing database..."
python3 -c "
import sqlite3
import json
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
"

# Create configuration files
print_status "Creating configuration files..."

# Main configuration
cat > config/system.yaml << 'CONFIG_EOF'
# JAIDA-OMEGA-SAIOS Configuration
version: "2.0-autonomous"

system:
  name: "JAIDA-OMEGA-SAIOS"
  mode: "autonomous"  # autonomous, manual, hybrid
  log_level: "INFO"
  
database:
  path: "data/sovereign.db"
  backup_interval: 3600  # seconds
  max_backups: 10

autonomous:
  enabled: true
  decision_confidence_threshold: 0.7
  max_pending_decisions: 50
  execution_interval: 60  # seconds
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
  api_rate_limit: 100  # requests per minute
CONFIG_EOF

# Autonomous engine configuration
cat > config/autonomous.yaml << 'CONFIG_EOF'
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
CONFIG_EOF

print_success "Configuration files created"

# Create __init__.py files
print_status "Creating Python package files..."
touch src/__init__.py
touch src/core/__init__.py
touch src/autonomous/__init__.py
touch src/integration/__init__.py
touch src/utils/__init__.py

# Create a simplified main orchestrator first
cat > jaida.py << 'EOF'
#!/usr/bin/env python3
"""
🏛️ JAIDA-OMEGA-SAIOS Main Entry Point
Simplified version for initial setup
"""

import sys
import os
import argparse

print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                  🏛️ JAIDA-OMEGA-SAIOS                   ║
    ║            Autonomous Cybersecurity Platform             ║
    ║                     v2.0 - Structured                    ║
    ╚══════════════════════════════════════════════════════════╝
""")

def check_system():
    """Check system status"""
    print("🔍 Checking system...")
    
    # Check database
    if os.path.exists("data/sovereign.db"):
        print("✅ Database: Found")
    else:
        print("❌ Database: Not found")
    
    # Check config
    if os.path.exists("config/system.yaml"):
        print("✅ Configuration: Found")
    else:
        print("❌ Configuration: Not found")
    
    print("\n📋 Setup completed successfully!")
    print("   Run './setup.sh' if you need to recreate the system")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['status', 'help'])
    args = parser.parse_args()
    
    if args.command == 'status':
        check_system()
    elif args.command == 'help':
        print("""
Available commands:
  status - Check system status
  help   - Show this help
  
Run './setup.sh' to initialize the system first.
        """)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        check_system()
    else:
        main()
