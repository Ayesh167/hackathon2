import google.generativeai as genai
import os

# Configure the API key
gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro-latest')
    
    # Test a simple prompt
    test_prompt = "Hello, how are you?"
    try:
        print("Testing Gemini API with simple prompt...")
        response = model.generate_content(test_prompt)
        print(f"Response: {response.text}")
        print("Gemini API is working correctly!")
    except Exception as e:
        print(f"Error with Gemini API: {e}")
else:
    print("No GEMINI_API_KEY found in environment variables")