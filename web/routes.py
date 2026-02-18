# routes.py

import requests
from flask import render_template, request, jsonify
from datetime import datetime

from config import (
    LM_STUDIO_URL,
    API_KEY,
    MODELS,
    DEFAULT_MODEL,
    MEMORY_FILE
)

from memory.memory import save_memory


# ----------------------------------
# Smart Model Selection
# ----------------------------------

def smart_select_model(user_text: str) -> str:
    text = user_text.lower().strip()

    return DEFAULT_MODEL


# ----------------------------------
# LM Studio Query
# ----------------------------------

def query_lm_studio(user_text: str, model_key: str) -> str:
    model_config = MODELS.get(model_key, MODELS[DEFAULT_MODEL])

    payload = {
        "model": model_config["model_name"],
        "messages": [
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json"
    }

    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"

    try:
        response = requests.post(
            LM_STUDIO_URL,
            json=payload,
            headers=headers,
            timeout=180
        )

        response.raise_for_status()
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            return "Model returned an empty response."

    except Exception as e:
        # Failover to default model if helper fails
        if model_key != DEFAULT_MODEL:
            return query_lm_studio(user_text, DEFAULT_MODEL)

        return f"Error: Could not reach model {model_key}. {str(e)}"


# ----------------------------------
# Flask Routes
# ----------------------------------

def register_routes(app, conversation_history):

    @app.route("/")
    def index():
        return render_template("index.html", conversation=conversation_history)

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json
        user_text = data.get("text", "").strip()
        timestamp = datetime.now().isoformat()

        # Store user message
        conversation_history.append({
            "role": "user",
            "content": user_text,
            "timestamp": timestamp
        })
        save_memory(conversation_history)

        # Determine model
        model_key = smart_select_model(user_text)

        # Query LM Studio
        ai_response = query_lm_studio(user_text, model_key)

        # Store AI response
        conversation_history.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": timestamp
        })
        save_memory(conversation_history)

        return jsonify({"response": ai_response})
