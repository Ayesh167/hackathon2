import subprocess
import time
import requests
import json

def test_with_server():
    # Start the server
    print("Starting the server...")
    server_process = subprocess.Popen(['uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'], 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for the server to start
    time.sleep(5)
    
    try:
        # Test if server is running
        health_response = requests.get('http://127.0.0.1:8000/health')
        print(f"Server health check: {health_response.status_code}")
        
        # Register a test user
        register_url = 'http://127.0.0.1:8000/auth/register'
        register_data = {
            'email': 'testuser3@example.com',
            'password': 'password123',
            'name': 'Test User 3'
        }

        register_response = requests.post(register_url, json=register_data)
        print(f'Register status: {register_response.status_code}')

        # Login
        login_url = 'http://127.0.0.1:8000/auth/login'
        login_data = {
            'email': 'testuser3@example.com',
            'password': 'password123'
        }

        login_response = requests.post(login_url, json=login_data)
        print(f'Login status: {login_response.status_code}')
        
        if login_response.status_code == 200:
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

            chat_response = requests.post(chat_url, headers=headers, json=chat_data)
            print(f'Chat status: {chat_response.status_code}')
            print(f'Chat response: {chat_response.text}')
        else:
            print(f"Login failed: {login_response.text}")
            
    except Exception as e:
        print(f'Error during test: {e}')
    finally:
        # Terminate the server
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    test_with_server()