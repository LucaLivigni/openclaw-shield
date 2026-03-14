#!/usr/bin/env python3
"""
OpenClaw Shield - Modular Firewall & Snapshot
Validates commands against configurable security policies and auto-commits on sensitive actions.
"""

import json
import re
import sys
import subprocess
import os
from pathlib import Path
from typing import Tuple, Dict, Any

class FirewallGuard:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.banned = self.config.get("firewall", {}).get("banned_patterns", [])
        self.forbidden = self.config.get("firewall", {}).get("forbidden_paths", [])
        self.sensitive = self.config.get("firewall", {}).get("sensitive_patterns", [])
        self.workspace_dir = Path(os.environ.get("HOME", "/tmp")) / ".openclaw" / "workspace-dev"

    def _load_config(self) -> Dict[str, Any]:
        try:
            root_dir = Path(__file__).parent.parent
            target_path = root_dir / self.config_path
            if not target_path.exists():
                return {}
            with open(target_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {}

    def _create_snapshot(self, command: str):
        """Creates an invisible auto-commit in the workspace before a sensitive action."""
        try:
            if not (self.workspace_dir / ".git").exists():
                subprocess.run(["git", "init"], cwd=self.workspace_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "add", "."], cwd=self.workspace_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            commit_msg = f"shield-auto-snapshot: before '{command}'"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.workspace_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass # Fail silently if git is not available or errors out

    def inspect_command(self, command: str) -> Tuple[str, str]:
        for path_pattern in self.forbidden:
            if re.search(path_pattern, command, re.IGNORECASE):
                return "BLOCKED", f"Privacy Violation: Access to '{path_pattern}' is forbidden."

        for pattern in self.banned:
            if re.search(pattern, command):
                return "BLOCKED", f"Security Violation: Command matches '{pattern}'."

        for pattern in self.sensitive:
            if re.search(pattern, command):
                self._create_snapshot(command)
                return "PENDING", f"Sensitive Operation: '{pattern}'. Auto-snapshot taken. Approval required."

        return "ALLOWED", "Command is safe to execute."

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    command = sys.argv[1]
    guard = FirewallGuard("config.json")
    status, message = guard.inspect_command(command)
    
    print(f"STATUS: {status}")
    print(f"MESSAGE: {message}")
    
    if status == "BLOCKED":
        sys.exit(1)
    elif status == "PENDING":
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
