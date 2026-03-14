import json
import os

PERMISSIONS_FILE = "agent_permissions.json"

DEFAULT_PERMISSIONS = {
    "dev": {
        "terminal": "RESTRICTED",
        "filesystem": "WORKSPACE_ONLY",
        "network": "ALLOWED",
        "approval_required": True
    },
    "trader": {
        "terminal": "BLOCKED",
        "filesystem": "NONE",
        "network": "ALLOWED",
        "approval_required": False
    },
    "researcher": {
        "terminal": "ALLOWED",
        "filesystem": "WORKSPACE_ONLY",
        "network": "ALLOWED",
        "approval_required": False
    }
}

def load_permissions():
    if not os.path.exists(PERMISSIONS_FILE):
        with open(PERMISSIONS_FILE, 'w') as f:
            json.dump(DEFAULT_PERMISSIONS, f, indent=4)
        return DEFAULT_PERMISSIONS
    
    with open(PERMISSIONS_FILE, 'r') as f:
        return json.load(f)

def update_permission(agent, key, value):
    perms = load_permissions()
    if agent in perms:
        perms[agent][key] = value
        with open(PERMISSIONS_FILE, 'w') as f:
            json.dump(perms, f, indent=4)
        return True
    return False

if __name__ == "__main__":
    # Test loading
    print("--- Loading Initial Permissions ---")
    p = load_permissions()
    print(json.dumps(p, indent=2))
    
    # Test updating (macOS Switch style)
    print("\n--- Updating 'dev' approval to False ---")
    update_permission("dev", "approval_required", False)
    print("Update successful.")
