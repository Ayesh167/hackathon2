import requests
import json

def test_ai_assistant():
    # Login first to get a token
    login_url = "http://127.0.0.1:8000/auth/login"
    login_data = {
        "email": "newuser@example.com",
        "password": "password123"
    }
    
    print("Logging in to get token...")
    login_response = requests.post(login_url, json=login_data, headers={"Content-Type": "application/json"})
    
    if login_response.status_code != 200:
        print("Login failed!")
        return
    
    token = login_response.json()["access_token"]
    print("Login successful! Got token.")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test different types of requests
    test_cases = [
        {"message": "Hello", "description": "Simple greeting"},
        {"message": "Hi there!", "description": "Another greeting"},
        {"message": "What can you do?", "description": "Asking for capabilities"},
        {"message": "Create a task to buy groceries", "description": "Creating a task"},
        {"message": "Show me my tasks", "description": "Listing tasks"},
        {"message": "How are you?", "description": "Asking about the assistant"}
    ]
    
    chat_url = "http://127.0.0.1:8000/api/chat"
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"Input: {test_case['message']}")
        
        data = {
            "message": test_case["message"],
            "conversation_id": None
        }
        
        try:
            response = requests.post(chat_url, headers=headers, json=data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"Response: {response_data['response']}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_ai_assistant()