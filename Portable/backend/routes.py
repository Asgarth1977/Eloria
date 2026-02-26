# backend/routes_portable.py
"""
Grimlock Portable Routes
- Minimal backend API for portable version
- Avoids local-only dependencies
"""

from flask import Blueprint, jsonify, request

# Create a blueprint for portable routes
portable_routes = Blueprint("portable_routes", __name__)

@portable_routes.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "Grimlock Portable Backend Running"})

@portable_routes.route("/api/test", methods=["POST"])
def test():
    data = request.json or {}
    return jsonify({"received": data, "message": "This is a portable test route"})