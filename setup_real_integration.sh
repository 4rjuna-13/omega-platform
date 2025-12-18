#!/bin/bash
# Setup script for JAIDA-OMEGA-SAIOS Real Integration

echo "🚀 Setting up JAIDA-OMEGA-SAIOS Real Integration"
echo "================================================"

# Check Python version
echo "1. Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Create directory structure
echo "2. Creating directory structure..."
mkdir -p src/integration/real
mkdir -p data/web_crawler/intel
mkdir -p data/omega_nexus/alerts
mkdir -p data/omega_nexus/processed
mkdir -p logs
mkdir -p config

# Check virtual environment
echo "3. Checking virtual environment..."
if [ -f "venv/bin/activate" ]; then
    echo "✅ Virtual environment found"
    source venv/bin/activate
else
    echo "⚠️ No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "4. Installing dependencies..."
pip install --upgrade pip

# Core dependencies
pip install pyyaml sqlite3

# Optional dependencies for dashboard
echo "Optional: Install dashboard dependencies? (y/n)"
read -r install_dashboard
if [[ "$install_dashboard" =~ ^[Yy]$ ]]; then
    pip install dash plotly pandas
    echo "✅ Dashboard dependencies installed"
else
    echo "⚠️ Skipping dashboard dependencies"
fi

# Copy files
echo "5. Setting up integration files..."

# Check if files exist in current directory
if [ -f "src/integration/real/alert_processor.py" ]; then
    echo "✅ Alert processor already exists"
else
    echo "⚠️ Alert processor not found. Make sure to create it."
fi

if [ -f "src/integration/real/integration_manager.py" ]; then
    echo "✅ Integration manager already exists"
else
    echo "⚠️ Integration manager not found. Make sure to create it."
fi

if [ -f "config/integration.yaml" ]; then
    echo "✅ Integration config already exists"
else
    echo "⚠️ Integration config not found. Creating default..."
    cat > config/integration.yaml << 'CONFIG_EOF'
# Default integration configuration
alert_sources:
  demo_mode:
    enabled: true
    generate_test_alerts: true
    alert_interval: 10

processing:
  alert_threshold: 0.7
  filter_low_confidence: true

demo_mode:
  enabled: true
CONFIG_EOF
    echo "✅ Default config created"
fi

# Check database
echo "6. Checking database..."
if [ -f "data/sovereign.db" ]; then
    echo "✅ Database exists"
    
    # Check for required tables
    python3 << 'DB_CHECK_EOF'
import sqlite3
try:
    conn = sqlite3.connect('data/sovereign.db')
    cursor = conn.cursor()
    
    # Check for autonomous_decisions table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='autonomous_decisions'")
    if cursor.fetchone():
        print("✅ Autonomous decisions table exists")
    else:
        print("⚠️ Autonomous decisions table not found")
    
    conn.close()
except Exception as e:
    print(f"❌ Database check failed: {e}")
DB_CHECK_EOF
else
    echo "⚠️ Database not found. Run setup_fixed.sh first or create it."
fi

# Create test data
echo "7. Creating test data..."
cat > data/omega_nexus/alerts/test_alert.json << 'TEST_ALERT_EOF'
{
  "alert_id": "FILE-ALERT-001",
  "source": "file_test",
  "alert_type": "test_alert",
  "severity": 8,
  "confidence": 0.85,
  "description": "Test alert from file",
  "timestamp": "2024-01-01T12:00:00",
  "details": {
    "source_ip": "192.168.1.100",
    "target": "server-01",
    "threat_type": "test"
  }
}
TEST_ALERT_EOF

cat > data/web_crawler/intel/test_intel.json << 'TEST_INTEL_EOF'
{
  "intel_id": "INTEL-001",
  "source": "test_feed",
  "threat_type": "phishing_campaign",
  "severity": 7,
  "confidence": 0.75,
  "summary": "Test phishing campaign intelligence",
  "details": {
    "targets": ["financial sector"],
    "indicators": ["phishing-domain.com"],
    "first_seen": "2024-01-01"
  }
}
TEST_INTEL_EOF

echo "✅ Test data created"

# Make scripts executable
echo "8. Making scripts executable..."
chmod +x omega_nexus_real_integration.py 2>/dev/null || true
chmod +x test_real_integration.py 2>/dev/null || true

# Run quick test
echo "9. Running quick test..."
python3 << 'QUICK_TEST_EOF'
import sys
sys.path.insert(0, 'src')

try:
    # Try to import integration modules
    from integration.real.alert_processor import RealAlertProcessor
    print("✅ Alert processor imports successfully")
    
    # Create test processor
    processor = RealAlertProcessor()
    print("✅ Alert processor instantiated")
    
    # Get statistics
    stats = processor.get_statistics()
    print(f"✅ Processor status: {stats['processor_status']}")
    
    print("\n✅ All quick tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure the integration files are in src/integration/real/")
except Exception as e:
    print(f"❌ Test error: {e}")
QUICK_TEST_EOF

echo ""
echo "================================================"
echo "✅ SETUP COMPLETE"
echo ""
echo "🚀 Quick Start:"
echo "   python3 omega_nexus_real_integration.py demo"
echo ""
echo "🔧 Test Integration:"
echo "   python3 test_real_integration.py"
echo ""
echo "📊 Start Integration:"
echo "   python3 omega_nexus_real_integration.py start"
echo ""
echo "🛑 Stop Integration:"
echo "   python3 omega_nexus_real_integration.py stop"
echo ""
echo "📈 Dashboard (if installed):"
echo "   http://localhost:8050"
echo "================================================"
