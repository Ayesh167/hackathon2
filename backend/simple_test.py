import requests
import json

print("Testing AI Assistant...")

# Register a test user
register_url = 'http://127.0.0.1:8000/auth/register'
register_data = {
    'email': 'testuser4@example.com',
    'password': 'password123',
    'name': 'Test User 4'
}

print("Registering user...")
register_response = requests.post(register_url, json=register_data)
print(f'Register status: {register_response.status_code}')
if register_response.status_code != 200:
    print(f'Register response: {register_response.text}')
    exit(1)

# Login
login_url = 'http://127.0.0.1:8000/auth/login'
login_data = {
    'email': 'testuser4@example.com',
    'password': 'password123'
}

print("Logging in...")
login_response = requests.post(login_url, json=login_data)
print(f'Login status: {login_response.status_code}')
if login_response.status_code != 200:
    print(f'Login response: {login_response.text}')
    exit(1)

token = login_response.json()['access_token']
print(f'Token received')

# Test a simple chat message
chat_url = 'http://127.0.0.1:8000/api/chat'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

chat_data = {
    'message': 'Hello',
    'conversation_id': None
}

print("Testing chat endpoint...")
chat_response = requests.post(chat_url, headers=headers, json=chat_data)
print(f'Chat status: {chat_response.status_code}')
print(f'Chat response: {chat_response.text}')

# Test another message that should trigger task creation
chat_data2 = {
    'message': 'Create a task to buy groceries',
    'conversation_id': None
}

print("\nTesting task creation...")
chat_response2 = requests.post(chat_url, headers=headers, json=chat_data2)
print(f'Chat status: {chat_response2.status_code}')
print(f'Chat response: {chat_response2.text}')

# Test showing tasks
chat_data3 = {
    'message': 'Show me my tasks',
    'conversation_id': None
}

print("\nTesting task listing...")
chat_response3 = requests.post(chat_url, headers=headers, json=chat_data3)
print(f'Chat status: {chat_response3.status_code}')
print(f'Chat response: {chat_response3.text}')