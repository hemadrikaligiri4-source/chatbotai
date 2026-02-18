import requests
import json

def test_local_chat():
    # 1. Login
    login_url = "http://127.0.0.1:5000/login"
    login_data = {"email": "test@example.com", "password": "password"}
    
    # First, let's register if not exists
    requests.post("http://127.0.0.1:5000/register", json={"full_name": "Test User", "email": "test@example.com", "password": "password"})
    
    session = requests.Session()
    login_res = session.post(login_url, json=login_data)
    print(f"Login Status: {login_res.status_code}")
    
    if login_res.status_code == 200:
        # 2. Chat
        chat_url = "http://127.0.0.1:5000/chat"
        chat_data = {"message": "Tell me about Java programming."}
        chat_res = session.post(chat_url, json=chat_data)
        print(f"Chat Status: {chat_res.status_code}")
        print(f"Chat Response: {chat_res.json()}")

if __name__ == "__main__":
    test_local_chat()
