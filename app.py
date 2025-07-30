from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# === OpenAI API Key ===
openai.api_key = os.getenv('OPENAI_API_KEY')

# === Twitter API Setup ===
auth = tweepy.OAuth1UserHandler(
    "7RHZ8QbyXlAcrJzMrTli5QdD4",  # API Key
    "fIfbEmExlLpJk1qEU8ZRSB4vkKNOgyst5IE2QDxfriiYGUxLsq",  # API Secret
    "1921236407311626240-w3LUisOEiitQsSieJulDZRuMCsrset",  # Access Token
    "jsyFTOjTa116gIjbSxp8NvyuaxZaRpJaQ3VpCta6wjdn7"  # Access Secret
)
twitter_api = tweepy.API(auth)

@app.route('/')
def home():
    return render_template('social-form.html')

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        age = data.get("age")
        country = data.get("country")
        state = data.get("state")
        interest = data.get("interest")
        tone = data.get("tone")
        perspective = data.get("perspective")
        hookline = data.get("hookline")

        prompt = f"Generate a {tone} social media post for a {age}-year-old from {state}, {country}, interested in {interest}. The perspective should be {perspective}. Start with: \"{hookline}\""

        # ✅ FIXED OpenAI call
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a social media content expert."},
                {"role": "user", "content": prompt}
            ]
        )
        post = response.choices[0].message.content.strip()

        return jsonify({
            "success": True,
            "prompt": prompt,
            "post": post
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == '__main__':
    app.run(debug=True)
