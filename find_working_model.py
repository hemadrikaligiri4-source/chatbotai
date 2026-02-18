import requests
import json

OPENROUTER_API_KEY = "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"

def find_working_free_model():
    try:
        print("Fetching models...")
        response = requests.get("https://openrouter.ai/api/v1/models")
        if response.status_code != 200:
            print("Failed to fetch list")
            return
        
        models = response.json()['data']
        free_models = [m['id'] for m in models if 'free' in m['id']]
        print(f"Testing {len(free_models)} models...")
        
        for model_id in free_models:
            print(f"  Testing {model_id}...", end=" ")
            res = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": model_id,
                    "messages": [{"role": "user", "content": "hi"}],
                })
            )
            if res.status_code == 200:
                print("SUCCESS!")
                return model_id
            else:
                print(f"FAILED ({res.status_code})")
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    working_model = find_working_free_model()
    if working_model:
        print(f"### WORKING MODEL: {working_model} ###")
    else:
        print("No working free model found.")
