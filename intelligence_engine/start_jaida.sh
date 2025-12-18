#!/bin/bash
echo "🚀 Starting JAIDA Platform..."
echo ""

# 1. Activate virtual environment
echo "1. Activating virtual environment..."
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found at ../venv/"
    echo "   Running without virtual environment..."
fi

# 2. Start Ollama if not running
echo "2. Checking Ollama..."
if ! curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "   Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    sleep 8
    echo "   ✅ Ollama started"
else
    echo "   ✅ Ollama already running"
fi

# 3. Verify Python environment
echo "3. Verifying Python environment..."
python3 -c "
import sys
print(f'   Python: {sys.version[:6]}')
print(f'   Executable: {sys.executable}')

try:
    import requests
    print(f'   ✅ requests: {requests.__version__}')
except:
    print('   ❌ requests module missing')

try:
    import sqlite3
    print(f'   ✅ sqlite3: {sqlite3.sqlite_version}')
except:
    print('   ❌ sqlite3 module missing')
"

# 4. Run pipeline
echo ""
echo "4. Running JAIDA threat analysis..."
python3 otx_llm_pipeline_fixed.py

# 5. Show results
echo ""
echo "5. Analysis complete! Results:"
python3 jaida_db.py recent

echo ""
echo "🎉 JAIDA Platform execution complete!"
echo ""
echo "Quick commands:"
echo "  python3 otx_llm_pipeline_fixed.py    # Run analysis"
echo "  python3 jaida_db.py recent           # Show recent analyses"
echo "  python3 jaida_db.py stats            # Show statistics"
