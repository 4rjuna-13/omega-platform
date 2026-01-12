#!/bin/bash
echo "🔄 Updating context with Sovereign Hierarchy..."

# Add hierarchy info to context
HIERARCHY_INFO="## 🏗️ NEW: SOVEREIGN HIERARCHY IMPLEMENTED
### **Files Added:**
- \`sovereign_hierarchy.py\` - Complete GC/WD hierarchy system
- \`test_sovereign_hierarchy.py\` - Integration tests

### **Key Components:**
1. **General Contractors (GC-class):** Compound intelligence systems
2. **Worker Drones (WD-class):** Singular task specialists  
3. **SovereignRegistry:** Persistent bot memory across sessions
4. **PartitionManager:** Temporary GC isolation for safety

### **Default GCs Created:**
- ✅ Bot Father Prime (GC-BOT-FATHER-001) - Highest authority
- ✅ Threat Modeler Alpha (GC-THREAT-MODELER-001)
- ✅ Web Crawler Command (GC-WEB-CRAWLER-001)

### **Next Integration Steps:**
1. Connect web crawler to GC-WEB-CRAWLER-001
2. Build Bot Father autonomous WD creation
3. Integrate dashboard with Threat Modeler GC
4. Add learning engine for continuous improvement"

# Update the context file
if [ -f JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md ]; then
    # Insert hierarchy info after architecture section
    sed -i "/## 🔐 ARCHITECTURE HIERARCHY/a $HIERARCHY_INFO" JAIDA_OMEGA_SAIOS_FULL_CONTEXT.md
    echo "✅ Context updated with Sovereign Hierarchy"
else
    echo "⚠️ Context file not found, running full update..."
    ./JAIDA_CONTEXT_SYSTEM.sh update
fi

echo ""
echo "🧪 Running hierarchy test..."
python3 sovereign_hierarchy.py 2>&1 | tail -20
