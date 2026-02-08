from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

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
                "content": "You are a friendly English speaking tutor. Keep responses simple."
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
