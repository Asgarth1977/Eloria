# memory_manager.py
from datetime import datetime, timedelta
import os
import json
from config import MEMORY_FOLDER
from .memory_core import get_memory_file_for_date, load_memory, save_memory
from .memory_watcher import MemoryWatcher
from .memory_summarizer import summarize_conversation, summarize_multiple_days

class MemoryManager:
    def __init__(self):
        self.conversation_history = []
        yesterday = self.load_yesterday() or []
        today = load_memory() or []
        self.conversation_history.extend(yesterday + today)

        self.watcher = MemoryWatcher(self)
        self.watcher.start()

        self.daily_summary_file = os.path.join(MEMORY_FOLDER, "summaries", "memory_summarization.json")
        os.makedirs(os.path.dirname(self.daily_summary_file), exist_ok=True)

    def get_history(self):
        return self.conversation_history

    def add_message(self, role: str, content: str, timestamp: str):
        self.conversation_history.append({"role": role, "content": content, "timestamp": timestamp})
        self.save_current()

    def save_current(self):
        save_memory(self.conversation_history)

    def start_new_day(self):
        self.conversation_history.clear()
        self.conversation_history.extend(load_memory() or [])

    def load_yesterday(self):
        yesterday_file = get_memory_file_for_date(datetime.now().date() - timedelta(days=1))
        return load_memory(yesterday_file) or []

    def get_last_days_messages(self, days: int = 3):
        """
        Retrieve messages from the last 'days' memory files before yesterday.
        Skips missing or corrupted files gracefully.
        """
        messages = []
        valid_files = 0

        # Start 2 days ago (day before yesterday) and go backwards
        for i in range(2, 2 + days):
            date = datetime.now().date() - timedelta(days=i)
            memory_file = get_memory_file_for_date(date)

            if os.path.exists(memory_file):
                try:
                    day_memory = load_memory(memory_file)
                    if isinstance(day_memory, list) and day_memory:
                        messages.extend(day_memory)
                        valid_files += 1
                    else:
                        print(f"[MemoryManager] Skipping {memory_file}: invalid or empty list")
                except Exception as e:
                    print(f"[MemoryManager] Skipping corrupted file {memory_file}: {e}")
            else:
                print(f"[MemoryManager] Memory file not found: {memory_file}")

        if not messages:
            print(f"[MemoryManager] No valid messages found in the {days} files before yesterday.")
        else:
            print(f"[MemoryManager] Loaded messages from {valid_files} valid memory file(s).")

        return messages

    def inject_memory_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.conversation_history.extend(data)
        self.save_current()

    def summarize_day(self, date: datetime = None) -> str:
        date = date or datetime.now()
        day_memory = load_memory(get_memory_file_for_date(date)) or []
        summary = summarize_conversation(day_memory)
        self._update_daily_summary_file(date, summary)
        return summary

    def summarize_week(self, days: int = 7) -> str:
        summaries = []
        for i in range(1, days + 1):
            day_file = get_memory_file_for_date(datetime.now().date() - timedelta(days=i))
            if os.path.exists(day_file):
                day_memory = load_memory(day_file) or []
                if day_memory:
                    summaries.append(day_memory)
        return summarize_multiple_days(summaries)

    def _update_daily_summary_file(self, date: datetime, summary: str):
        all_summaries = {}
        if os.path.exists(self.daily_summary_file):
            try:
                with open(self.daily_summary_file, "r", encoding="utf-8") as f:
                    all_summaries = json.load(f)
            except json.JSONDecodeError:
                print("[MemoryManager] Daily summary file corrupt. Starting fresh.")
        all_summaries[date.strftime("%Y-%m-%d")] = summary
        with open(self.daily_summary_file, "w", encoding="utf-8") as f:
            json.dump(all_summaries, f, indent=2, ensure_ascii=False)
