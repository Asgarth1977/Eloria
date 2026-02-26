# Memory Watcher - Eloria AI Assistant

import threading
import time
from datetime import datetime
from memory.memory import load_memory, save_memory

class MemoryWatcher:
    """
    Watches the system clock and automatically creates a new memory file
    when a new day starts. Keeps conversation_history updated.
    """

    def __init__(self, conversation_history):
        self.current_date = datetime.now().date()
        self.conversation_history = conversation_history
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._watch_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False

    def _watch_loop(self):
        while self.running:
            time.sleep(30)  # Check every 30 seconds
            now = datetime.now().date()
            if now != self.current_date:
                # Midnight passed, switch to new day's memory
                with self.lock:
                    print(f"[MemoryWatcher] New day detected: {now}. Switching memory file.")
                    # Save the previous day's memory
                    save_memory(self.conversation_history)
                    # Load new day's memory
                    self.conversation_history.clear()
                    self.conversation_history.extend(load_memory())
                    self.current_date = now
