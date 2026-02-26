# routes.py
import requests
from flask import render_template, request, jsonify
from datetime import datetime
from config import LM_STUDIO_URL, API_KEY, MODELS, DEFAULT_MODEL
from memory.memory_manager import MemoryManager

# ----------------------------------
# Smart Model Selection
# ----------------------------------
def smart_select_model(user_text: str) -> str:
    return DEFAULT_MODEL

# ----------------------------------
# LM Studio Query
# ----------------------------------
def query_lm_studio(user_text: str, model_key: str) -> str:
    model_config = MODELS.get(model_key, MODELS[DEFAULT_MODEL])
    payload = {
        "model": model_config["model_name"],
        "messages": [{"role": "user", "content": user_text}],
        "temperature": 0.7
    }
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, headers=headers, timeout=300)
        response.raise_for_status()
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        return "Model returned an empty response."
    except Exception as e:
        if model_key != DEFAULT_MODEL:
            return query_lm_studio(user_text, DEFAULT_MODEL)
        return f"Error: Could not reach model {model_key}. {str(e)}"

# ----------------------------------
# Flask Routes
# ----------------------------------
def register_routes(app, memory_manager: MemoryManager):
    @app.route("/")
    def index():
        return render_template("index.html", conversation=memory_manager.get_history())

    @app.route("/load_3_days", methods=["POST"])
    def load_3_days():
        try:
            messages = memory_manager.get_last_days_messages(3)
            return jsonify({"success": True, "messages": messages})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    @app.route("/summarize_now", methods=["POST"])
    def summarize_now():
        try:
            summary = memory_manager.summarize_day()
            return jsonify({"success": True, "summary": summary})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json
        user_text = data.get("text", "").strip()
        timestamp = datetime.now().isoformat()
        memory_manager.add_message("user", user_text, timestamp)
        model_key = smart_select_model(user_text)
        ai_response = query_lm_studio(user_text, model_key)
        memory_manager.add_message("assistant", ai_response, timestamp)
        return jsonify({"response": ai_response})
