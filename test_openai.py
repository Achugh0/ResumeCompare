
import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Testing API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("ERROR: No API key found in .env")
    exit(1)

openai.api_key = api_key

try:
    print("Sending test request to gpt-4o-mini...")
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, respond with 'API_OK' if you see this."}],
        max_tokens=10
    )
    print(f"SUCCESS! Response: {resp.choices[0].message.content}")
except Exception as e:
    print(f"FAILED! Error Type: {type(e).__name__}")
    print(f"Error Message: {e}")
