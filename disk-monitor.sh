#!/bin/bash
# Disk Space Monitor for Linux Container
# Triggers backup at 85% usage (15% buffer)

CONTAINER_PATH="/"  # Monitor the root filesystem
TRIGGER_PERCENT=85.0

# Calculate current usage percentage
USAGE_PERCENT=$(df --output=pcent "$CONTAINER_PATH" | tail -1 | tr -d '% ')

echo "[$(date)] Current disk usage: ${USAGE_PERCENT}%"

# Compare using bash arithmetic (no external bc needed)
if (( USAGE_PERCENT >= TRIGGER_PERCENT )); then
    echo "[$(date)] ⚠️  Trigger threshold reached! Starting backup workflow..."
    # Execute the main backup script
    /home/_4rjuna13/scripts/backup-workflow.sh
else
    echo "[$(date)] ✓ Within safe limits"
fi
