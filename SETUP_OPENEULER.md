# 🐧 openEuler Setup Guide

Complete guide to run the Tides & Tomes presentation on openEuler Linux.

## 📋 Prerequisites

### 1. Install Python 3.8+

```bash
# Check if Python is installed
python3 --version

# If not installed, install Python 3
sudo dnf install python3 python3-pip python3-devel

# Verify installation
python3 --version
pip3 --version
```

### 2. Install System Dependencies

```bash
# Required for some Python packages
sudo dnf install gcc gcc-c++ make
sudo dnf install python3-tkinter  # For matplotlib backend if needed
```

### 3. Clone or Transfer Project

```bash
# If using git
git clone <repository-url> htb67
cd htb67

# Or if transferring from Windows, ensure line endings are correct
dos2unix run.sh scripts/run_presentation.sh 2>/dev/null || true
```

## 🚀 Quick Start

### Option 1: Using the Quick Launcher

```bash
# Make executable
chmod +x run.sh

# Run
./run.sh
```

### Option 2: Using the Full Script

```bash
# Make executable
chmod +x scripts/run_presentation.sh

# Run
./scripts/run_presentation.sh
```

### Option 3: Direct Command

```bash
# Install dependencies
pip3 install -r presentation/requirements.txt

# Run the dashboard
python3 -m streamlit run presentation/app.py
```

## 🌐 Accessing the Dashboard

Once started, the dashboard will be available at:

- **Local:** http://localhost:8501
- **Network:** http://[your-server-ip]:8501

If running on a remote server, you may need to:

1. **Open firewall port 8501:**
   ```bash
   sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
   sudo firewall-cmd --reload
   ```

2. **Use SSH tunnel (more secure):**
   ```bash
   # On your local machine
   ssh -L 8501:localhost:8501 user@server-ip
   # Then access http://localhost:8501 on your local browser
   ```

## 📦 Manual Dependency Installation

If you need to install dependencies manually:

```bash
pip3 install streamlit>=1.28.0
pip3 install plotly>=5.17.0
pip3 install pandas>=2.1.0
pip3 install numpy>=1.24.0
pip3 install requests>=2.31.0
```

## 🔧 Troubleshooting

### Issue: Permission Denied

```bash
chmod +x run.sh
chmod +x scripts/run_presentation.sh
```

### Issue: Module Not Found

```bash
# Ensure pip packages are in PATH
python3 -m pip install --user -r presentation/requirements.txt

# Or use a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r presentation/requirements.txt
python3 -m streamlit run presentation/app.py
```

### Issue: Port Already in Use

```bash
# Find process using port 8501
sudo lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use a different port
python3 -m streamlit run presentation/app.py --server.port 8502
```

### Issue: Streamlit Command Not Found

```bash
# Use module syntax instead
python3 -m streamlit run presentation/app.py
```

### Issue: firewalld Not Running

```bash
# Start firewall service
sudo systemctl start firewalld
sudo systemctl enable firewalld
```

## 🐳 Docker Alternative (Optional)

If you prefer Docker on openEuler:

```bash
# Install Docker
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker

# Create Dockerfile (see DOCKER_SETUP.md)
# Build and run
sudo docker build -t tides-tomes .
sudo docker run -p 8501:8501 tides-tomes
```

## 🔄 Running in Background

To keep the dashboard running after logout:

### Using nohup

```bash
nohup python3 -m streamlit run presentation/app.py --server.headless=true > streamlit.log 2>&1 &

# View logs
tail -f streamlit.log

# Stop
pkill -f streamlit
```

### Using screen

```bash
# Install screen
sudo dnf install screen

# Start screen session
screen -S tides-tomes

# Run dashboard
python3 -m streamlit run presentation/app.py

# Detach: Press Ctrl+A then D
# Reattach: screen -r tides-tomes
# Kill session: screen -X -S tides-tomes quit
```

### Using systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/tides-tomes.service

# Add content (see SYSTEMD_SERVICE.md)
# Enable and start
sudo systemctl enable tides-tomes
sudo systemctl start tides-tomes
sudo systemctl status tides-tomes
```

## 📊 Resource Requirements

- **RAM:** 512MB minimum, 1GB recommended
- **CPU:** 1 core minimum, 2+ cores recommended
- **Disk:** 500MB for Python packages + application
- **Network:** Port 8501 open for HTTP access

## ✅ Verification

After installation, verify everything works:

```bash
# Test Python
python3 --version

# Test pip
pip3 --version

# Test streamlit
python3 -m streamlit --version

# Test application
python3 -c "import streamlit, plotly, pandas, numpy, requests; print('All dependencies OK')"

# Run dashboard
python3 -m streamlit run presentation/app.py
```

## 🎯 Challenge Pages

Once running, navigate through these pages:

1. **Overview** - Complete system visualization
2. **CompSoc Challenge** - Interactive sensitivity analysis
3. **G-Research Challenge** - Real-time data monitoring
4. **Hoppers Challenge** - Edinburgh impact analysis

## 📝 Notes for openEuler

- openEuler uses `dnf` package manager (RHEL-based)
- Python 3 is typically installed by default
- SELinux may be enforced - adjust if needed
- Firewall rules may need configuration
- Use `python3` instead of `python`
- Use `pip3` instead of `pip`

## 🆘 Support

For issues specific to openEuler, check:
- openEuler documentation: https://docs.openeuler.org/
- Python compatibility
- Firewall and networking settings
- SELinux policies if enforced
