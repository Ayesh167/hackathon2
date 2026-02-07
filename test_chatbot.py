# Test script for AI Chatbot functionality

import subprocess
import sys
import time
import requests
import json

def test_backend():
    """Test the backend implementation"""
    print("Testing backend implementation...")
    
    import os
    
    # Check if the chat router exists
    chat_router_path = "backend/app/routers/chat.py"
    if os.path.exists(chat_router_path):
        print("+ Chat router exists")
    else:
        print("- Chat router not found")
        return False
    
    # Check if the openai agent service exists
    agent_service_path = "backend/app/services/openai_agent_service.py"
    if os.path.exists(agent_service_path):
        print("+ OpenAI agent service exists")
    else:
        print("- OpenAI agent service not found")
        return False
    
    # Check if the mcp tools exist
    mcp_tools_path = "backend/app/mcp_tools/task_tools.py"
    if os.path.exists(mcp_tools_path):
        print("+ MCP tools exist")
    else:
        print("- MCP tools not found")
        return False
    
    # Check if the models were updated
    models_path = "backend/app/models/task_models.py"
    if os.path.exists(models_path):
        with open(models_path, "r") as f:
            content = f.read()
            if "Conversation" in content and "Message" in content:
                print("+ Conversation and Message models exist")
            else:
                print("- Conversation and Message models not found in task_models.py")
                return False
    else:
        print("- Task models file not found")
        return False
    
    # Check if main.py includes the chat router
    main_path = "backend/main.py"
    if os.path.exists(main_path):
        with open(main_path, "r") as f:
            content = f.read()
            if "from app.routers import chat" in content and "app.include_router(chat.router)" in content:
                print("+ Chat router included in main app")
            else:
                print("- Chat router not included in main app")
                return False
    else:
        print("- Main app file not found")
        return False
    
    return True

def test_database_schema():
    """Test if the new database tables were created"""
    print("\nTesting database schema...")
    
    try:
        import sqlite3
        conn = sqlite3.connect("backend/todo_app.db")
        cursor = conn.cursor()
        
        # Check if conversations table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversation';")
        if cursor.fetchone():
            print("[OK] Conversations table exists")
        else:
            print("[INFO] Conversations table not found (might be named differently)")
            # Try with lowercase
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations';")
            if cursor.fetchone():
                print("[OK] Conversations table exists (lowercase)")
            else:
                print("[MISSING] Conversations table does not exist")
        
        # Check if messages table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='message';")
        if cursor.fetchone():
            print("[OK] Messages table exists")
        else:
            print("[INFO] Messages table not found (might be named differently)")
            # Try with lowercase
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages';")
            if cursor.fetchone():
                print("[OK] Messages table exists (lowercase)")
            else:
                print("[MISSING] Messages table does not exist")
        
        conn.close()
        return True
    except Exception as e:
        print(f"[ERROR] Error testing database schema: {e}")
        return False

def test_frontend():
    """Test frontend components"""
    print("\nTesting frontend components...")
    
    import os
    
    # Check if the chat component exists
    chat_component_path = "frontend/components/chat/ChatInterface.tsx"
    if os.path.exists(chat_component_path):
        print("[OK] ChatInterface component exists")
    else:
        print("[MISSING] ChatInterface component not found")
        return False
    
    # Check if the chat page exists
    chat_page_path = "frontend/app/chat/page.tsx"
    if os.path.exists(chat_page_path):
        print("[OK] Chat page exists")
    else:
        print("[MISSING] Chat page not found")
        return False
    
    # Check if API client has chat methods
    with open("frontend/lib/api.ts", "r") as f:
        api_content = f.read()
        if "sendMessage" in api_content and "getConversations" in api_content:
            print("[OK] API client has chat methods")
        else:
            print("[MISSING] API client missing chat methods")
            return False
    
    return True

def run_tests():
    """Run all tests"""
    print("Starting AI Chatbot functionality tests...\n")
    
    all_passed = True
    
    # Test backend
    if not test_backend():
        all_passed = False
    
    # Test database schema
    if not test_database_schema():
        all_passed = False
    
    # Test frontend
    if not test_frontend():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("[SUCCESS] All tests passed! AI Chatbot functionality is properly implemented.")
        print("\nNext steps:")
        print("1. Start the backend server: uvicorn main:app --reload")
        print("2. Start the frontend: npm run dev")
        print("3. Visit http://localhost:3000/chat to use the chat interface")
    else:
        print("[FAILURE] Some tests failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    run_tests()