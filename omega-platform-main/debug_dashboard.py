import json

def analyze_dashboard_structure():
    print("🔍 Analyzing dashboard structure for bugs...")
    
    # Common bug patterns that cause 'int' has no len():
    bug_patterns = [
        "len(threat_score)",
        "len(ioc_count)", 
        "len(severity_level)",
        "len(confidence)",
        "len(return_value)",
        "len(data.get(",
        "len(result["
    ]
    
    # Read dashboard file
    try:
        with open('simple_threat_dashboard.py', 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
            print(f"📊 Dashboard file size: {len(content)} characters, {len(lines)} lines")
            
            # Look for len() calls
            len_calls = []
            for i, line in enumerate(lines, 1):
                if 'len(' in line and not line.strip().startswith('#'):
                    len_calls.append((i, line.strip()))
            
            if len_calls:
                print("\n🔎 Found len() calls (potential bug locations):")
                for line_num, line in len_calls:
                    print(f"  Line {line_num}: {line}")
                
                # Check each len() call context
                print("\n🔬 Checking context around len() calls:")
                for line_num, line in len_calls:
                    print(f"\n  --- Line {line_num} ---")
                    start = max(0, line_num - 3)
                    end = min(len(lines), line_num + 2)
                    for i in range(start, end):
                        prefix = ">>>" if i == line_num - 1 else "   "
                        print(f"{prefix} {i+1}: {lines[i]}")
            else:
                print("❌ No len() calls found in dashboard - check if imported module")
            
    except Exception as e:
        print(f"❌ Error reading dashboard: {e}")
    
    # Also check the test that's failing
    print("\n📋 Checking test suite for clues...")
    try:
        with open('test_all_components.py', 'r') as f:
            test_content = f.read()
            if 'test_threat_intelligence_dashboard' in test_content:
                # Extract that test function
                start = test_content.find('def test_threat_intelligence_dashboard')
                end = test_content.find('\n\n', start)
                test_func = test_content[start:end if end != -1 else len(test_content)]
                print(f"📝 Test function length: {len(test_func)} characters")
                
                # Look for what it's testing
                if 'dashboard' in test_func:
                    print("✅ Test function references dashboard")
    except Exception as e:
        print(f"⚠️ Couldn't analyze test: {e}")

if __name__ == "__main__":
    analyze_dashboard_structure()
