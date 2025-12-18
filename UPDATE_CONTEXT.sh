#!/bin/bash
# Auto-update context for new conversations
./JAIDA_CONTEXT_SYSTEM.sh update
echo "Context updated at: $(date)"
cp OMEGA_JAIDA_SAIOS_FULL_CONTEXT.txt ~/context_backup_$(date +%Y%m%d_%H%M%S).txt
