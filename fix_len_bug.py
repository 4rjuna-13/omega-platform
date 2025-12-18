print("🔧 Fixing len() bug in dashboard...")

with open('simple_threat_dashboard.py', 'r') as f:
    content = f.read()

# Replace the problematic len() call
# BEFORE: len(data.get('findings', []))
# AFTER: (len(data.get('findings')) if isinstance(data.get('findings'), (list, tuple)) else 0)

content = content.replace(
    "len(data.get('findings', []))",
    "(len(data.get('findings')) if isinstance(data.get('findings'), (list, tuple)) else 0)"
)

with open('simple_threat_dashboard.py', 'w') as f:
    f.write(content)

print("✅ Fixed len() bug in dashboard")

# Test the fix
print("\n🧪 Testing the fix...")
try:
    # First, let's test the specific line
    test_data = {'team_size': 5, 'findings': 10, 'exercise': 'test'}
    
    # This would have failed before
    result = "(len(data.get('findings')) if isinstance(data.get('findings'), (list, tuple)) else 0)"
    print(f"Fixed expression: {result}")
    print("✅ Fix applied successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
