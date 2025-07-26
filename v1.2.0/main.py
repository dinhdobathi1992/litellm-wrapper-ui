import os
import json
import base64
import uuid
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from auth import SECRET_KEY, get_current_user, require_auth, login_google, auth_callback, logout

load_dotenv()

app = FastAPI(title="LiteLLM Chat App")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Templates
templates = Jinja2Templates(directory="templates")

# Configuration
LITELLM_API_BASE = os.getenv("LITELLM_API_BASE", "https://litellm.shared-services.adb.adi.tech")
API_KEY = os.getenv("LITELLM_API_KEY")
VERSION = os.getenv("APP_VERSION", "1.0.0")

print("🚀 LiteLLM Chat App starting...")
print(f"📦 Version: {VERSION}")
print(f"🔗 API Base: {LITELLM_API_BASE}")

# In-memory storage for chat sessions (replace with database in production)
chat_sessions = {}

# Simple response cache for faster repeated queries
response_cache = {}

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Main chat page - requires authentication"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "version": VERSION,
        "user": user
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/", status_code=302)
    
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {
        "request": request, 
        "version": VERSION,
        "error": error
    })

@app.get("/auth/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    return await login_google(request)

@app.get("/auth/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    return await auth_callback(request)

@app.get("/logout")
async def logout_user(request: Request):
    """Logout user"""
    return await logout(request)

@app.get("/api/models")
async def get_models(request: Request):
    """Get available models - requires authentication"""
    user = require_auth(request)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LITELLM_API_BASE}/models", headers=headers, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error fetching models: {e}")
        return {"error": "Failed to fetch models", "data": []}

