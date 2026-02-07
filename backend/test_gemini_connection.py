import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the API key from environment
gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not gemini_api_key:
    print("ERROR: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not found!")
    print("Available environment variables:")
    for key, value in os.environ.items():
        if 'API' in key.upper() or 'KEY' in key.upper():
            print(f"  {key}: {value[:10]}..." if len(value) > 10 else f"  {key}: {value}")
    exit(1)

print("API key found, attempting to initialize client...")

try:
    # Configure the Gemini API
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    print("Google Gemini client initialized successfully!")

    # Test with a simple API call
    print("Testing API connection...")
    response = model.generate_content("Hello, this is a test.")
    
    print("API connection successful!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"ERROR: Failed to connect to Google Gemini API: {e}")