#!/bin/bash
echo "🧹 Continuing JAIDA Cleanup & Restructuring..."
echo "=============================================="

# Complete the jaida-manage script
cat > scripts/jaida-manage << 'MANAGE_SCRIPT'
#!/bin/bash
# JAIDA Management Script

JAIDA_PID_FILE="/tmp/jaida.pid"
LOG_FILE="logs/jaida.log"

case "$1" in
    "start")
        echo "🚀 Starting JAIDA..."
        source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found"
        mkdir -p logs data
        
        # Stop any existing instance
        if [ -f "$JAIDA_PID_FILE" ]; then
            PID=$(cat "$JAIDA_PID_FILE")
            kill "$PID" 2>/dev/null || true
        fi
        
        # Start the system
        python3 jaida.py 2>&1 | tee "$LOG_FILE" &
        echo $! > "$JAIDA_PID_FILE"
        
        echo "✅ JAIDA started (PID: $(cat "$JAIDA_PID_FILE"))"
        echo "📝 Logs: tail -f $LOG_FILE"
        ;;
    
    "stop")
        echo "🛑 Stopping JAIDA..."
        
        if [ -f "$JAIDA_PID_FILE" ]; then
            PID=$(cat "$JAIDA_PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                echo "✅ Stopped JAIDA (PID: $PID)"
            else
                echo "⚠️  JAIDA process not running"
            fi
            rm -f "$JAIDA_PID_FILE"
        else
            # Try to find and kill any JAIDA processes
            PIDS=$(pgrep -f "python.*jaida" || true)
            if [ -n "$PIDS" ]; then
                kill $PIDS 2>/dev/null || true
                echo "✅ Stopped JAIDA processes"
            else
                echo "✅ No JAIDA processes found"
            fi
        fi
        ;;
    
    "status")
        echo "📊 JAIDA Status"
        echo "=============="
        
        if [ -f "$JAIDA_PID_FILE" ] && kill -0 $(cat "$JAIDA_PID_FILE") 2>/dev/null; then
            echo "✅ Running (PID: $(cat "$JAIDA_PID_FILE"))"
            echo ""
            echo "📈 Database Stats:"
            python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign_data.db')
    cursor = conn.cursor()
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
    tables = cursor.fetchall()
    print(f'   Tables: {len(tables)}')
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table[0]}')
        count = cursor.fetchone()[0]
        print(f'   - {table[0]}: {count} rows')
    conn.close()
except Exception as e:
    print(f'   ❌ Error: {e}')
"
        else
            echo "❌ Not running"
        fi
        
        echo ""
        echo "📁 Disk Usage:"
        du -h data/sovereign_data.db 2>/dev/null || echo "   Database not found"
        echo ""
        echo "📝 Latest Log:"
        tail -3 "$LOG_FILE" 2>/dev/null || echo "   No log file"
        ;;
    
    "dashboard")
        echo "📊 Starting Dashboard..."
        source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found"
        python3 -c "
