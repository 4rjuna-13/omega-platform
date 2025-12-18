#!/bin/bash
echo "🌐 Testing JAIDA Frontend Setup"
echo "================================"

echo "1. Checking Flask installation..."
python3 -c "import flask; print('✅ Flask installed')"

echo ""
echo "2. Testing dashboard imports..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from src.dashboard.web_app import app, get_db_connection
    print('✅ Dashboard module imports successfully')
    
    # Test database connection
    conn = get_db_connection()
    print('✅ Database connection works')
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "3. Checking directory structure..."
if [ -f "src/dashboard/web_app.py" ]; then
    echo "✅ Dashboard app exists"
else
    echo "❌ Dashboard app missing"
fi

if [ -f "src/dashboard/templates/index.html" ]; then
    echo "✅ HTML template exists"
else
    echo "❌ HTML template missing"
fi

echo ""
echo "================================"
echo "🎯 Frontend setup test complete!"
echo ""
echo "🚀 To start dashboard: ./scripts/dashboard-manage start"
echo "🌐 Then open: http://localhost:8080"
