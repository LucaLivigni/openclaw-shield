#!/usr/bin/env bash
# OpenClaw Shield - Hardened Docker Launcher
# Runs the container with extreme security limits (Apple Sandbox style)

IMAGE_NAME="openclaw-sandbox:latest"
WORKSPACE_DIR="$HOME/.openclaw/workspace-dev"

# Build if missing
if ! docker image inspect $IMAGE_NAME > /dev/null 2>&1; then
    echo "🛡️  Building OpenClaw Shield Sandbox..."
    docker build -t $IMAGE_NAME "$(dirname "$0")"
fi

# Ensure workspace exists
mkdir -p "$WORKSPACE_DIR"

echo "🔒 Starting Hardened Sandbox..."

docker run -it --rm \
    --name openclaw_agent_session \
    --user clawagent \
    --workdir /workspace \
    --read-only \
    --tmpfs /tmp:rw,nosuid,nodev,exec,size=512m \
    --tmpfs /run:rw,nosuid,nodev \
    --security-opt="no-new-privileges:true" \
    --cap-drop=ALL \
    --cpus="1.0" \
    --memory="1g" \
    --network=none \
    -v "$WORKSPACE_DIR:/workspace:rw" \
    $IMAGE_NAME \
    /bin/bash
