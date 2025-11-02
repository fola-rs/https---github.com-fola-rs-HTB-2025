# 🐧 Running on openEuler - Quick Reference

This project is now fully compatible with openEuler Linux! Choose your preferred method below.

## 🚀 Quick Start Options

### 1️⃣ Automated Installation (Recommended)

```bash
chmod +x install_openeuler.sh
./install_openeuler.sh
```

This script will:
- Check and install Python 3
- Install system dependencies
- Optionally create virtual environment
- Install Python packages
- Configure firewall
- Offer to start the dashboard

### 2️⃣ Quick Launcher

```bash
chmod +x run.sh
./run.sh
```

### 3️⃣ Full Script

```bash
chmod +x scripts/run_presentation.sh
./scripts/run_presentation.sh
```

### 4️⃣ Manual Command

```bash
pip3 install -r presentation/requirements.txt
python3 -m streamlit run presentation/app.py
```

## 📚 Detailed Guides

Choose the guide that matches your use case:

| Guide | Use Case | Link |
|-------|----------|------|
| **Basic Setup** | General installation on openEuler | [SETUP_OPENEULER.md](SETUP_OPENEULER.md) |
| **Docker/Podman** | Containerized deployment | [DOCKER_SETUP.md](DOCKER_SETUP.md) |
| **systemd Service** | Run as background service | [SYSTEMD_SERVICE.md](SYSTEMD_SERVICE.md) |

## 🔧 Key Differences from Windows

| Aspect | Windows | openEuler |
|--------|---------|-----------|
| Python command | `python` | `python3` |
| pip command | `pip` | `pip3` |
| Path separator | `\` | `/` |
| Script extension | `.ps1` | `.sh` |
| Package manager | N/A | `dnf` |
| Service manager | Services | `systemd` |
| Firewall | Windows Firewall | `firewalld` |

## 🌐 Accessing the Dashboard

- **Local:** <http://localhost:8501>
- **Network:** <http://your-server-ip:8501>
- **SSH Tunnel:** `ssh -L 8501:localhost:8501 user@server`

## 🔥 Firewall Configuration

```bash
# Open port 8501
sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
sudo firewall-cmd --reload

# Verify
sudo firewall-cmd --list-ports
```

## 🐳 Docker Quick Start

```bash
# Install Docker
sudo dnf install docker
sudo systemctl start docker

# Build image
docker build -t tides-tomes .

# Run container
docker run -d -p 8501:8501 --name tides-tomes tides-tomes:latest

# Access at http://localhost:8501
```

## 📦 Dependencies

All required packages are in `presentation/requirements.txt`:

- `streamlit>=1.28.0` - Web dashboard framework
- `plotly>=5.17.0` - Interactive visualizations
- `pandas>=2.1.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `requests>=2.31.0` - HTTP requests

## 🔍 Troubleshooting

### Command Not Found

```bash
# Use python3 instead of python
python3 -m streamlit run presentation/app.py
```

### Permission Denied

```bash
chmod +x run.sh
chmod +x install_openeuler.sh
```

### Port Already in Use

```bash
# Find and kill process
sudo lsof -i :8501
kill -9 <PID>

# Or use different port
python3 -m streamlit run presentation/app.py --server.port 8502
```

### Module Not Found

```bash
# Install dependencies
pip3 install -r presentation/requirements.txt

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r presentation/requirements.txt
```

## 🎯 Challenge Pages

1. **Overview** - Complete system visualization with Sankey diagram
2. **CompSoc Challenge** - Interactive sensitivity analysis with sliders
3. **G-Research Challenge** - Real-time correlation analysis and predictions
4. **Hoppers Challenge** - Edinburgh tourism and economic impact

## 📊 System Requirements

- **OS:** openEuler 20.03 LTS or newer (or any RHEL-based distro)
- **Python:** 3.8 or higher
- **RAM:** 512MB minimum, 1GB recommended
- **CPU:** 1 core minimum, 2+ recommended
- **Disk:** 500MB for packages + application
- **Network:** Port 8501 open (HTTP)

## ✅ Verification

Test everything is working:

```bash
# Check Python
python3 --version

# Check Streamlit
python3 -m streamlit --version

# Test imports
python3 -c "import streamlit, plotly, pandas, numpy, requests; print('✅ All OK')"

# Run dashboard
python3 -m streamlit run presentation/app.py
```

## 🆘 Getting Help

- Check the detailed guides in `SETUP_OPENEULER.md`
- Review logs: `journalctl -u tides-tomes -f` (if using systemd)
- Docker logs: `docker logs tides-tomes` (if using Docker)
- openEuler docs: <https://docs.openeuler.org/>

## 📝 Files for openEuler

- `install_openeuler.sh` - Automated setup script
- `run.sh` - Quick launcher
- `scripts/run_presentation.sh` - Full launch script with messages
- `SETUP_OPENEULER.md` - Complete setup guide
- `DOCKER_SETUP.md` - Container deployment guide
- `SYSTEMD_SERVICE.md` - Background service setup

## 🔄 Migrating from Windows

If you're moving from Windows to openEuler:

1. **Transfer files** (ensure line endings are correct)
2. **Run installation script:** `./install_openeuler.sh`
3. **Start dashboard:** `./run.sh`
4. Done! Access at <http://localhost:8501>

No code changes needed - the Python application works identically on both platforms!
