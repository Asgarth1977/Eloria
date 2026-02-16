#    Main app.py file.
#    This file initializes the Flask application, sets up routes, and starts the desktop WebView window.

import threading
import webview
from flask import Flask
from web.routes import register_routes
from memory.memory import load_memory
from memory.memory_watcher import MemoryWatcher
# -------------------------------
# Flask app for Web UI
# -------------------------------

app = Flask(__name__)

# Initialize conversation history and memory watcher
conversation_history = load_memory()

# Start memory watcher in a separate thread
memory_watcher = MemoryWatcher(conversation_history)
memory_watcher.start()

# Register routes
register_routes(app, conversation_history)

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=start_flask, daemon=True).start()
    
    # Start desktop WebView window
    webview.create_window("Eloria Local AI", "http://127.0.0.1:5000", width=500, height=900)
    
    # Keep the script alive while the window is open
    webview.start()  # <-- this blocks until the window is closed
