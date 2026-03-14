# OpenClaw Shield - Hardened Sandbox
# Base: Minimal Ubuntu
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update and install minimal necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    git \
    nano \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged agent user
RUN useradd -m -s /bin/bash clawagent

# Block access to dangerous binaries (defense in depth)
RUN chmod 700 /bin/su /usr/bin/sudo /sbin/shutdown /sbin/reboot

# Setup workspace directory
WORKDIR /workspace
RUN chown clawagent:clawagent /workspace

# Switch to the restricted user
USER clawagent

# Default command
CMD ["/bin/bash"]
