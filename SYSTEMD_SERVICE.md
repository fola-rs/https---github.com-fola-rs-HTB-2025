# systemd Service Configuration for Tides & Tomes

## Create Service File

```bash
sudo nano /etc/systemd/system/tides-tomes.service
```

## Service Configuration

```ini
[Unit]
Description=Tides & Tomes Streamlit Dashboard
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/htb67
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 -m streamlit run presentation/app.py --server.headless=true --server.port=8501
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Setup Instructions

1. **Edit the service file** - Replace placeholders:
   - `your-username` with your Linux username
   - `/path/to/htb67` with actual path (e.g., `/home/user/htb67`)

2. **Reload systemd:**
   ```bash
   sudo systemctl daemon-reload
   ```

3. **Enable service** (start on boot):
   ```bash
   sudo systemctl enable tides-tomes
   ```

4. **Start service:**
   ```bash
   sudo systemctl start tides-tomes
   ```

5. **Check status:**
   ```bash
   sudo systemctl status tides-tomes
   ```

6. **View logs:**
   ```bash
   sudo journalctl -u tides-tomes -f
   ```

## Service Management Commands

```bash
# Start
sudo systemctl start tides-tomes

# Stop
sudo systemctl stop tides-tomes

# Restart
sudo systemctl restart tides-tomes

# Status
sudo systemctl status tides-tomes

# Enable (auto-start on boot)
sudo systemctl enable tides-tomes

# Disable (don't auto-start)
sudo systemctl disable tides-tomes

# View logs (last 50 lines)
sudo journalctl -u tides-tomes -n 50

# Follow logs in real-time
sudo journalctl -u tides-tomes -f
```

## Advanced Configuration

### With Virtual Environment

```ini
[Unit]
Description=Tides & Tomes Streamlit Dashboard
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/htb67
Environment="PATH=/path/to/htb67/venv/bin:/usr/bin:/usr/local/bin"
ExecStart=/path/to/htb67/venv/bin/python -m streamlit run presentation/app.py --server.headless=true --server.port=8501
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### With Custom Port

Change `--server.port=8501` to your desired port (e.g., `--server.port=8080`)

### With Environment Variables

```ini
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="STREAMLIT_SERVER_PORT=8501"
Environment="STREAMLIT_SERVER_HEADLESS=true"
```
