"""
Groq Chatbot Server
-------------------
Runs a local web server that:
  1. Serves the chatbot frontend at http://localhost:5000
  2. Proxies API calls to Groq (so your key stays safe & no CORS issues)

Usage:
  pip install flask flask-cors requests
  python server.py
Then open: http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder=".")
CORS(app)

API_KEY  = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# ── Serve the frontend ──────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# ── Proxy endpoint ──────────────────────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No JSON body"}), 400

    try:
        res = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type":  "application/json",
            },
            json=payload,
            timeout=30,
        )
        return jsonify(res.json()), res.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": {"message": "Request timed out"}}), 504
    except Exception as e:
        return jsonify({"error": {"message": str(e)}}), 500

# ── Run ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n  ✓ Chatbot running at → http://localhost:{port}\n")
    app.run(debug=False, port=port)
