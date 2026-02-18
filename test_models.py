import requests
import json

OPENROUTER_API_KEY = "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"

def test_model(model_id):
    try:
        print(f"Testing model: {model_id}")
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": model_id,
                "messages": [
                    {"role": "user", "content": "Hi"}
                ],
            })
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test a few likely free models
    test_model("mistralai/mistral-7b-instruct:free")
    test_model("google/gemma-7b-it:free")
    test_model("meta-llama/llama-3-8b-instruct:free") # Maybe the .1 was the issue
