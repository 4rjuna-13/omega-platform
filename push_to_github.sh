#!/bin/bash

# PROJECT OMEGA - GitHub Push Script
# Phase 2G Launch Ready

echo "🚀 PROJECT OMEGA - GITHUB LAUNCH PUSH"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "omega_v4_phase_2g_final.py" ]; then
    echo "❌ Error: Not in omega-platform directory"
    echo "Run this script from the omega-platform directory"
    exit 1
fi

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📁 Adding files to git..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "🚀 Project Omega Phase 2G Launch

Complete Phase 2G: Beginner Tutorial System
- 15-minute guided tutorial experience
- 3 modules: Observability, Deception, Response
- Integrated mock server for safe training
- Complete documentation and marketing assets
- Ready for public launch"

echo ""
echo "📊 GIT STATUS:"
echo "============="
git status

echo ""
echo "🔗 REMOTE REPOSITORY SETUP"
echo "=========================="
echo "Your GitHub repository: https://github.com/birdsongcherokee-crypto/omega-platform"
echo ""
echo "To push to GitHub, run:"
echo "git remote add origin https://github.com/birdsongcherokee-crypto/omega-platform.git"
echo "git push -u origin main"
echo ""
echo "Or use SSH:"
echo "git remote add origin git@github.com:birdsongcherokee-crypto/omega-platform.git"
echo "git push -u origin main"
echo ""
echo "🎉 READY FOR LAUNCH! 🚀"
