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
