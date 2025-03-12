from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os, traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


# AI-powered bio generator
@app.route("/generate_bio", methods=["POST"])
def generate_bio():
    try:
        print(f"🚀 Received {request.method} request on /generate_bio")  # Debugging

        if request.method != "POST":
            return jsonify({"error": "This endpoint only accepts POST requests"}), 405

        data = request.get_json()
        candidate_info = data.get("candidate_info", "")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": candidate_info}
            ]
        )
        return jsonify({"bio": completion.choices[0].message.content})
    except Exception as e:
        print("🚨 Error in /generate_bio:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# API test endpoint
@app.route("/test_ai", methods=["GET"])
def test_ai():
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "write a haiku about AI"}
            ]
        )
        return jsonify({"haiku": completion.choices[0].message.content})
    except Exception as e:
        print("🚨 Error in /test_ai:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
