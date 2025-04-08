from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided."}), 400

    prompt = (
        f"You are a helpful assistant that explains things clearly in a step-by-step way.\\n"
        f"Question: {query}\\n"
        f"Answer in a numbered list of steps."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You provide step-by-step answers to tech-related questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        answer = response.choices[0].message.content
        steps = [step.strip() for step in answer.split("\\n") if step.strip()]

        return jsonify({"steps": steps})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

