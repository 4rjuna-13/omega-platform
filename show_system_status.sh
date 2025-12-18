#!/bin/bash
# Show JAIDA-OMEGA-SAIOS System Status

echo "================================================"
echo "🏛️ JAIDA-OMEGA-SAIOS SYSTEM STATUS"
echo "================================================"
echo ""

# Check modules
echo "📊 MODULE STATUS:"
python3 -c "
try:
    from simple_threat_dashboard import SimpleDashboard
    print('   ✅ Dashboard: Import successful')
except ImportError as e:
    print(f'   ❌ Dashboard: {e}')

try:
    from enterprise_platform_simple import SimpleOrchestrator
    print('   ✅ Enterprise: Import successful')
except ImportError as e:
    print(f'   ❌ Enterprise: {e}')
"

echo ""
echo "🧪 TEST STATUS:"
if python3 test_all_components.py 2>&1 | grep -q "ALL TESTS PASSED"; then
    echo "   ✅ All tests passing"
else
    echo "   ⚠️ Some tests failing"
fi

echo ""
echo "📁 CONTEXT SYSTEM:"
if [ -f JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md ]; then
    echo "   ✅ Context file exists ($(wc -l < JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md) lines)"
    echo "   📅 Last updated: $(stat -c %y JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md)"
else
    echo "   ❌ Context file missing"
fi

echo ""
echo "🚀 QUICK COMMANDS:"
echo "   ./JAIDA_CONTEXT_SYSTEM.sh recall   # Get context for new conversations"
echo "   ./JAIDA_CONTEXT_SYSTEM.sh update   # Update context with current status"
echo "   python3 test_all_components.py     # Run all tests"
echo "   ./show_system_status.sh           # Show this status"
echo ""

echo "================================================"
echo "💾 CONTEXT ID: $(grep -m1 'CONTEXT ID:' JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md 2>/dev/null | cut -d: -f2- | tr -d ' ' || echo 'Not available')"
echo "================================================"
