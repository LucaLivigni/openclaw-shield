import sys
import re

# --- CONFIGURATION ---
# List of banned commands or patterns
BANNED_PATTERNS = [
    r'rm\s+-rf\s+/',      # Dangerous delete
    r'sudo',              # Admin elevation
    r'mkfs',              # Format disk
    r'dd\s+if=',          # Raw disk access
    r'>\s*/dev/',         # Writing to devices
    r'shutdown',          # System shutdown
    r'reboot'             # System reboot
]

# Sensitive patterns that require explicit approval
SENSITIVE_PATTERNS = [
    r'rm\s+',             # Any deletion
    r'kill\s+',           # Killing processes
    r'curl\s+',           # External downloads
    r'wget\s+',
    r'chmod',             # Permission changes
    r'chown'
]

def check_command(command):
    # 1. Check for Hard Bans
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, command):
            return "BLOCKED", f"Security violation: Command matches banned pattern '{pattern}'"

    # 2. Check for Sensitive commands
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, command):
            return "PENDING", f"Sensitive command detected: '{pattern}'. Approval required."

    # 3. If clean
    return "ALLOWED", "Command is safe to execute."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python guard.py '<command>'")
        sys.exit(1)

    cmd_to_test = sys.argv[1]
    status, message = check_command(cmd_to_test)
    
    print(f"STATUS: {status}")
    print(f"MESSAGE: {message}")
