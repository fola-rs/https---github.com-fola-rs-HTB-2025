#!/bin/bash
# OpenEuler Setup Script for Tides & Tomes Dashboard
# Compatible with OpenEuler 20.03 LTS and later

set -e

echo "=========================================="
echo "Tides & Tomes - OpenEuler Setup"
echo "=========================================="

# Update system
echo "[1/6] Updating system packages..."
sudo yum update -y

# Install Python 3.9+ and development tools
echo "[2/6] Installing Python and build dependencies..."
sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++ make cmake \
    git wget curl bzip2 libffi-devel openssl-devel zlib-devel \
    postgresql-devel sqlite-devel

# Upgrade pip
echo "[3/6] Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
echo "[4/6] Installing Python packages..."
python3 -m pip install --no-cache-dir \
    pandas==2.1.3 \
    numpy==1.26.2 \
    scipy==1.11.4 \
    statsmodels==0.14.0 \
    scikit-learn==1.3.2 \
    matplotlib==3.8.2 \
    seaborn==0.13.0 \
    plotly==5.18.0 \
    streamlit==1.29.0 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    pyyaml==6.0.1

# Verify installation
echo "[5/6] Verifying Python installation..."
python3 --version
python3 -c "import streamlit; import pandas; import plotly; print('All critical packages imported successfully')"

# Create systemd service file
echo "[6/6] Creating systemd service (optional)..."
cat > /tmp/tides-tomes.service <<'EOF'
[Unit]
Description=Tides & Tomes Streamlit Dashboard
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/path/to/htb67
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/bin/python3 -m streamlit run presentation/app_complete.py --server.port=8501 --server.headless=true
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the dashboard:"
echo "  cd /path/to/htb67"
echo "  python3 -m streamlit run presentation/app_complete.py"
echo ""
echo "To install as systemd service:"
echo "  1. Edit /tmp/tides-tomes.service with your user and path"
echo "  2. sudo mv /tmp/tides-tomes.service /etc/systemd/system/"
echo "  3. sudo systemctl daemon-reload"
echo "  4. sudo systemctl enable --now tides-tomes"
echo ""
echo "Dashboard will be available at: http://localhost:8501"
echo "=========================================="
