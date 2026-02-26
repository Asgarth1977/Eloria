# bootstrap_env.py
"""
Bootstrap Script for Grimlock Portable
- Installs required Python packages automatically
- Prepares folder structure and placeholders
- Ensures portable environment is ready for first run
"""

import os
import subprocess
import sys
import json

# ----------------------------
# Configuration
# ----------------------------
PORTABLE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(PORTABLE_DIR, "config", "app_config.json")
REQUIRED_PYTHON_PACKAGES = [
    "flask",
    "requests",
    "flask_cors",
    "pywebview",
    # add other dependencies your app needs
]

REQUIRED_NODE_PACKAGES = [
    # example: if using npm frontend dependencies
    # "react", "react-dom", ...
]

# ----------------------------
# Helper functions
# ----------------------------
def install_python_packages():
    for package in REQUIRED_PYTHON_PACKAGES:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ensure_directories():
    folders = ["backend", "frontend", "memory", "config", "logs"]
    for folder in folders:
        path = os.path.join(PORTABLE_DIR, folder)
        os.makedirs(path, exist_ok=True)

def create_default_config():
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "lm_studio_host": "127.0.0.1",
            "lm_studio_port": 7860,
            "memory_path": os.path.join(PORTABLE_DIR, "memory"),
            "logs_path": os.path.join(PORTABLE_DIR, "logs"),
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)

# ----------------------------
# Main Bootstrap Execution
# ----------------------------
if __name__ == "__main__":
    print("Starting Grimlock Portable Bootstrap...")
    ensure_directories()
    install_python_packages()
    create_default_config()
    print("Bootstrap complete! You can now run `desktop.py`.")