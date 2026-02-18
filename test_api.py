import requests
import json

OPENROUTER_API_KEY = "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"

def test_api():
    try:
        print("Testing OpenRouter API connection...")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:5000", # Optional, for OpenRouter rank
                "X-Title": "Hemadri Chatbot", # Optional
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
            })
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
