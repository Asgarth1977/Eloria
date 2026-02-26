#    Main app.py file.
#    This file initializes the Flask application, sets up routes, and starts the desktop WebView window.

import threading
import webview
from flask import Flask
from web.routes import register_routes
from memory import memory_manager
from memory.memory_manager import MemoryManager

# -------------------------------
# Flask app for Web UI
# -------------------------------

app = Flask(__name__)

# Conversation history is shared between Flask routes and MemoryManager
# -------------------------------
# Initialize MemoryManager & Watcher
# -------------------------------
memory_manager = MemoryManager()
# MemoryWatcher is already started inside MemoryManager.__init__()

# Register routes
register_routes(app, memory_manager)

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=start_flask, daemon=True).start()
    
    # Start desktop WebView window
    webview.create_window("Project Grimlock", "http://127.0.0.1:5000", width=1200, height=800)
    
    # Keep the script alive while the window is open
    webview.start()  # <-- this blocks until the window is closed
