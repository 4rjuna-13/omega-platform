#!/bin/bash
echo "🔄 Updating context with current build status..."

# Create a backup
cp JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.backup

# Create new file with updated test results
{
    # Copy everything until test status
    sed -n '1,/### \*\*Last Test Status:\*\*/p' JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md | head -n -1
    
    echo "### **Last Test Status:**"
    echo "\`\`\`bash"
    python3 test_all_components.py 2>&1
    echo "\`\`\`"
    
    # Skip old test status and continue from after it
    sed -n '/^\`\`\`$/,${n;:a;n;/### \*\*Key Files:\*\*/{p;q};p;ba}' JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md
} > JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.new

# Update IDs and timestamp
sed -i "s|CONTEXT ID:.*|CONTEXT ID: JAIDA-OMEGA-SAIOS-CTX-$(date +%Y%m%d-%H%M%S)|" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.new
sed -i "s|GENERATED:.*|GENERATED: $(date)|" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.new

mv JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md.new JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md

echo "✅ Context updated!"
echo "📊 Run: ./recall_full_context.sh to see updated context"
