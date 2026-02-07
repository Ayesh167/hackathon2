import requests
import json

# Test the authentication and chat functionality
def test_auth_and_chat():
    base_url = "http://127.0.0.1:8000"
    
    # Step 1: Register a new user
    print("Step 1: Registering a new user...")
    register_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    register_response = requests.post(f"{base_url}/auth/register", json=register_data)
    print(f"Register Status: {register_response.status_code}")
    
    if register_response.status_code == 200:
        register_json = register_response.json()
        token = register_json.get("access_token")
        print("Registration successful!")
        print(f"Token: {token[:20]}..." if token else "No token")
    else:
        print(f"Registration failed: {register_response.text}")
        # Try logging in if user already exists
        print("\nTrying to login instead...")
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"Login Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_json = login_response.json()
            token = login_json.get("access_token")
            print("Login successful!")
            print(f"Token: {token[:20]}..." if token else "No token")
        else:
            print(f"Login failed: {login_response.text}")
            return False
    
    # Step 2: Use the token to access protected endpoints
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\nStep 2: Testing protected endpoints with token...")
    
    # Test getting user details
    user_response = requests.get(f"{base_url}/auth/me", headers=headers)
    print(f"Get user details Status: {user_response.status_code}")
    if user_response.status_code == 200:
        print("User details retrieved successfully!")
    else:
        print(f"Failed to get user details: {user_response.text}")
    
    # Step 3: Test the chat endpoint
    print("\nStep 3: Testing chat endpoint...")
    chat_data = {
        "message": "Hello, can you help me create a test task?",
        "conversation_id": None
    }
    
    chat_response = requests.post(f"{base_url}/api/chat", headers=headers, json=chat_data)
    print(f"Chat Status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        print("Chat request successful!")
        print(f"Response: {chat_response.json()}")
    else:
        print(f"Chat request failed: {chat_response.text}")
    
    return True

if __name__ == "__main__":
    test_auth_and_chat()