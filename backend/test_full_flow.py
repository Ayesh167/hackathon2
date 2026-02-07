import requests
import json

def test_login():
    url = "http://127.0.0.1:8000/auth/login"
    
    # Login data
    data = {
        "email": "newuser@example.com",
        "password": "password123"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Sending login request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Login successful!")
            response_data = response.json()
            token = response_data.get("access_token")
            print(f"Token received: {token[:20]}..." if token else "No token")
            return token
        else:
            print("Login failed!")
            return None
    except Exception as e:
        print(f"Error making request: {e}")
        return None

def test_get_user_details(token):
    url = "http://127.0.0.1:8000/auth/me"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\nSending get user details request...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Get user details successful!")
            return True
        else:
            print("Get user details failed!")
            return False
    except Exception as e:
        print(f"Error making request: {e}")
        return False

def test_create_task(token):
    url = "http://127.0.0.1:8000/api/9c622aa5-1205-4b23-ab5b-2e165e2e1475/tasks"  # Using the user ID from registration
    
    data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\nSending create task request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200 or response.status_code == 201:
            print("Create task successful!")
            return True
        else:
            print("Create task failed!")
            return False
    except Exception as e:
        print(f"Error making request: {e}")
        return False

def test_chat_endpoint(token):
    url = "http://127.0.0.1:8000/api/chat"
    
    data = {
        "message": "Hello, can you help me create a test task?",
        "conversation_id": None
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\nSending chat request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Chat request successful!")
            return True
        else:
            print("Chat request failed!")
            return False
    except Exception as e:
        print(f"Error making request: {e}")
        return False

if __name__ == "__main__":
    # Test login
    token = test_login()
    
    if token:
        # Test getting user details
        test_get_user_details(token)
        
        # Test creating a task
        test_create_task(token)
        
        # Test chat endpoint
        test_chat_endpoint(token)