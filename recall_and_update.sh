#!/bin/bash
# This script UPDATES context with current status, THEN recalls it

echo "🔄 Updating context with current build status..."
echo ""

# Run tests and capture output
TEST_OUTPUT=$(python3 test_all_components.py 2>&1)

# Extract test summary
SUMMARY=$(echo "$TEST_OUTPUT" | grep -A5 "TEST SUMMARY:")

# Update the context file with current test results
sed -i "/### \*\*Last Test Status:\*\*/,/^\`\`\`/d" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md

# Find where to insert new test status
LINE_NUM=$(grep -n "### \*\*Last Test Status:\*\*" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md | cut -d: -f1)
if [ -z "$LINE_NUM" ]; then
    # If not found, add after Current Bug section
    LINE_NUM=$(grep -n "### \*\*Current Bug:\*\*" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md | cut -d: -f1)
    LINE_NUM=$((LINE_NUM + 6))
fi

# Insert new test status
{
    head -n $((LINE_NUM-1)) JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md
    echo ""
    echo "### **Last Test Status:**"
    echo "\`\`\`bash"
    echo "$TEST_OUTPUT" | tail -30
    echo "\`\`\`"
    tail -n +$LINE_NUM JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md
} > JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.tmp
mv JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.tmp JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md

# Update timestamp
sed -i "s|CONTEXT ID:.*|CONTEXT ID: JAIDA-OMEGA-SAIOS-CTX-$(date +%Y%m%d-%H%M%S)|" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md
sed -i "s|GENERATED:.*|GENERATED: $(date)|" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md

echo "✅ Context updated with latest test results: $(date)"
echo ""

# Now recall the updated context
echo "================================================================================"
echo "🏛️  JAIDA-OMEGA-SAIOS FULL CONTEXT (UPDATED)"
echo "================================================================================"
echo ""
echo "📋 COPY FROM LINE BELOW FOR NEW CONVERSATIONS:"
echo ""
cat JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md
echo ""
echo "================================================================================"
echo "🔄 Context UPDATED at: $(date)"
echo "📊 Test status: $SUMMARY" | head -2
