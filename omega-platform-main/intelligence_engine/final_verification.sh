#!/bin/bash
echo "🧪 JAIDA PLATFORM - FINAL VERIFICATION"
echo "======================================"

# Activate virtual environment if available
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
    echo "Virtual environment activated"
fi

echo "1. Checking file structure..."
ESSENTIAL_FILES=("otx_llm_pipeline_fixed.py" "optimized_analyst.py" "llm_analyst.py" "jaida_db.py")
missing=0
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        echo "  ✅ $file ($lines lines)"
    else
        echo "  ❌ $file (MISSING)"
        missing=1
    fi
done

if [ $missing -eq 1 ]; then
    echo "ERROR: Essential files missing!"
    exit 1
fi

echo ""
echo "2. Testing Python environment..."
python3 -c "
import sys
print('Python version:', sys.version[:6])
print('Executable:', sys.executable)
print('Virtual env:', 'venv' in sys.executable)
"

echo ""
echo "3. Testing Python imports..."
python3 -c "
try:
    import requests
    print('✅ requests module available')
    
    import sqlite3
    print('✅ sqlite3 module available')
    
    from llm_analyst import JAIDALLMAnalyst
    print('✅ llm_analyst imports OK')
    
    from optimized_analyst import OptimizedJAIDAAnalyst
    print('✅ optimized_analyst imports OK')
        
    # Test pipeline imports
    try:
        import otx_llm_pipeline_fixed
        print('✅ Pipeline imports OK')
    except Exception as e:
        print(f'⚠️  Pipeline import issue: {str(e)[:50]}')
        
except Exception as e:
    print(f'❌ Import failed: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo "4. Testing Ollama..."
# Simple Ollama test
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "✅ Ollama server responding"
else
    echo "⚠️  Ollama not responding (may need to start)"
    echo "   Run: ollama serve &"
    echo "   Then: sleep 5"
fi

echo ""
echo "5. Testing database..."
python3 jaida_db.py stats

echo ""
echo "6. Quick AI test..."
echo "   (Testing with 10-second timeout)"
timeout 10 python3 -c "
try:
    from llm_analyst import JAIDALLMAnalyst
    analyst = JAIDALLMAnalyst()
    test = {'name': 'verification test', 'description': 'test'}
    result = analyst.analyze_threat_intel(test)
    if 'classification' in result:
        print(f'✅ AI test passed: {result[\"classification\"]}')
        if 'cia_scores' in result:
            cia = result['cia_scores']
            print(f'   CIA: C={cia.get(\"confidentiality\", \"?\")}, ' +
                  f'I={cia.get(\"integrity\", \"?\")}, ' +
                  f'A={cia.get(\"availability\", \"?\")}')
        print(f'   Confidence: {result.get(\"confidence\", 0):.2f}')
    else:
        print('⚠️  AI returned unexpected format')
except Exception as e:
    print(f'⚠️  AI test failed: {str(e)[:50]}')
"

echo ""
echo "======================================"
echo "🎯 VERIFICATION COMPLETE"
echo ""
echo "To run full analysis:"
echo "  ./start_jaida.sh"
echo "  or"
echo "  python3 otx_llm_pipeline_fixed.py"
echo ""
echo "To check results:"
echo "  python3 jaida_db.py recent"
