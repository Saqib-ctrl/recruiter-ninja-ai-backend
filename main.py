from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
client = OpenAI(api_key=OPENAI_API_KEY)


# AI-powered bio generator
@app.route("/generate_bio", methods=["POST"])
def generate_bio():
    try:
        data = request.get_json()
        candidate_info = data.get("candidate_info", "")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Generate a professional candidate bio for: {candidate_info}"}
            ]
        )
        return jsonify({"bio": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# AI-powered candidate recommendation
@app.route("/recommend_candidates", methods=["POST"])
def recommend_candidates():
    try:
        data = request.get_json()
        job_description = data.get("job_description", "")
        candidates = data.get("candidates", [])

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": f"Recommend the best candidates for: {job_description}. Candidates: {', '.join(candidates)}"}
            ]
        )
        return jsonify({"recommended_candidates": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# AI-powered contract generator
@app.route("/generate_contract", methods=["POST"])
def generate_contract():
    try:
        data = request.get_json()
        contract_prompt = f"Create a contract for {data.get('candidate_name', '')} as {data.get('position', '')} with a salary of {data.get('salary', '')}."

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": contract_prompt}
            ]
        )
        return jsonify({"contract": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# AI-powered job filtering
@app.route("/filter_jobs", methods=["POST"])
def filter_jobs():
    try:
        data = request.get_json()
        job_listings = data.get("job_listings", [])
        criteria = data.get("criteria", "")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user",
                 "content": f"Filter job listings that match this criteria: {criteria}. Jobs: {', '.join(job_listings)}"}
            ]
        )
        return jsonify({"filtered_jobs": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
