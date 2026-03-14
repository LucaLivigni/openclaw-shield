# 🛡️ OpenClaw Shield 

> **The Essential Security Layer for AI Agents.**

OpenClaw Shield is a security orchestration tool designed to make running AI agents (like those powered by OpenClaw or Claude Code) safe, private, and easy to manage. It provides a hardened sandbox, a command-level firewall, and a beautiful macOS-style dashboard.

---

## ❓ Why do you need Shield?
AI agents are powerful because they can execute terminal commands. But without protection:
*   **Accidents happen:** A wrong `rm` command could wipe your project or your entire disk.
*   **Privacy leaks:** An agent might accidentally read your `.env` files, SSH keys, or browser cookies.
*   **Supply chain risks:** If an agent downloads and runs a malicious script (`curl | sh`), your system is compromised.
*   **Resource drain:** A bug in a script could lead to an infinite loop, crashing your machine.

**Shield solves this by putting a "Digital Bodyguard" between the Agent and your OS.**

---

## 🌟 Key Features

### 1. 🛡️ Command Guard (Firewall)
A real-time interceptor that checks every command before it runs.
- **Privacy Shield:** Automatically blocks any attempt to read sensitive folders like `.ssh`, `.aws`, or `.env`.
- **Blacklist:** Prevents dangerous system-level commands (`sudo`, `mkfs`, `shutdown`).
- **Smart Filtering:** Intercepts risky patterns like `curl | sh` and asks for your approval.

### 2. 🧊 Hardened Sandbox (Docker)
Run your agents in an isolated, restricted environment.
- **Limited Resources:** Cap RAM and CPU usage.
- **Rootless:** Agents can't gain administrative privileges.
- **Safe Filesystem:** Restrict the agent to its designated workspace.

### 3. 🖥️ macOS-Style Dashboard
Manage everything via a beautiful, intuitive interface.
- **Toggles:** Turn terminal access or web browsing ON/OFF for each agent.
- **Activity Monitor:** See a real-time log of what your agents are doing and what Shield has blocked.
- **Dark Mode:** Automatically follows your system theme.

---

## 🚀 Quick Start (World-Ready)

Install Shield with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/LucaLivigni/openclaw-shield/main/install.sh | bash
```

### Next Steps:
1.  **Activate the Sandbox:** `cd docker && docker-compose up -d`
2.  **Open the Dashboard:** Just open `dashboard/index.html` in your browser.
3.  **Sleep Soundly:** Let your agents work while Shield keeps you safe.

---

## 🤝 Contributing
OpenClaw Shield is built for the community. If you have security patterns or ideas, please open an issue or a PR!

## 📄 License
MIT License
