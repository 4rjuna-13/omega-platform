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
