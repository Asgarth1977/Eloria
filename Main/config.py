
# This is the Config File, when fixed DO NOT TOUCH THIS FILE, 
# unless you know what you are doing.

import os

# -------------------------------
#              Config
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEMORY_FOLDER = os.path.join(BASE_DIR, "memory")
os.makedirs(MEMORY_FOLDER, exist_ok=True)
MEMORY_FILE = os.path.join(MEMORY_FOLDER, "eloria_memory.json")

LITELLM_API_KEY = "sk-1234"  # Your LiteLLM API key
LITELLM_URL = "http://localhost:4000/chat/completions"

EMOJI_FOLDER = os.path.join(BASE_DIR, "emojis")