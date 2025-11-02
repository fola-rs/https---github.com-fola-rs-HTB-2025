#!/bin/bash
# Installation script for openEuler/RHEL-based systems

set -e

echo "🌊 Tides & Tomes - openEuler Installation Script"
echo "=================================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ This script is for Linux systems only"
    exit 1
fi

# Check for Python 3
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 not found. Installing..."
    sudo dnf install -y python3 python3-pip python3-devel
else
    echo "✅ Python 3 found: $(python3 --version)"
fi

# Check for pip
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 not found. Installing..."
    sudo dnf install -y python3-pip
else
    echo "✅ pip3 found: $(pip3 --version)"
fi

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."
sudo dnf install -y gcc gcc-c++ make

# Create virtual environment (recommended)
echo ""
read -p "🤔 Create Python virtual environment? (recommended) [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
    VENV=true
else
    VENV=false
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
if [ "$VENV" = true ]; then
    pip install -r presentation/requirements.txt
else
    pip3 install --user -r presentation/requirements.txt
fi

echo ""
echo "✅ Installation complete!"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x run.sh
chmod +x scripts/run_presentation.sh
echo "✅ Scripts are now executable"

# Check firewall
echo ""
read -p "🔥 Configure firewall to open port 8501? [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    if command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
        sudo firewall-cmd --reload
        echo "✅ Firewall configured"
    else
        echo "⚠️  firewalld not found. You may need to configure firewall manually."
    fi
fi

# Offer to run the dashboard
echo ""
echo "=================================================="
echo "🎉 Setup Complete!"
echo "=================================================="
echo ""
echo "To start the dashboard:"
if [ "$VENV" = true ]; then
    echo "  1. Activate virtual environment: source venv/bin/activate"
    echo "  2. Run: ./run.sh"
else
    echo "  Run: ./run.sh"
fi
echo ""
echo "Or use: python3 -m streamlit run presentation/app.py"
echo ""
echo "Access at: http://localhost:8501"
echo ""

read -p "🚀 Start the dashboard now? [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    if [ "$VENV" = true ]; then
        python -m streamlit run presentation/app.py
    else
        python3 -m streamlit run presentation/app.py
    fi
fi
