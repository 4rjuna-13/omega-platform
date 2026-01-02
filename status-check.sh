#!/bin/bash
echo "=== SYSTEM STATUS ==="
echo "1. Disk: $(df -h ~/ | tail -1 | awk '{print $4}') free"
echo "2. Backups: $(find ~/backups -type f 2>/dev/null | wc -l) files"
echo "3. Shared folders:"
ls -la /mnt/chromeos/ 2>/dev/null || echo "   Not accessible"
echo "4. Git status:"
git status --short 2>/dev/null || echo "   Not a git repo"
echo "===================="
