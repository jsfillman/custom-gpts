# docker build -t web-adventure .
# docker run -d -p 5000:5000 --name web-adventure -e OPENAI_API_KEY=$OPENAI_API_KEY web-adventure
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
    """Get an immersive opening scene for the survival adventure game."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
You are the game master of a survival adventure game. The player has been 
separated from their family in an unfamiliar world and must survive long 
enough to find them.

The game should reflect:
- **Open-world survival mechanics**: Gathering resources, crafting, 
  building shelter, and managing hunger/thirst.
- **Exploration and mystery**: Clues, radio signals, and NPCs hint at 
  where the player's family might be.
- **Dangerous encounters**: Hostile creatures, extreme weather, or 
  hidden enemies make survival difficult.
- **Dangerous nights**: Creatures and dangers come out more at night.
- **Player choices matter**: Every action (or inaction) has consequences.

Drop the player into the world with immediate tension, high stakes, and 
a reason to start exploring.
"""},

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
    app.run(host="0.0.0.0", port=5000, debug=True)
