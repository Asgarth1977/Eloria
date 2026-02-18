# config.py
# -------------------------------
# Eloria Local AI Configuration
# Direct LM Studio usage (no LiteLLM)
# -------------------------------

import os

# -------------------------------
# Base Directories
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MEMORY_FOLDER = os.path.join(BASE_DIR, "memory")
os.makedirs(MEMORY_FOLDER, exist_ok=True)
MEMORY_FILE = os.path.join(MEMORY_FOLDER, "conversation.json")

# -------------------------------
# LM Studio Settings
# -------------------------------
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
API_KEY = "sk-1234"  # optional if LM Studio requires auth

# -------------------------------
# Model Configuration
# -------------------------------
# Each model has: model_name (LM Studio), max_tokens, optional id
MODELS = {
    "Eloria": {
        "model_name": "mistralai/ministral-3-14b-reasoning",
        "id": "eloria-voice"
    },
}

# -------------------------------
# Global Settings
# -------------------------------
GENERAL_SETTINGS = {
    "master_key": "sk-1234"
}

# -------------------------------
# Routing / Defaults
# -------------------------------
# Default user-facing model: Eloria
DEFAULT_MODEL = "Eloria"