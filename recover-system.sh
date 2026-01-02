#!/bin/bash
echo "=== SYSTEM RECOVERY ==="
echo "This will restore your Omega Platform environment"

if [ ! -d ~/backups/daily ]; then
    echo "❌ No backups found!"
    exit 1
fi

# Find latest backup
LATEST=$(ls -t ~/backups/daily/ | head -1)
echo "Restoring from: $LATEST"

# Restore projects
cp -r ~/backups/daily/$LATEST/projects ~/ 2>/dev/null
cp -r ~/backups/daily/$LATEST/workspace ~/ 2>/dev/null
cp -r ~/backups/daily/$LATEST/config ~/ 2>/dev/null

# Restore scripts
mkdir -p ~/scripts
cp ~/backups/daily/$LATEST/scripts/* ~/scripts/ 2>/dev/null

# Restore Git config
cp ~/backups/daily/$LATEST/.gitconfig ~/ 2>/dev/null

echo "✅ Recovery complete!"
echo "Run ~/scripts/dashboard.sh to verify"
