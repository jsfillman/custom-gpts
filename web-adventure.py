from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing API Key. Set OPENAI_API_KEY as an environment variable.")

client = OpenAI(api_key=api_key)

conversation_history = [
    {"role": "system", "content": "You are an interactive sci-fi text adventure game master with Ozzie's chill but sharp attitude."}
]

def get_intro():
    """Get an immersive opening scene from GPT with Commonwealth-specific details."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are Ozzie, the legendary explorer and game master of the Commonwealth universe..."},
            {"role": "user", "content": "Describe the player's starting point with tension, stakes, and rich details."}
        ]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html', show_input=False)

@app.route('/start', methods=['POST'])
def start():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": "You are an interactive sci-fi text adventure game master with Ozzie's chill but sharp attitude."}
    ]
    intro_text = get_intro()
    conversation_history.append({"role": "assistant", "content": intro_text})
    return jsonify({"response": intro_text, "show_input": True})

@app.route('/input', methods=['POST'])
def user_input():
    global conversation_history
    user_text = request.json.get("text", "")
    if user_text.lower() in ["exit", "quit"]:
        return jsonify({"response": "The adventure ends... for now. 👋"})
    
    conversation_history.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(model="gpt-4o-mini", messages=conversation_history)
    answer = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": answer})
    
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
