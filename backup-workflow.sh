#!/bin/bash
# Main Backup Workflow Script
LOG_FILE="/home/_4rjuna13/backup.log"
DOWNLOADS_PATH="/mnt/chromeos/MyFiles/Downloads"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== BACKUP WORKFLOW STARTED: ${TIMESTAMP} ===" >> "$LOG_FILE"

# 1. GitHub Commit
echo "[${TIMESTAMP}] Step 1: Committing to GitHub..." >> "$LOG_FILE"
cd /home/_4rjuna13

# Clean pycache before committing
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

if git add . >> "$LOG_FILE" 2>&1; then
    git commit -m "Auto-backup: ${TIMESTAMP}" >> "$LOG_FILE" 2>&1
    # Push with stored credentials (set up git credential helper first)
    git push origin main >> "$LOG_FILE" 2>&1
else
    echo "[${TIMESTAMP}] No changes to commit" >> "$LOG_FILE"
fi

# 2. Context System Update (PLACEHOLDER - Define your command)
echo "[${TIMESTAMP}] Step 2: Updating context system..." >> "$LOG_FILE"
# Example: python3 ~/update_context.py >> "$LOG_FILE" 2>&1

# 3. Google Drive Sync (Manual step for now)
echo "[${TIMESTAMP}] Step 3: Manual Drive sync required" >> "$LOG_FILE"
echo "  Use ChromeOS Files app to sync ~/projects to Google Drive" >> "$LOG_FILE"

# 4. Cleanup old Downloads (files older than 3 days)
echo "[${TIMESTAMP}] Step 4: Cleaning up old downloads..." >> "$LOG_FILE"
find "$DOWNLOADS_PATH" -type f -mtime +3 -delete 2>/dev/null

echo "[${TIMESTAMP}] Workflow completed." >> "$LOG_FILE"
echo "=== WORKFLOW ENDED ===" >> "$LOG_FILE"