@app.post("/api/chat")
async def chat_completion(
    request: Request,
    message: str = Form(...),
    model: str = Form(...),
    session_id: str = Form(...),
    file_content: Optional[str] = Form(None),
    file_name: Optional[str] = Form(None)
):
    """Chat completion endpoint - requires authentication"""
    user = require_auth(request)
    
    # Initialize session if it doesn't exist
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # Add user message to session
    user_message = {
        "role": "user",
        "content": message,
        "file_name": file_name if file_content else None
    }
    chat_sessions[session_id].append(user_message)
    
    # Prepare the message for LiteLLM
    user_content = message
    file_info = ""
    max_file_chars = 4000
    
    # Create cache key for this request
    cache_key = f"{model}:{user_content}:{file_name or 'no_file'}"
    
    # Check cache first for faster responses
    if cache_key in response_cache:
        cached_response = response_cache[cache_key]
        assistant_msg = {
            "role": "assistant",
            "content": cached_response,
            "file_name": None
        }
        chat_sessions[session_id].append(assistant_msg)
        return {"content": cached_response, "file_name": file_name}
    
    if file_content and file_name:
        try:
            file_data = base64.b64decode(file_content)
            try:
                file_text = file_data.decode('utf-8')
            except Exception:
                file_text = None
            if file_text:
                if len(file_text) > max_file_chars:
                    file_text = file_text[:max_file_chars] + "\n... (truncated)"
                file_info = f"\n\n[Uploaded file: {file_name}]\n---\n{file_text}\n---"
            else:
                file_info = f"\n\n[Uploaded file: {file_name} (binary or non-text)]"
        except Exception as e:
            file_info = f"\n\n[Uploaded file: {file_name} (could not decode)]"
        user_content = f"{message}{file_info}"
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system", 
                "content": """You are a helpful AI assistant with expertise in analyzing data, files, and providing insights. 

🚀 **CRITICAL FORMATTING REQUIREMENTS - ALWAYS FOLLOW THESE:**

1. **ALWAYS start responses with relevant emojis** (🎯, 📊, 🔍, 💡, etc.)
2. **ALWAYS use clear section headers** with ### or ** for structure
3. **ALWAYS include bullet points** (• or -) for lists and key points
4. **ALWAYS use numbered lists** (1., 2., 3.) for steps or sequences
5. **ALWAYS format code blocks** with proper syntax highlighting
6. **ALWAYS use bold text** (**text**) for emphasis on important terms
7. **ALWAYS include actionable recommendations** when applicable
8. **ALWAYS use tables or structured formats** for data presentation
9. **ALWAYS end with a call-to-action** or next steps
10. **NEVER return plain text** - always use rich formatting

📋 **RESPONSE STRUCTURE:**
- Start with emoji + bold title: 🎯 **Your Title Here**
- Use ### for main sections: ### 🔍 **Section Name**
- Use bullet points for lists: • **Key Point**
- Use numbered lists for steps: 1. **Step One**
- Use code blocks: ```python\ncode here\n```
- End with: ### 🚀 **Next Steps** + 💡 call-to-action

Your responses should be informative, visually appealing, and easy to understand."""
            },
            {"role": "user", "content": user_content}
        ],
        "stream": False,
        "max_tokens": 4096,
        "temperature": 0.5,
        "top_p": 0.9
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    print(f"🔍 Debug: Sending request to {LITELLM_API_BASE}/chat/completions")
    print(f"🔍 Debug: Model: {model}")
    print(f"🔍 Debug: Headers: {headers}")
    print(f"🔍 Debug: Payload message length: {len(user_content)}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LITELLM_API_BASE}/chat/completions",
                json=payload,
                headers=headers,
                timeout=15.0
            )
            print(f"🔍 Debug: Response status: {response.status_code}")
            print(f"🔍 Debug: Response headers: {dict(response.headers)}")
            result = response.json()
            print(f"🔍 Debug: Response body: {result}")
            
            if "error" in result:
                error_msg = result["error"]
                if "NotFoundError" in error_msg:
                    # Extract model name from error message
                    import re
                    model_match = re.search(r"'([^']+)'", error_msg)
                    if model_match:
                        model_name = model_match.group(1)
                        return {"error": f"Model '{model_name}' not found. Please select a different model from the dropdown.", "file_name": file_name}
                    else:
                        return {"error": "Model not found. Please select a different model from the dropdown.", "file_name": file_name}
                else:
                    return {"error": error_msg, "file_name": file_name}
            
            if "choices" not in result or not result["choices"]:
                return {"error": "Invalid response format from API", "file_name": file_name}
            
            assistant_message = result.get("choices", [{}])[0].get("message", {}).get("content", "No response received")
            if not assistant_message or assistant_message == "No response received":
                return {"error": "No response content received from API", "file_name": file_name}
            
            # Add assistant message to session
            assistant_msg = {
                "role": "assistant",
                "content": assistant_message,
                "file_name": None
            }
            chat_sessions[session_id].append(assistant_msg)
            
            # Cache the response for future use
            response_cache[cache_key] = assistant_message
            
            # Limit cache size to prevent memory issues
            if len(response_cache) > 100:
                # Remove oldest entries
                oldest_keys = list(response_cache.keys())[:20]
                for key in oldest_keys:
                    del response_cache[key]
            
            return {"content": assistant_message, "file_name": file_name}
            
    except httpx.HTTPStatusError as e:
        print(f"🔍 Debug: HTTP Status Error: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 404:
            return {"error": f"Model '{model}' not found. Please select a different model from the dropdown.", "file_name": file_name}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed. Please check your API key.", "file_name": file_name}
        elif e.response.status_code == 403:
            return {"error": "Access forbidden. Please check your API key and permissions.", "file_name": file_name}
        else:
            return {"error": f"API error ({e.response.status_code}): {e.response.text}", "file_name": file_name}
    except httpx.TimeoutException:
        return {"error": "Request timed out. Please try again.", "file_name": file_name}
    except httpx.ConnectError:
        return {"error": "Could not connect to the API server. Please check your internet connection.", "file_name": file_name}
    except json.JSONDecodeError as e:
        print(f"🔍 Debug: JSON Decode Error: {e}")
        return {"error": "Invalid JSON response from API", "file_name": file_name}
    except Exception as e:
        print(f"🔍 Debug: Unexpected Error: {type(e).__name__}: {str(e)}")
        return {"error": f"Unexpected error: {type(e).__name__}: {str(e)}", "file_name": file_name}

@app.get("/api/chat-history/{session_id}")
async def get_chat_history(session_id: str, request: Request):
    """Get chat history for a session - requires authentication"""
    user = require_auth(request)
    
    if session_id in chat_sessions:
        return {"messages": chat_sessions[session_id]}
    else:
        return {"messages": []}

@app.post("/api/new-session")
async def create_new_session(request: Request):
    """Create a new chat session - requires authentication"""
    user = require_auth(request)
    
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = []
    return {"session_id": session_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 