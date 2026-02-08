import requests
import json

# Test the Flask endpoint
url = "http://127.0.0.1:5000/agent"
data = {
    "user_id": "test_user", 
    "message": "Hello, can you help me learn English?"
}

print("Testing Flask endpoint...")
print(f"URL: {url}")
print(f"Data: {data}")

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✅ SUCCESS: {response.json()}")
    else:
        print(f"❌ ERROR: {response.text}")
        
except Exception as e:
    print(f"❌ REQUEST FAILED: {e}")

# Also test the health endpoint
print("\nTesting health endpoint...")
try:
    health_response = requests.get("http://127.0.0.1:5000/")
    print(f"Health Status: {health_response.status_code}")
    print(f"Health Response: {health_response.text}")
except Exception as e:
    print(f"Health check failed: {e}")