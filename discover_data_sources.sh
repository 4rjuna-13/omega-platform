#!/bin/bash
echo "🔍 Discovering Available Data Sources..."

# 1. Check for existing data connectors
echo "### Existing Connectors:"
find . -name "*api*.py" -o -name "*data*.py" -o -name "*source*.py" | head -10

# 2. Check database contents
echo -e "\n### Database Structure:"
python3 -c "
import sqlite3
conn = sqlite3.connect('sovereign_data.db')
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
tables = cursor.fetchall()
print(f'Tables: {len(tables)}')
for table in tables:
    cursor.execute(f\"PRAGMA table_info({table[0]});\")
    cols = cursor.fetchall()
    print(f'  {table[0]}: {len(cols)} columns')
conn.close()
"

# 3. Check for data files
echo -e "\n### Data Files:"
find . -name "*.json" -o -name "*.csv" -o -name "*.log" | head -15

# 4. Check network/API capabilities
echo -e "\n### API/Network Modules:"
grep -l "requests\|http\|api\|socket" *.py | head -10
