#!/bin/bash
clear
echo "=================================================="
echo "           OMEGA PLATFORM DASHBOARD"
echo "=================================================="
echo "Time: $(date)"
echo "User: $(whoami)"
echo "Chromebook: $(uname -a | cut -d' ' -f13)"
echo ""

# System Status
echo "=== SYSTEM STATUS ==="
echo "• Disk: $(df -h ~/ | tail -1 | awk '{print $4 " free (" $5 " used)"}')"
echo "• Memory: $(free -h | awk '/^Mem:/ {print $3 " / " $2 " (" $3/$2*100 "%%)"}')"
echo "• Backups: $(find ~/backups -type f 2>/dev/null | wc -l) files"
echo "• Projects: $(find ~/projects -type f \( -name "*.py" -o -name "*.sh" -o -name "*.md" \) | wc -l) files"
echo ""

# GitHub Status
echo "=== GITHUB STATUS ==="
if git remote -v 2>/dev/null | grep -q "origin"; then
    echo "• Remote: $(git remote get-url origin | cut -d'/' -f4-5)"
    # Test connection
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo "• SSH: ✅ Connected"
    else
        echo "• SSH: ❌ Not connected"
    fi
    echo "• Changes: $(git status --short 2>/dev/null | wc -l) uncommitted"
else
    echo "• Remote: ❌ Not configured"
fi
echo ""

# Recent Backups
echo "=== RECENT BACKUPS ==="
if [ -d ~/backups/daily ]; then
    ls -lt ~/backups/daily/ 2>/dev/null | head -3 | awk '{print "• "$6" "$7" "$8" - "$9}'
else
    echo "• No backups found"
fi
echo ""

# Services Status
echo "=== SERVICES ==="
if systemctl --user list-timers 2>/dev/null | grep -q backup.timer; then
    echo "• Backup timer: ✅ Active"
    systemctl --user list-timers --no-pager 2>/dev/null | grep backup | awk '{print "• Next: "$1" "$2" "$3}'
else
    echo "• Backup timer: ❌ Inactive"
fi
echo ""

# Quick Actions
echo "=== QUICK ACTIONS ==="
echo "[1] Run backup now        [2] Fix GitHub auth"
echo "[3] Check logs            [4] Push to GitHub"
echo "[5] Update dashboard      [6] System cleanup"
echo ""
echo "Enter choice (1-6) or press Enter to refresh: "
read -t 5 choice
case $choice in
    1) ~/scripts/complete-backup.sh ;;
    2) echo "See: https://github.com/settings/tokens" ;;
    3) tail -f ~/backups/backup.log ;;
    4) git push origin main ;;
    5) exec ~/scripts/dashboard.sh ;;
    6) ~/scripts/cleanup.sh ;;
    *) echo "Refreshing..." ;;
esac
echo "=================================================="
