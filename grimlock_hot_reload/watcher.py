# grimlock_hot_reload/watcher.py

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import WATCH_PATHS, WATCH_EXTENSIONS, RELOAD_DELAY
from .reloader import Reloader

class HotReloadHandler(FileSystemEventHandler):
    def __init__(self, reloader):
        super().__init__()
        self.reloader = reloader

    def on_modified(self, event):
        if event.src_path.endswith(WATCH_EXTENSIONS):
            time.sleep(RELOAD_DELAY)
            self.reloader.reload()

def start_hot_reload(webview_instance):
    """Start watching Grimlock project files and reload WebView on changes."""
    reloader = Reloader(webview_instance)
    event_handler = HotReloadHandler(reloader)
    observer = Observer()

    for path in WATCH_PATHS:
        observer.schedule(event_handler, path=path, recursive=True)

    observer.start()
    print("[HotReload] Watching files for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()