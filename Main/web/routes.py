# routes.py
import json
from flask import render_template, request, jsonify, send_from_directory
from memory.memory import save_memory
from core.llm_client import LiteLLMClient
from config import EMOJI_FOLDER
from datetime import datetime
import os

# Initialize the LiteLLM client
llm_client = LiteLLMClient()

# Memory Injection Route.
injected_memory_store = {}  # key = session/user id, value = list of messages

def register_routes(app, conversation_history):
    
    @app.route("/")
    def home():
        emojis = []
        if os.path.exists(EMOJI_FOLDER):
            emojis = [f for f in os.listdir(EMOJI_FOLDER)
                      if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg"))]
        return render_template(
            "index.html",
            conversation=conversation_history,
            emojis=emojis
        )

    @app.route("/emojis/<filename>")
    def serve_emoji(filename):
        return send_from_directory(EMOJI_FOLDER, filename)

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json
        user_text = data.get("text", "").strip()
        timestamp = datetime.now().isoformat()

        # Append user message
        conversation_history.append({
            "role": "user",
            "content": user_text,
            "timestamp": timestamp
        })
        save_memory(conversation_history)

        injected_memory_text = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in conversation_history
            if msg.get("injected")
        )
        if injected_memory_text:
            user_text = f"{injected_memory_text}\n\n{user_text}"
        else:
            user_text = f"{user_text}"

        # -------------------------------
        # Build prompt & get response
        # -------------------------------
        response_text = llm_client.send_text(user_text)

        # Append AI response
        conversation_history.append({
            "role": "ai",
            "content": response_text,
            "timestamp": timestamp
        })
        save_memory(conversation_history)

        return jsonify({"response": response_text})
    
    @app.route("/inject_memory", methods=["POST"])
    def inject_memory():
        data = request.json
        memory_to_inject = data.get("memory", [])

        # Validate memory structure
        if not isinstance(memory_to_inject, list):
            return jsonify({"status": "Invalid format"}), 400
        
        # Mark messages as injected and append to conversation history
        for msg in memory_to_inject:
            if "role" in msg and "content" in msg:
                msg["injected"] = True  # Mark as injected
            else:
                return jsonify({"status": "Invalid message format"}), 400

        # Append temporarily to conversation (do not save permanently)
        conversation_history.extend(memory_to_inject)
        return jsonify({"status": "Memory injected successfully"})