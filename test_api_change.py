import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test the API change
try:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[{"role": "user", "content": "Hello"}]
    )
    
    print("✅ Success! Response:", response.output_text)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Test the correct API call
    print("\n🔧 Testing correct API call:")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}]
        )
        print("✅ Correct API works:", response.choices[0].message.content)
    except Exception as e2:
        print(f"❌ Even correct API fails: {e2}")