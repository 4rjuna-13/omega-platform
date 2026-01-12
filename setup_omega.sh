#!/bin/bash

echo "🚀 Setting up Enhanced Omega Platform v4.5"

# Create required directories
mkdir -p omega_platform/data/{mitre_attack,scenarios/{marketplace,user},data_lake}
mkdir -p omega_platform/tools
mkdir -p omega_platform/web/templates
mkdir -p config

# Create __init__.py files
touch omega_platform/__init__.py
touch omega_platform/modules/__init__.py
touch omega_platform/tools/__init__.py
touch omega_platform/web/__init__.py

# Create requirements file if it doesn't exist
if [ ! -f requirements-enhanced.txt ]; then
    echo "Creating requirements-enhanced.txt..."
    cat > requirements-enhanced.txt << 'REQEOF'
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
plotly>=5.15.0
flask>=2.3.0
flask-cors>=4.0.0
sqlalchemy>=2.0.0
requests>=2.31.0
pyyaml>=6.0
jsonschema>=4.17.0
REQEOF
fi

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements-enhanced.txt

# Run the enhanced setup
echo "Initializing enhanced modules..."
python omega_platform/modules/setup_enhanced.py

echo "🎉 Setup complete!"
echo ""
echo "To start the platform:"
echo "  python omega_platform/web/app.py"
echo ""
echo "To generate reports:"
echo "  python omega_platform/tools/generate_reports.py"
