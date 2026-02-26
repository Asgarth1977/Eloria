# grimlock_hot_reload/reloader.py

class Reloader:
    def __init__(self, webview_instance):
        self.webview = webview_instance

    def reload(self):
        """Force the WebView to fully reload from Flask, bypassing cache."""
        try:
            if self.webview:
                # Full page reload by navigating to the URL again
                self.webview.load_url("http://127.0.0.1:5000")
                print("[HotReload] WebView fully reloaded")
            else:
                print("[HotReload] WebView not ready yet")
        except Exception as e:
            print(f"[HotReload] Failed to reload WebView: {e}")