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

# Privacy Shield: Paths that agents should NEVER read or write
FORBIDDEN_PATHS = [
    r'\.ssh',             # SSH keys
    r'\.aws',             # Cloud credentials
    r'\.env',             # Environment secrets
    r'\.bash_history',    # Command history
    r'/etc/passwd',       # System users
    r'keychain',          # macOS Keychain
    r'Cookies'            # Browser cookies
]

# Sensitive patterns that require explicit approval
SENSITIVE_PATTERNS = [
    r'rm\s+',             # Any deletion
    r'kill\s+',           # Killing processes
    r'curl\s+.*\s*\|\s*sh', # The "curl to bash" pipe (extremely dangerous)
    r'wget\s+.*\s*\|\s*sh',
    r'chmod',             # Permission changes
    r'chown',
    r'npm\s+publish'      # Prevent accidental publishing
]

def check_command(command):
    # 1. Check for Forbidden Paths (Privacy Shield)
    for path in FORBIDDEN_PATHS:
        if re.search(path, command, re.IGNORECASE):
            return "BLOCKED", f"Privacy Violation: Access to sensitive path '{path}' is forbidden."

    # 2. Check for Hard Bans
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, command):
            return "BLOCKED", f"Security violation: Command matches banned pattern '{pattern}'"

    # 3. Check for Sensitive commands
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, command):
            return "PENDING", f"Sensitive command detected: '{pattern}'. Approval required."

    # 4. If clean
    return "ALLOWED", "Command is safe to execute."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python guard.py '<command>'")
        sys.exit(1)

    cmd_to_test = sys.argv[1]
    status, message = check_command(cmd_to_test)
    
    print(f"STATUS: {status}")
    print(f"MESSAGE: {message}")
