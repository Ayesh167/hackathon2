import requests
import json

# Test the registration endpoint with a fresh email
def test_registration():
    url = "http://127.0.0.1:8000/auth/register"
    
    # Test data with a unique email
    data = {
        "email": "newuser@example.com",
        "password": "password123",
        "name": "New User"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Sending registration request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("Registration successful!")
            return True
        else:
            print("Registration failed!")
            return False
    except Exception as e:
        print(f"Error making request: {e}")
        return False

if __name__ == "__main__":
    test_registration()