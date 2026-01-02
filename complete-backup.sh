#!/bin/bash
# ========================
# COMPLETE BACKUP SYSTEM
# ========================

# Configuration
BACKUP_ROOT="$HOME/backups"
DAILY_DIR="$BACKUP_ROOT/daily/$(date +%Y-%m-%d)"
LOG_FILE="$BACKUP_ROOT/backup.log"
SYNC_DIRS=("$HOME/projects" "$HOME/workspace" "$HOME/config")

echo "==================================" >> "$LOG_FILE"
echo "BACKUP START: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"

# Create backup directory
mkdir -p "$DAILY_DIR"

# 1. Backup each directory
for dir in "${SYNC_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Backing up: $dir" >> "$LOG_FILE"
        cp -r "$dir" "$DAILY_DIR/" 2>&1 | head -5 >> "$LOG_FILE"
    fi
done

# 2. Clean old backups (keep 7 daily)
find "$BACKUP_ROOT/daily/" -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

# 3. Log disk usage
echo "Disk usage:" >> "$LOG_FILE"
df -h "$HOME" >> "$LOG_FILE"

# 4. Sync ChromeOS Downloads to workspace
if [ -d "/mnt/chromeos/MyFiles/Downloads" ]; then
    mkdir -p "$HOME/workspace/chromeos-sync"
    rsync -av --delete \
        /mnt/chromeos/MyFiles/Downloads/ \
        "$HOME/workspace/chromeos-sync/" \
        >> "$LOG_FILE" 2>&1
fi

# 5. Git operations (skip if no auth)
cd "$HOME"
if git add . >> "$LOG_FILE" 2>&1; then
    git commit -m "Auto-backup: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1
    # Try push but don't fail if auth issues
    git push origin main >> "$LOG_FILE" 2>&1 || echo "Git push failed (check auth)" >> "$LOG_FILE"
else
    echo "No changes to commit" >> "$LOG_FILE"
fi

echo "BACKUP COMPLETE: $(date)" >> "$LOG_FILE"
echo "==================================" >> "$LOG_FILE"

# Show summary
echo "Backup created at: $DAILY_DIR"
echo "Log file: $LOG_FILE"
