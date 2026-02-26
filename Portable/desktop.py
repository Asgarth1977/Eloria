# run_grimlock_desktop.py
"""
Grimlock Portable Desktop Launcher
Fully automated portable startup
"""

import os
import sys
import json
import subprocess
import time
import requests
import webview

# ==============================
# Paths
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_SCRIPT = os.path.join(BASE_DIR, "backend", "app.py")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "app_config.json")
FRONTEND_PATH = os.path.join(BASE_DIR, "frontend", "index.html")

MEMORY_DIR = os.path.join(BASE_DIR, "memory")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# ==============================
# Ensure folders exist
# ==============================

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

# ==============================
# Default config (if missing)
# ==============================

DEFAULT_CONFIG = {
    "backend_host": "127.0.0.1",
    "backend_port": 5000,
    "lm_studio_host": "127.0.0.1",
    "lm_studio_port": 7860
}

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

BACKEND_HOST = config.get("backend_host", "127.0.0.1")
BACKEND_PORT = config.get("backend_port", 5000)

# ==============================
# Start backend
# ==============================

if not os.path.exists(BACKEND_SCRIPT):
    print(f"[!] Backend not found at {BACKEND_SCRIPT}")
    sys.exit(1)

print("[*] Launching backend...")

backend_process = subprocess.Popen(
    [sys.executable, BACKEND_SCRIPT],
    cwd=os.path.join(BASE_DIR, "backend")
)

# ==============================
# Wait for backend to be ready
# ==============================

print("[*] Waiting for backend to become available...")

backend_url = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/status"

for _ in range(20):  # wait up to ~10 seconds
    try:
        r = requests.get(backend_url, timeout=1)
        if r.status_code == 200:
            print("[✓] Backend is ready.")
            break
    except requests.exceptions.RequestException:
        pass
    time.sleep(0.5)
else:
    print("[!] Backend did not start in time.")
    backend_process.terminate()
    sys.exit(1)

# ==============================
# Launch Desktop Window
# ==============================

if not os.path.exists(FRONTEND_PATH):
    print(f"[!] Frontend not found at {FRONTEND_PATH}")
    backend_process.terminate()
    sys.exit(1)

print("[*] Launching Grimlock Portable Desktop...")

webview.create_window(
    "Grimlock Portable",
    FRONTEND_PATH,
    width=1000,
    height=700,
    resizable=True
)

webview.start()

# ==============================
# Cleanup when window closes
# ==============================

print("[*] Shutting down backend...")
backend_process.terminate()