# memory_watcher.py
# Memory Watcher - Eloria AI Assistant

import threading
import time
from datetime import datetime

class MemoryWatcher:
    """
    Watches the system clock and automatically triggers
    the MemoryManager to switch to a new day's memory.
    """

    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.current_date = datetime.now().date()
        self.running = False
        self.lock = threading.Lock()

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
                with self.lock:
                    print(f"[MemoryWatcher] New day detected: {now}. Switching memory file.")
                    # Let MemoryManager handle the new day
                    self.memory_manager.start_new_day()
                    self.current_date = now
