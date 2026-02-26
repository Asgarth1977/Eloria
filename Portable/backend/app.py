# backend/app.py
"""
Grimlock Portable - Backend
Fully self-contained backend for portable version
"""

import os
import sys
import json
from flask import Flask
from flask_cors import CORS
import threading
import subprocess

# Import portable routes
from routes import portable_routes

# ===============================
# Configuration
# ===============================
PORTABLE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(PORTABLE_DIR, "..", "config", "app_config.json")

DEFAULT_CONFIG = {
    "lm_studio_host": "127.0.0.1",
    "lm_studio_port": 7860
}

# Ensure config exists
if not os.path.exists(CONFIG_FILE):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4)

# Load config
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

LM_HOST = config.get("lm_studio_host", "127.0.0.1")
LM_PORT = config.get("lm_studio_port", 7860)

# ===============================
# Flask app setup
# ===============================
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Register portable routes
app.register_blueprint(portable_routes)

# ===============================
# Optional: Launch LM Studio backend (if needed)
# ===============================
def launch_lm_studio():
    """
    Launch LM Studio backend process
    Only if portable app should start it automatically
    """
    backend_cmd = [
        sys.executable,
        os.path.join(PORTABLE_DIR, "..", "lm_studio_launcher.py"),
        "--host", LM_HOST,
        "--port", str(LM_PORT)
    ]
    try:
        subprocess.Popen(backend_cmd)
        print("[*] LM Studio backend launched in background")
    except Exception as e:
        print(f"[!] Failed to launch LM Studio: {e}")

# ===============================
# Start Flask server
# ===============================
if __name__ == "__main__":
    print("[*] Grimlock Portable Backend starting...")
    # Launch LM Studio in a separate thread if needed
    # threading.Thread(target=launch_lm_studio, daemon=True).start()

    app.run(host="0.0.0.0", port=5000)