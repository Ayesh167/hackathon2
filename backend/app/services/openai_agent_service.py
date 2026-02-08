"""
Google Gemini Agent Service for Natural Language Processing

This service integrates Google's Gemini API to process natural language
requests and route them to appropriate MCP tools for task management.
"""

import os
import re
from typing import Dict, Any, List
from sqlmodel import Session
import google.generativeai as genai
import logging
from ..mcp_tools.task_tools import (
    create_task_tool,
    get_tasks_tool,
    get_task_tool,
    update_task_tool,
    delete_task_tool,
    toggle_task_completion_tool,
    get_user_info_tool
)

# Initialize Google Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
model = None
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        # Use a text generation model - using the correct model name
        model = genai.GenerativeModel('gemini-pro-latest')
        print("Google Gemini client initialized successfully")
    except Exception as e:
        print(f"Error initializing Google Gemini client: {e}")
        print("Running in offline mode with keyword matching fallback")
else:
    # If no API key is provided, set model to None to handle gracefully
    print("GEMINI_API_KEY or GOOGLE_API_KEY not found in environment variables")
    print("Running in offline mode with keyword matching fallback")


def parse_user_request_for_task_action(user_message: str) -> Dict[str, Any]:
    """
    Parse the user's message to determine what task action they want to perform.
    Uses Google Gemini API for natural language understanding.
    """
    try:
        # Handle null or empty input
        if not user_message:
            return {"action": "general_conversation", "message": user_message}

        # If Gemini model is available, use it for natural language understanding
        if model:
            try:
                # Create a prompt to understand the user's intent
                prompt = f"""
                Analyze the following user message and determine the intent. 
                Respond in JSON format with the following structure:
                
                {{
                  "action": "create|get_all|get_completed|get_pending|update|delete|toggle|general_conversation|help|greeting",
                  "title": "task title if creating/updating",
                  "task_id": "task ID if relevant",
                  "status_filter": "all|completed|pending if getting tasks",
                  "completed": "true|false if toggling",
                  "description": "task description if creating/updating"
                }}
                
                For general conversation, greeting, or help requests, use "general_conversation", "greeting", or "help" as the action.
                
                User message: "{user_message}"
                """
                
                response = model.generate_content(prompt)
                response_text = response.text.strip()
                
                # Clean up the response to extract JSON
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                import json
                parsed_intent = json.loads(response_text)
                
                return parsed_intent
            except Exception as e:
                print(f"Error using Gemini for intent parsing: {e}")
                # Fall back to keyword matching if Gemini fails
        
        # Fallback to keyword matching if Gemini is not available or fails
        user_message_lower = user_message.lower().strip()

        # Define all variables at the beginning
        create_keywords = ['create', 'add', 'make', 'new', 'build', 'setup', 'start', 'begin']
        task_related_words = ['task', 'todo', 'to-do', 'item', 'thing', 'activity', 'job', 'chore', 'work', 'assignment']
        list_keywords = ['show', 'list', 'display', 'view', 'see', 'get', 'fetch', 'retrieve', 'find', 'tell me', 'about']
        all_related_words = ['all', 'my', 'every', 'each', 'total', 'everything']
        pending_related_words = ['pending', 'incomplete', 'not done', 'open', 'active', 'remaining', 'left', 'unfinished']
        completed_related_words = ['completed', 'done', 'finished', 'closed', 'marked done', 'checked', 'completed tasks']
        
        # Enhanced keyword matching for fallback - using one continuous if/elif chain
        # Task creation - more comprehensive matching
        if any(keyword in user_message_lower for keyword in create_keywords) and any(word in user_message_lower for word in task_related_words):
            # Extract title after common phrases
            title = user_message_lower
            for phrase in ['create task', 'create a task', 'create the task', 'add task', 'add a task', 'add the task', 
                          'make task', 'make a task', 'make the task', 'new task', 'create to', 'add to', 'make to',
                          'create a new', 'add a new', 'make a new']:
                if phrase in title:
                    title = title.split(phrase, 1)[1].strip()
                    break
            
            # Further clean up the title by removing common prefixes
            for prefix in ['to ', 'for ', 'that ', 'should ', 'need to ', 'want to ', 'going to ', 'will ', 'can you ']:
                if title.startswith(prefix):
                    title = title[len(prefix):].strip()
                    
            return {"action": "create", "title": title or "New Task"}

        # Task listing - more comprehensive matching
        # Check for "pending tasks" - before general tasks to avoid conflicts
        elif (any(keyword in user_message_lower for keyword in list_keywords) and 
            any(word in user_message_lower for word in pending_related_words) and 
            any(task_word in user_message_lower for task_word in task_related_words)):
            return {"action": "get_pending", "status_filter": "pending"}
        
        # Check for "completed tasks" - before general tasks to avoid conflicts
        elif (any(keyword in user_message_lower for keyword in list_keywords) and 
              any(word in user_message_lower for word in completed_related_words) and 
              any(task_word in user_message_lower for task_word in task_related_words)):
            return {"action": "get_completed", "status_filter": "completed"}
        
        # Check for "all tasks" or "my tasks"
        elif (any(keyword in user_message_lower for keyword in list_keywords) and 
            any(word in user_message_lower for word in all_related_words) and 
            any(task_word in user_message_lower for task_word in task_related_words)):
            return {"action": "get_all", "status_filter": "all"}
        
        # Special case for "what tasks do I have?" - before the general condition to avoid conflicts
        elif 'what' in user_message_lower and 'tasks' in user_message_lower and ('have' in user_message_lower or 'got' in user_message_lower):
            return {"action": "get_all", "status_filter": "all"}

        # General "tasks" query (without specific status)
        elif any(keyword in user_message_lower for keyword in list_keywords) and any(task_word in user_message_lower for task_word in task_related_words):
            return {"action": "get_all", "status_filter": "all"}

        # Greeting detection - enhanced (whole word matching to avoid substring issues)
        elif any(greeting in user_message_lower for greeting in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            return {"action": "greeting", "message": user_message}

        # More specific patterns first to avoid conflicts
        
        # Specific "how are you" question should be general conversation, not greeting
        elif 'how are you' in user_message_lower:
            return {"action": "general_conversation", "message": user_message}
        
        # Thank you messages should be general conversation - before help detection to avoid conflicts
        elif any(thanks in user_message_lower for thanks in ['thank you', 'thanks', 'thank you so much', 'appreciate', 'grateful']):
            return {"action": "general_conversation", "message": user_message}
        
        # Question about capabilities or help - before assistant questions to avoid conflicts
        elif any(phrase in user_message_lower for phrase in ['what can you', 'what are you able', 'how can you', 'help', 'assist', 'can you', 'how do i use', 'what do you do']):
            return {"action": "help", "message": user_message}

        # Questions about the assistant
        elif ('how do you' in user_message_lower or 
              'how are things' in user_message_lower or 'how is it going' in user_message_lower or 
              'what are you' in user_message_lower):
            return {"action": "greeting", "message": user_message}

        # Default to general conversation for unrecognized requests
        else:
            return {"action": "general_conversation", "message": user_message}

    except Exception as e:
        # If any error occurs, default to general conversation
        print(f"Error in parse_user_request_for_task_action: {e}")
        return {"action": "general_conversation", "message": user_message}


def process_natural_language_request(
    session: Session,
    user_id: str,
    user_message: str,
    conversation_history: List[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Process a natural language request using local logic and MCP tools.

    Args:
        session: Database session
        user_id: ID of the user making the request
        user_message: Natural language request from the user
        conversation_history: Previous conversation history (for context)

    Returns:
        Dictionary with the agent's response and any action results
    """
    # Parse the user's request to determine the action
    parsed_request = parse_user_request_for_task_action(user_message)
    action = parsed_request.get("action")

    action_results = []

    # Perform the appropriate action based on the parsed request
    if action == "create":
        title = parsed_request.get("title", "Untitled Task")
        result = create_task_tool(session=session, user_id=user_id, title=title)
        action_results.append(result)

        if result.get("success"):
            ai_response = f"I've created the task '{title}' for you."
        else:
            ai_response = f"I couldn't create the task: {result.get('error', 'Unknown error')}"

    elif action == "get_all":
        status_filter = parsed_request.get("status_filter", "all")
        result = get_tasks_tool(session=session, user_id=user_id, status_filter=status_filter)
        action_results.append(result)

        if result.get("success"):
            tasks = result.get("tasks", [])
            if tasks:
                task_list = "\n".join([f"- {task.get('title', 'No title')} (ID: {task.get('id', 'Unknown')})" for task in tasks])
                ai_response = f"Here are your tasks:\n{task_list}"
            else:
                ai_response = "You don't have any tasks."
        else:
            ai_response = f"I couldn't retrieve your tasks: {result.get('error', 'Unknown error')}"

    elif action == "get_completed":
        result = get_tasks_tool(session=session, user_id=user_id, status_filter="completed")
        action_results.append(result)

        if result.get("success"):
            tasks = result.get("tasks", [])
            if tasks:
                task_list = "\n".join([f"- {task.get('title', 'No title')} (ID: {task.get('id', 'Unknown')})" for task in tasks])
                ai_response = f"Here are your completed tasks:\n{task_list}"
            else:
                ai_response = "You don't have any completed tasks."
        else:
            ai_response = f"I couldn't retrieve your completed tasks: {result.get('error', 'Unknown error')}"

    elif action == "get_pending":
        result = get_tasks_tool(session=session, user_id=user_id, status_filter="pending")
        action_results.append(result)

        if result.get("success"):
            tasks = result.get("tasks", [])
            if tasks:
                task_list = "\n".join([f"- {task.get('title', 'No title')} (ID: {task.get('id', 'Unknown')})" for task in tasks])
                ai_response = f"Here are your pending tasks:\n{task_list}"
            else:
                ai_response = "You don't have any pending tasks."
        else:
            ai_response = f"I couldn't retrieve your pending tasks: {result.get('error', 'Unknown error')}"

    elif action == "update":
        task_id = parsed_request.get("task_id")
        title = parsed_request.get("title")
        description = parsed_request.get("description")

        if not task_id:
            ai_response = "I need the task ID to update. Please specify which task you want to update."
        else:
            result = update_task_tool(session=session, user_id=user_id, task_id=task_id, title=title, description=description)
            action_results.append(result)

            if result.get("success"):
                ai_response = f"I've updated task #{task_id}."
            else:
                ai_response = f"I couldn't update the task: {result.get('error', 'Unknown error')}"

    elif action == "delete":
        task_id = parsed_request.get("task_id")

        if not task_id:
            ai_response = "I need the task ID to delete. Please specify which task you want to delete."
        else:
            result = delete_task_tool(session=session, user_id=user_id, task_id=task_id)
            action_results.append(result)

            if result.get("success"):
                ai_response = f"I've deleted task #{task_id}."
            else:
                ai_response = f"I couldn't delete the task: {result.get('error', 'Unknown error')}"

    elif action == "toggle":
        task_id = parsed_request.get("task_id")

        if not task_id:
            ai_response = "I need the task ID to toggle. Please specify which task you want to toggle."
        else:
            result = toggle_task_completion_tool(session=session, user_id=user_id, task_id=task_id)
            action_results.append(result)

            if result.get("success"):
                new_status = "completed" if result.get("completed") else "pending"
                ai_response = f"I've marked task #{task_id} as {new_status}."
            else:
                ai_response = f"I couldn't toggle the task: {result.get('error', 'Unknown error')}"

    elif action == "greeting":
        # Handle greeting requests
        ai_response = "Hello! I'm your AI assistant. I can help you manage your tasks. You can ask me to create, list, update, or delete tasks."
        
    elif action == "help":
        # Handle help requests
        ai_response = "I can help you manage your tasks! You can ask me to: create tasks, list all tasks, list pending tasks, list completed tasks, update tasks, delete tasks, or mark tasks as complete/incomplete. For example, you can say 'Create a task to buy groceries' or 'Show me my tasks'."
    
    elif action == "general_conversation":
        # For general conversation requests, use Gemini to generate a more natural response if available
        if model:
            try:
                # Create a prompt for the Gemini model to generate a natural response
                prompt = f"""
                You are a helpful AI assistant for a task management application. The user said: "{user_message}"
                
                Provide a friendly, helpful response that acknowledges their message and reminds them about task management capabilities if relevant.
                Keep the response concise and helpful.
                """
                
                response = model.generate_content(prompt)
                ai_response = response.text.strip()
            except Exception as e:
                print(f"Error generating response with Gemini: {e}")
                # Fallback to default response
                ai_response = "I'm here to help you manage your tasks! You can ask me to create, list, update, or delete tasks."
        else:
            # For other general conversation, provide a helpful default response
            ai_response = "I'm here to help you manage your tasks! You can ask me to create, list, update, or delete tasks."
    else:
        # For unrecognized requests, provide a helpful default response
        ai_response = "I'm here to help you manage your tasks! You can ask me to create, list, update, or delete tasks. For example, you can say 'Create a task to buy groceries' or 'Show me my tasks'."

    return {
        "response": ai_response,
        "action_results": action_results
    }