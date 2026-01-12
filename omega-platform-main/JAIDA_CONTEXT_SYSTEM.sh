#!/bin/bash
# JAIDA Context System - One script for everything

case "$1" in
    "update")
        echo "🔄 Updating context..."
        
        # Get current test results
        TEST_RESULTS=$(python3 test_all_components.py 2>&1)
        
        # Create fresh context with updated results
        cat > JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md << CONTENT
# 🏛️ JAIDA-OMEGA-SAIOS UNIVERSAL CONTEXT
## 🚨 COPY EVERYTHING FROM HERE TO END FOR NEW CONVERSATIONS

## 📊 CURRENT BUILD STATUS - UPDATED: $(date)

### **Test Results:**
\`\`\`bash
$TEST_RESULTS
\`\`\`

### **Active Components:**
$(find . -name "*.py" -type f -exec ls -lh {} \; 2>/dev/null | head -10 | awk '{print "  • " $9 " (" $5 ")"}')

### **System Status:**
- **OMEGA_NEXUS**: OPERATIONAL
- **Test Success Rate**: $(echo "$TEST_RESULTS" | grep "Success Rate:" | sed 's/.*Success Rate: //' || echo "Unknown")
- **Last Update**: $(date)

## 🚀 QUICK COMMANDS
\`\`\`bash
# Update and view context
./JAIDA_CONTEXT_SYSTEM.sh update
./JAIDA_CONTEXT_SYSTEM.sh recall

# Use the nexus orchestrator
python3 omega_nexus.py status
python3 omega_nexus.py test

# Interactive mode
python3 omega_nexus.py
\`\`\`

## 🎯 NEXT ACTIONS
1. Run: \`python3 omega_nexus.py deploy\` - Deploy bot fleet
2. Run: \`python3 omega_nexus.py crawl\` - Execute web crawl
3. Run: \`python3 omega_nexus.py dashboard\` - Generate threat dashboard

---
**CONTEXT ID:** JAIDA-OMEGA-SAIOS-CTX-$(date +%Y%m%d-%H%M%S)
**LAST UPDATE:** $(date)
**STATUS:** OPERATIONAL
**RECALL:** ./JAIDA_CONTEXT_SYSTEM.sh recall
**UPDATE:** ./JAIDA_CONTEXT_SYSTEM.sh update

## 🚨 FOR NEW CONVERSATIONS:
COPY FROM \`# 🏛️ JAIDA-OMEGA-SAIOS UNIVERSAL CONTEXT\` TO END
CONTENT
        
        echo "✅ Context UPDATED with current test results"
        echo "📊 Test summary included"
        ;;
        
    "recall")
        echo "================================================================================"
        echo "🏛️  JAIDA-OMEGA-SAIOS CONTEXT"
        echo "================================================================================"
        echo ""
        echo "📋 COPY FROM LINE BELOW FOR NEW CONVERSATIONS:"
        echo ""
        cat JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md 2>/dev/null || {
            echo "⚠️ Context file not found. Run: ./JAIDA_CONTEXT_SYSTEM.sh update"
        }
        echo ""
        echo "================================================================================"
        echo "🔄 To update: ./JAIDA_CONTEXT_SYSTEM.sh update"
        ;;
        
    "test")
        echo "🧪 Running tests and updating context..."
        ./JAIDA_CONTEXT_SYSTEM.sh update
        ;;
        
    *)
        echo "JAIDA Context System"
        echo "Usage:"
        echo "  ./JAIDA_CONTEXT_SYSTEM.sh update   - Update context with current status"
        echo "  ./JAIDA_CONTEXT_SYSTEM.sh recall   - Display context for new conversations"
        echo "  ./JAIDA_CONTEXT_SYSTEM.sh test     - Run tests and update context"
        echo ""
        if [ -f JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md ]; then
            echo "Context file exists: $(stat -c %y JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md)"
        else
            echo "No context file found"
        fi
        ;;
esac
