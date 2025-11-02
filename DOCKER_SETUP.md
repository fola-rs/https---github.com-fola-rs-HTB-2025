# Docker Setup for openEuler

Complete guide to run Tides & Tomes using Docker/Podman on openEuler.

## 🐳 Prerequisites

### Install Docker (or Podman)

```bash
# Install Docker on openEuler
sudo dnf install docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect

# Verify installation
docker --version
```

Or use Podman (Docker alternative):

```bash
# Podman is often preferred on RHEL-based systems
sudo dnf install podman
podman --version
```

## 📦 Building the Image

### Option 1: Using Dockerfile

Create a `Dockerfile` in the project root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY presentation/requirements.txt /app/presentation/requirements.txt
RUN pip install --no-cache-dir -r presentation/requirements.txt

# Copy application
COPY presentation/ /app/presentation/
COPY data/ /app/data/

# Expose port
EXPOSE 8501

# Environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run
CMD ["python", "-m", "streamlit", "run", "presentation/app.py", \
     "--server.headless=true", "--server.address=0.0.0.0"]
```

Build the image:

```bash
# Using Docker
docker build -t tides-tomes:latest .

# Using Podman
podman build -t tides-tomes:latest .
```

### Option 2: Multi-stage Build (Smaller Image)

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY presentation/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY presentation/ /app/presentation/
COPY data/ /app/data/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "presentation/app.py", \
     "--server.headless=true", "--server.address=0.0.0.0"]
```

## 🚀 Running the Container

### Basic Run

```bash
# Docker
docker run -d -p 8501:8501 --name tides-tomes tides-tomes:latest

# Podman
podman run -d -p 8501:8501 --name tides-tomes tides-tomes:latest
```

### Run with Custom Port

```bash
docker run -d -p 8080:8501 --name tides-tomes tides-tomes:latest
# Access at http://localhost:8080
```

### Run with Volume Mount (for development)

```bash
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/presentation:/app/presentation \
  --name tides-tomes \
  tides-tomes:latest
```

### Run with Auto-restart

```bash
docker run -d \
  -p 8501:8501 \
  --name tides-tomes \
  --restart unless-stopped \
  tides-tomes:latest
```

## 🔧 Container Management

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View logs
docker logs tides-tomes

# Follow logs in real-time
docker logs -f tides-tomes

# Stop container
docker stop tides-tomes

# Start container
docker start tides-tomes

# Restart container
docker restart tides-tomes

# Remove container
docker rm tides-tomes

# Remove image
docker rmi tides-tomes:latest
```

## 🌐 Accessing the Dashboard

Once running:

- **Local:** <http://localhost:8501>
- **Network:** <http://server-ip:8501>

### Configure Firewall

```bash
# Open port 8501
sudo firewall-cmd --zone=public --add-port=8501/tcp --permanent
sudo firewall-cmd --reload
```

## 🔒 Security Considerations

### Run as Non-root User

Update Dockerfile:

```dockerfile
# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
```

### Use Read-only Filesystem

```bash
docker run -d \
  -p 8501:8501 \
  --read-only \
  --tmpfs /tmp \
  --name tides-tomes \
  tides-tomes:latest
```

### Limit Resources

```bash
docker run -d \
  -p 8501:8501 \
  --memory="512m" \
  --cpus="1.0" \
  --name tides-tomes \
  tides-tomes:latest
```

## 📝 Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  tides-tomes:
    build: .
    ports:
      - "8501:8501"
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8501/_stcore/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with Docker Compose:

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

## 🐙 Using Podman Instead

Podman commands are nearly identical to Docker:

```bash
# Build
podman build -t tides-tomes:latest .

# Run
podman run -d -p 8501:8501 --name tides-tomes tides-tomes:latest

# Manage
podman ps
podman logs tides-tomes
podman stop tides-tomes
```

### Podman with systemd

Generate systemd service:

```bash
# Start container
podman run -d -p 8501:8501 --name tides-tomes tides-tomes:latest

# Generate service file
podman generate systemd --name tides-tomes --files --new

# Move to systemd directory
sudo mv container-tides-tomes.service /etc/systemd/system/

# Enable and start
sudo systemctl enable container-tides-tomes
sudo systemctl start container-tides-tomes
```

## 🔍 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs tides-tomes

# Check if port is in use
sudo lsof -i :8501
```

### Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in

# Or run with sudo
sudo docker run ...
```

### SELinux Issues (openEuler)

```bash
# Check SELinux status
sestatus

# If enforcing, temporarily set to permissive
sudo setenforce 0

# Or add SELinux context to volume mounts
docker run -v $(pwd)/presentation:/app/presentation:Z ...
```

## 📊 Resource Usage

Typical container resource usage:

- **Image size:** ~400-600 MB
- **RAM usage:** 200-400 MB
- **CPU:** Minimal (<1% idle, 10-20% under load)

## ✅ Verification

```bash
# Check if container is running
docker ps | grep tides-tomes

# Test health endpoint
curl http://localhost:8501/_stcore/health

# Access dashboard
curl http://localhost:8501
```
