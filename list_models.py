import requests

def list_models():
    try:
        print("Fetching model list from OpenRouter...")
        response = requests.get("https://openrouter.ai/api/v1/models")
        if response.status_code == 200:
            models = response.json()['data']
            free_models = [m['id'] for m in models if 'free' in m['id']]
            print(f"Found {len(free_models)} free models:")
            for m in free_models:
                print(f"- {m}")
        else:
            print(f"Failed to fetch models: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_models()
