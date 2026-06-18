#!/bin/bash
# ═══════════════════════════════════════════════════════
# EStock API — VPS Initial Setup Script
# Run once on the VPS to set up the environment
# ═══════════════════════════════════════════════════════

set -e

APP_DIR="/home/nhox9xy/estock-api"
VENV_DIR="$APP_DIR/venv"

echo "══════════════════════════════════════════════════"
echo "  EStock API — VPS Setup"
echo "══════════════════════════════════════════════════"

# 1. Update system
echo "→ Updating system packages..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git

# 2. Create virtual environment
echo "→ Creating virtual environment..."
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
echo "→ Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create .env if not exists
if [ ! -f .env ]; then
    echo "→ Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env to add your VNSTOCK_API_KEY"
fi

# 5. Create systemd service
echo "→ Creating systemd service..."
sudo tee /etc/systemd/system/estock-api.service > /dev/null << 'EOF'
[Unit]
Description=EStock API - Vietnamese Stock Market Data Service
After=network.target

[Service]
Type=simple
User=nhox9xy
Group=nhox9xy
WorkingDirectory=/home/nhox9xy/estock-api
Environment=PATH=/home/nhox9xy/estock-api/venv/bin:/usr/bin
ExecStart=/home/nhox9xy/estock-api/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable and start service
echo "→ Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable estock-api
sudo systemctl restart estock-api

# 7. Check status
echo ""
echo "══════════════════════════════════════════════════"
sudo systemctl status estock-api --no-pager
echo "══════════════════════════════════════════════════"
echo "✅ Setup complete! API running at http://0.0.0.0:8000"
echo "   Swagger: http://34.87.142.4:8000/docs"
