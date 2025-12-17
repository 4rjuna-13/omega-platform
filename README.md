# 🛡️ Omega Platform - Advanced Threat Simulation System

> **Phase 3 Complete: Professional Architecture & Dashboard Deployed**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Status](https://img.shields.io/badge/Phase-3%20Complete-success)](README.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Omega Platform** is a comprehensive security simulation and threat intelligence platform designed for security teams to safely test defenses, simulate attacks, and predict threats using machine learning.

## 🎯 Features

### ✅ **Phase 3: Architecture Complete**
- **Modern Python Package Architecture** - Clean, modular structure
- **Simulation Dashboard** - Web interface with real-time metrics
- **REST API** - 8+ endpoints for integration and automation
- **Plugin System** - Modular architecture for easy extension
- **6 Threat Simulation Scenarios** - Ready-to-use attack simulations
- **Hierarchical Configuration** - Environment-based settings management

### 🔄 **In Development (Phase 4)**
- **Predictive Threat Modeling** - ML-powered threat prediction
- **Deception Engine Integration** - Real honeypot management
- **Enhanced Visualization** - Advanced threat analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/omega-platform.git
cd omega-platform

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the platform
python -m omega_platform start --env development
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
env/
venv/
ENV/
env.bak/
venv.bak/
omega_env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log
omega_platform.log

# Test coverage
.coverage
htmlcov/
.pytest_cache/
.coverage.*
.tox/

# Jupyter Notebook
.ipynb_checkpoints

# Environment variables
.env
.env.local
.env.*.local

# Backup files
*.bak
*.backup
backup/
archive/
backup_pre_architecture_migration/

# Database
*.db
*.sqlite

# ML Models (except our trained model)
!omega_platform/modules/prediction/threat_model.pkl
*.pkl
*.joblib
*.h5
*.keras

# Temporary files
tmp/
temp/

# Documentation
_site/
.sass-cache/
.jekyll-cache/
.jekyll-metadata

# Security
secrets.txt
api_keys.txt
credentials.json

# Performance
profile/
prof/

# Archive old versions
archive_old_versions/

# Patch files
*.patch
*.rej
*.orig

# Test files
test_*.py

# Old scripts
CLEANUP_LEGACY.sh
start_*.sh
test_*.sh
