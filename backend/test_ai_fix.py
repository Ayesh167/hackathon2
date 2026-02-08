import requests
import json

def test_ai_assistant_offline_mode():
    """
    Test the AI assistant with the improved offline mode functionality.
    This test verifies that the assistant works even without a Gemini API key.
    """
    print("Testing AI Assistant in offline mode...")
    
    # Test the chat endpoint without authentication to check general functionality
    url = "http://127.0.0.1:8000/"
    response = requests.get(url)
    print(f"Server status: {response.status_code}")
    print(f"Server response: {response.json()}")
    
    # Since we need a registered user to test the chat functionality,
    # let's test the registration first
    register_url = "http://127.0.0.1:8000/auth/register"
    register_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    print("\nRegistering a test user...")
    try:
        register_response = requests.post(register_url, json=register_data)
        print(f"Registration status: {register_response.status_code}")
        if register_response.status_code == 200:
            print("User registered successfully")
        else:
            print(f"Registration response: {register_response.text}")
    except Exception as e:
        print(f"Error registering user: {e}")
        return
    
    # Now try to login
    login_url = "http://127.0.0.1:8000/auth/login"
    login_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    print("\nLogging in...")
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Login status: {login_response.status_code}")
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("Login successful!")
        else:
            print(f"Login response: {login_response.text}")
            return
    except Exception as e:
        print(f"Error logging in: {e}")
        return
    
    # Now test the chat functionality
    chat_url = "http://127.0.0.1:8000/api/chat"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    test_messages = [
        "Hello",
        "Create a task to buy groceries",
        "Show me my tasks",
        "What can you do?",
        "How are you?"
    ]
    
    print("\nTesting chat functionality...")
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i}: {message} ---")
        
        chat_data = {
            "message": message,
            "conversation_id": None
        }
        
        try:
            chat_response = requests.post(chat_url, headers=headers, json=chat_data)
            print(f"Chat response status: {chat_response.status_code}")
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"AI Response: {response_data['response']}")
                print(f"Conversation ID: {response_data['conversation_id']}")
            else:
                print(f"Chat error: {chat_response.text}")
        except Exception as e:
            print(f"Error in chat test: {e}")
    
    print("\nAI Assistant offline mode test completed!")

if __name__ == "__main__":
    test_ai_assistant_offline_mode()