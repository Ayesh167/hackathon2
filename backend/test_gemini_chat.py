import requests
import json

# Test the chatbot functionality with authentication
def test_chatbot():
    # Test URL - adjust if needed
    url = "http://127.0.0.1:8000/api/chat"

    # Sample request data
    data = {
        "message": "Hello, can you help me create a test task?",
        "conversation_id": None  # This will create a new conversation
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print("Testing chatbot endpoint...")
        response = requests.post(url, headers=headers, json=data)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("Chatbot API is working correctly!")
            return True
        else:
            print("There might be an issue with the chatbot API")
            return False

    except Exception as e:
        print(f"Error testing chatbot: {e}")
        return False

if __name__ == "__main__":
    test_chatbot()