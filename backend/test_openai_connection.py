import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("ERROR: OPENAI_API_KEY environment variable not found!")
    print("Available environment variables:")
    for key, value in os.environ.items():
        if 'API' in key.upper() or 'KEY' in key.upper():
            print(f"  {key}: {value[:10]}..." if len(value) > 10 else f"  {key}: {value}")
    exit(1)

print("API key found, attempting to initialize client...")

try:
    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key)
    print("OpenAI client initialized successfully!")

    # Test with a simple API call
    print("Testing API connection...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, this is a test."}],
        max_tokens=10
    )
    
    print("API connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"ERROR: Failed to connect to OpenAI API: {e}")