import sys
sys.path.insert(0, 'src')
from dashboard.jaida_dashboard import JAIDADashboard
dashboard = JAIDADashboard()
dashboard.display_dashboard()
" &
        echo "✅ Dashboard started in background"
        echo "   Access logs: tail -f logs/jaida.log"
        ;;
    
    "logs")
        echo "📝 JAIDA Logs:"
        if [ -f "$LOG_FILE" ]; then
            tail -20 "$LOG_FILE"
        else
            echo "No log file found"
        fi
        ;;
    
    "clean")
        echo "🧹 Cleaning up..."
        ./scripts/jaida-manage stop
        rm -rf __pycache__ */__pycache__ */*/__pycache__
        rm -f logs/*.log
        echo "✅ Cleanup completed"
        ;;
    
    *)
        echo "JAIDA-Omega-SAIOS Management"
        echo ""
        echo "Usage: $0 {start|stop|status|dashboard|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  start     - Start JAIDA system"
        echo "  stop      - Stop JAIDA system"
        echo "  status    - Check system status"
        echo "  dashboard - Start web dashboard"
        echo "  logs      - Show recent logs"
        echo "  clean     - Clean cache and logs"
        ;;
esac
MANAGE_SCRIPT

chmod +x scripts/jaida-manage

# Move essential files to proper locations
echo "📦 Moving essential files..."

# Move Python files to src
mv jaida_enhanced_fixed.py src/core/jaida_core.py 2>/dev/null || true
mv real_data_adapter.py src/adapters/ 2>/dev/null || true
mv jaida_dashboard.py src/dashboard/ 2>/dev/null || true
mv production_logger.py src/core/ 2>/dev/null || true
mv config_manager.py src/core/ 2>/dev/null || true

# Move configuration
mkdir -p config
mv *.yaml config/ 2>/dev/null || true
mv .env config/ 2>/dev/null || true

# Move scripts
mv manage_jaida.sh scripts/ 2>/dev/null || true
mv check_status.sh scripts/ 2>/dev/null || true
mv verify_system.sh scripts/ 2>/dev/null || true

# Create main entry point
echo "🎯 Creating main entry point..."
cat > jaida.py << 'PYTHON'
#!/usr/bin/env python3
"""
🏛️ JAIDA-Omega-SAIOS - Main Entry Point
Version: 1.0.0
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_system():
    """Run the main JAIDA system"""
    from core.jaida_core import EnhancedJAIDA
    
    print("🤖 JAIDA-Omega-SAIOS Autonomous System")
    print("=" * 50)
    print("Starting enhanced threat detection engine...")
    
    jaida = EnhancedJAIDA()
    jaida.run()

def show_status():
    """Show system status"""
    from core.config_manager import config
    import sqlite3
    
    print("📊 JAIDA System Status")
    print("=" * 50)
    print(f"Environment: {config.environment}")
    print(f"Config loaded: {config.get('version', 'Unknown')}")
    
    # Database status
    db_path = config.get('database.path', 'data/sovereign_data.db')
    if os.path.exists(db_path):
        size = os.path.getsize(db_path) / 1024 / 1024
        print(f"Database: {db_path} ({size:.2f} MB)")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"Tables: {len(tables)}")
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")
    else:
        print("Database: Not found")
    
    print("\n✅ Status check complete")

def main():
    """Main entry point with command line interface"""
    parser = argparse.ArgumentParser(description="JAIDA-Omega-SAIOS Autonomous System")
    parser.add_argument('command', nargs='?', default='run', 
                       choices=['run', 'status', 'test', 'config'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_system()
    elif args.command == 'status':
        show_status()
    elif args.command == 'test':
        print("🧪 Running tests...")
        # Test imports
        try:
            import importlib
            modules = ['core.jaida_core', 'adapters.real_data_adapter', 
                      'dashboard.jaida_dashboard', 'core.config_manager']
            for module in modules:
                importlib.import_module(module)
                print(f"✅ {module}")
            print("\n✅ All imports successful")
        except ImportError as e:
            print(f"❌ Import error: {e}")
    elif args.command == 'config':
        from core.config_manager import config
        import json
        print(json.dumps(config.config, indent=2, default=str))

if __name__ == "__main__":
    main()
PYTHON

chmod +x jaida.py

# Create a simple requirements check
cat > check_environment.sh << 'ENV_CHECK'
#!/bin/bash
echo "🔍 Checking JAIDA Environment"
echo "============================="

# Check Python
echo "Python: $(python3 --version 2>/dev/null || echo 'Not found')"

# Check virtual environment
if [ -d "venv" ]; then
    echo "✅ Virtual environment exists"
    source venv/bin/activate
    echo "Python path: $(which python3)"
else
    echo "⚠️  No virtual environment"
fi

# Check dependencies
echo ""
echo "Dependencies:"
python3 -c "
import sys
deps = [
    ('pandas', 'Data analysis'),
    ('flask', 'Web framework'),
    ('pyyaml', 'Config parsing'),
    ('prometheus_client', 'Metrics'),
    ('sqlite3', 'Database')
]

for module, desc in deps:
    try:
        __import__(module)
        print(f'  ✅ {module:20} - {desc}')
    except ImportError:
        print(f'  ❌ {module:20} - {desc} (missing)')
"

# Check directory structure
echo ""
echo "Directory Structure:"
ls -la | grep -E "^(src|config|data|logs|scripts|tests)" || echo "  Some directories missing"

echo ""
echo "============================="
ENV_CHECK

chmod +x check_environment.sh
mv check_environment.sh scripts/

# Clean up old files
echo "🗑️  Cleaning up old files..."
rm -f \
    '=' \
    '🏛️' \
    '0' '30' '5' '50' '70' \
    'hour_ago]' \
    'recent_cutoff]' \
    'self.resource_limits[disk_quota_mb]' \
    *.tmp *.bak *.backup \
    2>/dev/null || true

# Remove broken files
rm -f \
    fix_*.py \
    update_context_*.sh \
    start_jaida_properly.sh \
    jaida_simple_working.py \
    unified_orchestrator_simple.py \
    omega_nexus_*.py.backup \
    deploy_production*.sh \
    integrate_real_data.sh \
    2>/dev/null || true

# Remove empty files
find . -maxdepth 1 -type f -size 0 -delete 2>/dev/null || true

# Clean up __pycache__
echo "🧹 Cleaning Python cache..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Final organization
echo "📋 Final organization..."

# Ensure essential directories exist
mkdir -p logs data backups

# Create a .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'GITIGNORE'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/*.log
*.log

# Backups
backups/*
*.bak

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temp
tmp/
temp/
GITIGNORE
fi

# Create a simple test
cat > tests/test_basic.py << 'TEST'
#!/usr/bin/env python3
"""
Basic tests for JAIDA-Omega-SAIOS
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestImports(unittest.TestCase):
    """Test that all modules can be imported"""
    
    def test_core_imports(self):
        """Test core module imports"""
        try:
            import core.jaida_core
            import core.config_manager
            import core.production_logger
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_adapter_imports(self):
        """Test adapter imports"""
        try:
            import adapters.real_data_adapter
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_database(self):
        """Test database connection"""
        import sqlite3
        try:
            conn = sqlite3.connect('data/sovereign_data.db')
            conn.close()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Database test failed: {e}")

if __name__ == '__main__':
    unittest.main()
TEST

echo ""
echo "=============================================="
echo "🎉 CLEANUP COMPLETED SUCCESSFULLY!"
echo ""
echo "📁 NEW STRUCTURE:"
echo "  src/core/        - Core system components"
echo "  src/adapters/    - Data source adapters"
echo "  src/dashboard/   - Monitoring dashboard"
echo "  config/          - Configuration files"
echo "  data/            - Database files"
echo "  logs/            - System logs"
echo "  scripts/         - Management scripts"
echo "  tests/           - Test suites"
echo ""
echo "🚀 QUICK START:"
echo "  1. Check environment: ./scripts/check_environment.sh"
echo "  2. Start JAIDA: ./scripts/jaida-manage start"
echo "  3. Check status: ./scripts/jaida-manage status"
echo "  4. View logs: ./scripts/jaida-manage logs"
echo "  5. Stop: ./scripts/jaida-manage stop"
echo ""
echo "📦 Backup created at: $BACKUP_DIR"
echo "=============================================="
