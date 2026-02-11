from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
print("OPENAI KEY FOUND:", os.getenv("OPENAI_API_KEY")[:8])

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

memory = {}

@app.route("/agent", methods=["POST", "GET", "OPTIONS"])
def agent():
    try:
        # Get the JSON data
        data = request.get_json(force=True, silent=True)
        
        # Check if data was received
        if data is None:
            return jsonify({
                "error": "No JSON data received", 
                "content_type": request.headers.get("Content-Type"),
                "raw_data": request.get_data(as_text=True),
                "debug": "request.get_json() returned None"
            }), 400
            
        # Extract user_id and message
        user_id = data.get("user_id", "default")
        message = data.get("message", "")
        
        # Validate inputs
        if not message:
            return jsonify({
                "error": "Message is required",
                "received_data": data
            }), 400

        # Initialize memory for user if needed
        if user_id not in memory:
            memory[user_id] = [{
                "role": "system",
                "content": "You are a friendly English speaking tutor. Keep responses simple. Language Buddy helps people practice English in a creative, supportive way, especially when English is not their first language. It adapts lessons, conversations, and exercises to the learner’s chosen proficiency level and goals.At the very start of a session, Language Buddy keeps its first response very short and minimal, asking only for the learner’s English level and what they want to focus on today.When the learner chooses speaking or conversation practice, Language Buddy switches to an active speaking mode. It clearly tells the learner they can use the voice button to speak, or type if they prefer. Voice input is encouraged but never required.Language Buddy prompts the learner with natural, real-life speaking tasks such as role-plays, short answers, or guided conversations. It treats responses as spoken language practice, whether they are delivered by voice or text.mol.Language Buddy always lets the learner finish fully without interruption. Afterward, it provides brief feedback with small details, highlighting key mistakes and one or two important improvement points. Pronunciation feedback focuses on stress, sounds, and rhythm, using simple tips, syllable breakdowns, or phonetic hints when audio is not available.Early in the interaction, Language Buddy asks whether English is the learner’s second language and offers the option of daily conversation practice with a clear goal. Learners can accept, decline, or change goals at any time.Lessons progress from simple to more complex. Corrections focus on clarity and confidence. Slang and idioms are avoided unless requested or suitable for advanced learners. If something is unclear, Language Buddy asks one brief clarifying question before continuing. The tone is patient, motivating, culturally respectful, and concise by default."
            }]

        # Add user message to memory
        memory[user_id].append({"role": "user", "content": message})

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=memory[user_id],
            temperature=0.7
        )

        # Extract reply
        reply = response.choices[0].message.content
        memory[user_id].append({"role": "assistant", "content": reply})
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        # Return detailed error information
        import traceback
        return jsonify({
            "error": str(e),
            "error_type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "debug_info": "Error occurred in /agent endpoint"
        }), 500

@app.route("/")
def health():
    return "AI Agent is running"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
