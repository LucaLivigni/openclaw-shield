#!/bin/bash

# --- OpenClaw Shield Installer ---
# Vision: One-line installation for instant security.

echo "🛡️  Starting OpenClaw Shield Installation..."

# 1. Create directory structure
mkdir -p logs config scripts dashboard docker

# 2. Check for Docker
if ! [ -x "$(command -v docker)" ]; then
  echo "⚠️  Error: Docker is not installed. Please install Docker to use the Sandbox feature."
else
  echo "✅ Docker detected."
fi

# 3. Create a default .env if not exists
if [ ! -f .env ]; then
  echo "SHIELD_MODE=HARDENED" > .env
  echo "TELEGRAM_ALERTS=DISABLED" >> .env
  echo "✅ Created default .env configuration."
fi

# 4. Set permissions
chmod +x scripts/guard.py

echo ""
echo "🚀 OpenClaw Shield is ready to fortify your agents!"
echo "Next steps:"
echo "1. Run 'docker-compose up -d' in the /docker folder to start the Sandbox."
echo "2. Open 'dashboard/index.html' in your browser to manage permissions."
echo ""
echo "For more info, visit: https://github.com/LucaLivigni/openclaw-shield"
