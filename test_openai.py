import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {api_key[:10]}...{api_key[-4:] if api_key else 'None'}")

# Test OpenAI connection
try:
    client = OpenAI(api_key=api_key)
    
    # Try a simple completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Say hello in one word"}
        ],
        max_tokens=5
    )
    
    print("✅ SUCCESS: OpenAI API is working!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"Error type: {type(e).__name__}")