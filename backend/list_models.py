import google.generativeai as genai
import os

# Configure the API key
gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    
    # List available models
    print("Listing available models...")
    try:
        models = genai.list_models()
        for model in models:
            print(f"Model: {model.name}")
            print(f"  Supported operations: {[m for m in model.supported_generation_methods]}")
            print()
    except Exception as e:
        print(f"Error listing models: {e}")
else:
    print("No GEMINI_API_KEY found in environment variables")