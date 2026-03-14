#!/usr/bin/env python3
"""
OpenClaw Shield - Modular Firewall
Validates commands against configurable security policies.
"""

import json
import re
import sys
from pathlib import Path
from typing import Tuple, List, Dict, Any

class FirewallGuard:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.banned = self.config.get("firewall", {}).get("banned_patterns", [])
        self.forbidden = self.config.get("firewall", {}).get("forbidden_paths", [])
        self.sensitive = self.config.get("firewall", {}).get("sensitive_patterns", [])

    def _load_config(self) -> Dict[str, Any]:
        """Loads firewall rules from the main configuration file."""
        try:
            # Try relative to the script's parent (root of the project)
            root_dir = Path(__file__).parent.parent
            target_path = root_dir / self.config_path
            
            if not target_path.exists():
                return {}
                
            with open(target_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load config from {self.config_path} - {e}", file=sys.stderr)
            return {}

    def inspect_command(self, command: str) -> Tuple[str, str]:
        """
        Inspects a command against the firewall rules.
        Returns a tuple of (Status, Message).
        """
        # 1. Check Privacy Constraints (Forbidden Paths)
        for path_pattern in self.forbidden:
            if re.search(path_pattern, command, re.IGNORECASE):
                return "BLOCKED", f"Privacy Violation: Access to sensitive path '{path_pattern}' is forbidden."

        # 2. Check Hard Bans (Banned Patterns)
        for pattern in self.banned:
            if re.search(pattern, command):
                return "BLOCKED", f"Security Violation: Command matches banned pattern '{pattern}'."

        # 3. Check Sensitive Operations (Requires Approval)
        for pattern in self.sensitive:
            if re.search(pattern, command):
                return "PENDING", f"Sensitive Operation: Command matches '{pattern}'. Approval required."

        return "ALLOWED", "Command is safe to execute."

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 guard.py '<command>'")
        sys.exit(1)

    command = sys.argv[1]
    guard = FirewallGuard("config.json")
    status, message = guard.inspect_command(command)
    
    print(f"STATUS: {status}")
    print(f"MESSAGE: {message}")
    
    # Exit code based on status
    if status == "BLOCKED":
        sys.exit(1)
    elif status == "PENDING":
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
