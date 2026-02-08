import requests
import json
import time
import uuid

def test_ai_assistant_locally():
    print("Testing AI Assistant locally...")
    
    # Register a test user
    register_url = 'http://127.0.0.1:8000/auth/register'
    unique_email = f'testuser_{int(time.time())}@example.com'
    register_data = {
        'email': unique_email,
        'password': 'password123',
        'name': 'Test User'
    }

    print(f"Registering user with email: {unique_email}")
    register_response = requests.post(register_url, json=register_data)
    print(f"Registration status: {register_response.status_code}")
    
    if register_response.status_code != 200:
        print(f"Registration failed: {register_response.text}")
        return

    # Login
    login_url = 'http://127.0.0.1:8000/auth/login'
    login_data = {
        'email': unique_email,
        'password': 'password123'
    }

    login_response = requests.post(login_url, json=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return

    token = login_response.json()['access_token']
    print("Login successful, got token")
    
    # Test headers
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test basic AI assistant functionality
    test_cases = [
        {"message": "Add a task to buy groceries", "description": "Adding a task"},
        {"message": "Show me my tasks", "description": "Listing tasks"},
        {"message": "Create a task to walk the dog", "description": "Creating another task"},
        {"message": "What can you do?", "description": "Asking for capabilities"}
    ]
    
    chat_url = 'http://127.0.0.1:8000/api/chat'
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"Input: {test_case['message']}")
        
        chat_data = {
            'message': test_case['message'],
            'conversation_id': None
        }
        
        try:
            chat_response = requests.post(chat_url, headers=headers, json=chat_data)
            print(f"Status Code: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"AI Response: {response_data['response']}")
                print(f"Conversation ID: {response_data['conversation_id']}")
            else:
                print(f"Error: {chat_response.text}")
        except Exception as e:
            print(f"Exception: {e}")
    
    print("\nAI Assistant test completed!")

if __name__ == "__main__":
    test_ai_assistant_locally()