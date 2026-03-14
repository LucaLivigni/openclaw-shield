#!/usr/bin/env python3
"""
OpenClaw Shield - Dashboard Server
Includes temp permissions, fs map, and rollback support.
"""

import json
import os
import time
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config.json"
DASHBOARD_DIR = BASE_DIR / "dashboard"
WORKSPACE_DIR = Path(os.environ.get("HOME", "/tmp")) / ".openclaw" / "workspace-dev"

def enforce_expirations():
    try:
        if not CONFIG_PATH.exists(): return
        with open(CONFIG_PATH, 'r') as f: config = json.load(f)
        changed = False
        now = time.time()
        
        for agent, data in config.get("agents", {}).items():
            if "expirations" in data:
                expired = []
                for key, exp_time in data["expirations"].items():
                    if now > exp_time:
                        if key == "approval_required": data[key] = True
                        elif key == "terminal": data[key] = "RESTRICTED"
                        expired.append(key)
                for k in expired:
                    del data["expirations"][k]
                    changed = True

        if changed:
            with open(CONFIG_PATH, 'w') as f: json.dump(config, f, indent=2)
    except Exception as e:
        print("Expiration check failed:", e)

class ShieldHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self):
        enforce_expirations()
        if self.path == '/api/config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            try:
                with open(CONFIG_PATH, 'r') as f:
                    config_data = f.read()
                self.wfile.write(config_data.encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        elif self.path == '/api/fs':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            try:
                tree = self._build_tree(WORKSPACE_DIR)
                self.wfile.write(json.dumps(tree).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            if self.path == '/':
                self.path = '/index.html'
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/config':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                new_config = json.loads(post_data.decode('utf-8'))
                with open(CONFIG_PATH, 'w') as f:
                    json.dump(new_config, f, indent=2)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
                
        elif self.path == '/api/rollback':
            try:
                # Rollback using git
                subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=WORKSPACE_DIR, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "Rollback successful."}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Failed to rollback: " + str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def _build_tree(self, path: Path):
        name = path.name
        if path.is_dir():
            try:
                children = [self._build_tree(child) for child in path.iterdir() if not child.name.startswith('.')]
                return {"name": name, "type": "directory", "children": children}
            except PermissionError:
                return {"name": name, "type": "directory", "children": []}
        else:
            return {"name": name, "type": "file"}

def run(server_class=HTTPServer, handler_class=ShieldHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🛡️  OpenClaw Shield Dashboard running at http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("\nServer stopped.")

if __name__ == '__main__':
    run()
