# memory_core.py
import os
import json
from datetime import datetime
from config import MEMORY_FOLDER

# Ensure memory folder exists
os.makedirs(MEMORY_FOLDER, exist_ok=True)

# -------------------------------
# File Path Utilities
# -------------------------------

def get_memory_file_for_date(date: datetime) -> str:
    """Return the memory file path for a specific date."""
    date_str = date.strftime("%Y-%m-%d")
    return os.path.join(MEMORY_FOLDER, f"{date_str}.json")

def get_today_memory_file() -> str:
    """Return today's memory file path and create it if it doesn't exist."""
    file_path = get_memory_file_for_date(datetime.now())
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
    return file_path

# -------------------------------
# Load / Save Memory
# -------------------------------

def load_memory(file_path: str = None) -> list:
    """Load memory from a given file path, or today's memory if none provided."""
    if file_path is None:
        file_path = get_today_memory_file()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"[Memory Core] Memory file {file_path} corrupt. Starting fresh.")
        return []

def save_memory(conversation: list, file_path: str = None):
    """Save memory to a given file path, or today's memory if none provided."""
    if file_path is None:
        file_path = get_today_memory_file()
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(conversation, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Memory Core] Could not save memory: {e}")

# -------------------------------
# Recall Older Memories
# -------------------------------

def recall_memory(date_str: str) -> list:
    """
    Load memory from a specific date.
    Example date_str format: '2026-02-12'
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        file_path = get_memory_file_for_date(dt)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            print(f"[Memory Core] No memory file found for {date_str}.")
            return []
    except ValueError:
        print("[Memory Core] Invalid date format. Use YYYY-MM-DD.")
        return []

# -------------------------------
# List Available Memory Files
# -------------------------------

def list_memory_files() -> list:
    """Return a sorted list of available memory dates as strings."""
    files = [f for f in os.listdir(MEMORY_FOLDER) if f.endswith(".json")]
    dates = [os.path.splitext(f)[0] for f in files]
    return sorted(dates)
