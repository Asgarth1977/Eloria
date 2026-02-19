from memory.memory_manager import MemoryManager
from memory.memory_core import load_memory
from datetime import datetime, timedelta
import os

# Mock conversation history
conversation_history = [
    {"role": "user", "content": "Hello Eloria!", "timestamp": datetime.now().isoformat()},
    {"role": "assistant", "content": "Hello! How can I assist you today?", "timestamp": datetime.now().isoformat()},
]

# Initialize MemoryManager
mm = MemoryManager(conversation_history)

# -------------------------------
# Test saving today's memory
# -------------------------------
mm.save_current()
print("Saved current conversation to today's memory.")

# -------------------------------
# Test loading yesterday's memory
# -------------------------------
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
yesterday_memory = mm.load_yesterday()
print(f"Loaded yesterday's memory ({yesterday}):")
print(yesterday_memory)

# -------------------------------
# Test injecting a memory file
# -------------------------------
# Create a dummy JSON for injection
dummy_file = os.path.join(os.path.dirname(__file__), "memory", "memories", "dummy.json")
with open(dummy_file, "w", encoding="utf-8") as f:
    f.write('[{"role":"user","content":"Injected memory test","timestamp":"2026-02-18T12:00:00"}]')

mm.inject_memory_file(dummy_file)
print("Injected dummy memory file.")
print("Current conversation after injection:")
print(conversation_history)

# -------------------------------
# Test summarization
# -------------------------------
summary = mm.summarize_day()
print("Summary of today’s memory:")
print(summary)
