#!/bin/bash
echo "=== SYSTEM CLEANUP ==="
echo "Cleaning temporary files..."

# Remove Python cache
find ~ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find ~ -name "*.pyc" -delete

# Clean backup logs older than 30 days
find ~/backups -name "*.log" -mtime +30 -delete

# Remove empty directories
find ~/workspace -type d -empty -delete
find ~/projects -type d -empty -delete

# Optimize Git
git gc --prune=now 2>/dev/null

echo "Cleanup complete!"
echo "Disk space before:"
df -h ~/ | tail -1
