import os
import json
from datetime import datetime
from config import MEMORY_FOLDER


def get_memory_file(date=None):
    """
    Returns the memory file path for today or a specific date.
    """
    if date is None:
        date = datetime.now().date()

    filename = f"{date.strftime('%Y-%m-%d')}.json"
    return os.path.join(MEMORY_FOLDER, filename)


def load_memory(date=None):
    """
    Load memory for given date (defaults to today).
    """
    path = get_memory_file(date)

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"[Memory] File {path} is corrupt. Starting fresh.")
        return []


def save_memory(conversation, date=None):
    """
    Save memory to given date file (defaults to today).
    """
    path = get_memory_file(date)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Memory] Could not save memory: {e}")
