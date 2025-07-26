from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import httpx
from httpx import HTTPStatusError
import json
import os
import re
import base64
from typing import List, Dict, Any, Optional
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="LiteLLM Chat App")

# Templates setup
templates = Jinja2Templates(directory="templates")

# Serve static files (for TailwindCSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory storage for chat sessions
chat_sessions: Dict[str, List[Dict[str, Any]]] = {}

# LiteLLM API configuration
LITELLM_API_BASE = os.getenv("LITELLM_API_BASE", "https://litellm.shared-services.adb.adi.tech")
API_KEY = os.getenv("LITELLM_API_KEY")
VERSION = os.getenv("APP_VERSION", "1.0.0")

# Debug: Print version on startup
print(f"🚀 LiteLLM Chat App starting...")
print(f"📦 Version: {VERSION}")
print(f"🔗 API Base: {LITELLM_API_BASE}")

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    """Main chat interface page"""
    return templates.TemplateResponse("chat.html", {"request": request, "version": VERSION})

@app.get("/api/version")
async def get_version():
    """Get application version"""
    return {"version": VERSION}

@app.get("/api/models")
async def get_models():
    """Fetch available models from LiteLLM API"""
    try:
        headers = {}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{LITELLM_API_BASE}/models", headers=headers)
            models_data = response.json()
            return models_data
    except Exception as e:
        return {"error": f"Failed to fetch models: {str(e)}"}

@app.post("/api/chat")
async def chat_completion(
    message: str = Form(...),
    model: str = Form(...),
    session_id: str = Form(...),
    file_content: Optional[str] = Form(None),
    file_name: Optional[str] = Form(None)
):
    """Handle chat completion requests"""
    try:
        # Prepare the request payload
        user_content = message
        file_info = ""
        max_file_chars = 4000
        
        if file_content and file_name:
            try:
                file_data = base64.b64decode(file_content)
                # Try to decode as utf-8, fallback to show as bytes
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

🚨 **MANDATORY FORMATTING RULES - YOU MUST FOLLOW EVERY SINGLE ONE:**

🎯 **RESPONSE STRUCTURE (ALWAYS FOLLOW THIS EXACT ORDER):**
1. **START** with a relevant emoji + bold title: "🎯 **Your Title Here**"
2. **ALWAYS** use ### for main sections: "### 🔍 **Section Name**"
3. **ALWAYS** use ** for subsections: "**Subsection Name:**"
4. **ALWAYS** use bullet points (•) for lists: "• Item 1"
5. **ALWAYS** use numbered lists (1., 2., 3.) for steps: "1. Step one"
6. **ALWAYS** format code with proper blocks: "```language\ncode\n```"
7. **ALWAYS** use bold for emphasis: "**Important term**"
8. **ALWAYS** end with "### 🚀 **Next Steps**" section
9. **ALWAYS** include a final call-to-action with emoji

📋 **REQUIRED ELEMENTS IN EVERY RESPONSE:**
- 🎯 **Opening emoji + bold title**
- ### **Main sections with emojis**
- **Bold subsections**
- • Bullet point lists
- 1. Numbered step lists
- ```code blocks with syntax```
- **Bold emphasis on key terms**
- ### 🚀 **Next Steps** section
- 💡 **Final call-to-action**

🎨 **MANDATORY EMOJIS TO USE:**
- 🎯 (for titles)
- 🔍 (for analysis)
- 📊 (for data)
- 💡 (for insights)
- 🚀 (for next steps)
- ⚡ (for tips)
- 🔥 (for important info)
- ✅ (for success)
- ❌ (for errors)
- 💪 (for recommendations)

📝 **EXAMPLE FORMAT:**
🎯 **Your Response Title**

### 🔍 **Main Section**
**Subsection:**
• Bullet point 1
• Bullet point 2

1. Numbered step 1
2. Numbered step 2

```language
code example
```

### 🚀 **Next Steps**
💡 **Call to action here**

**YOU MUST FOLLOW THIS EXACT FORMAT FOR EVERY RESPONSE!**"""
                },
                {"role": "user", "content": user_content}
            ],
            "stream": False
        }
        
        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        
        print(f"🔍 Debug: Sending request to {LITELLM_API_BASE}/chat/completions")
        print(f"🔍 Debug: Model: {model}")
        print(f"🔍 Debug: Headers: {headers}")
        print(f"🔍 Debug: Payload message length: {len(user_content)}")
        
        # Send request to LiteLLM API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LITELLM_API_BASE}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            print(f"🔍 Debug: Response status: {response.status_code}")
            print(f"🔍 Debug: Response headers: {dict(response.headers)}")
            
            result = response.json()
            print(f"🔍 Debug: Response body: {result}")
            
            # Check for errors in the response body
            if "error" in result:
                error_msg = result["error"].get("message", "Unknown error")
                if "NotFoundError" in error_msg and "Model Group=" in error_msg:
                    model_match = re.search(r'Model Group=([^\n]+)', error_msg)
                    if model_match:
                        model_name = model_match.group(1)
                        return {"error": f"Model '{model_name}' not found. Please select a different model from the dropdown.", "file_name": file_name}
                    else:
                        return {"error": f"Model '{model}' not found. Please select a different model from the dropdown.", "file_name": file_name}
                else:
                    return {"error": f"API Error: {error_msg}", "file_name": file_name}
            
            # Check if response has the expected structure
            if "choices" not in result or not result["choices"]:
                return {"error": "Invalid response format from API", "file_name": file_name}
            
            assistant_message = result.get("choices", [{}])[0].get("message", {}).get("content", "No response received")
            
            if not assistant_message or assistant_message == "No response received":
                return {"error": "No response content received from API", "file_name": file_name}
            
            # Store in session (if session_id provided)
            if session_id:
                if session_id not in chat_sessions:
                    chat_sessions[session_id] = []
                chat_sessions[session_id].extend([
                    {"role": "user", "content": user_content, "file_name": file_name},
                    {"role": "assistant", "content": assistant_message}
                ])
            
            return {
                "role": "assistant",
                "content": assistant_message,
                "session_id": session_id,
                "file_name": file_name
            }
            
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
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    return chat_sessions.get(session_id, [])

@app.post("/api/new-session")
async def create_new_session():
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    chat_sessions[session_id] = []
    return {"session_id": session_id}

@app.post("/api/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and return file info"""
    try:
        # Read file content
        content = await file.read()
        
        # Encode file content as base64
        file_content_b64 = base64.b64encode(content).decode('utf-8')
        
        # Get file info
        file_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "content_b64": file_content_b64
        }
        
        return {
            "success": True,
            "file_info": file_info,
            "message": f"File '{file.filename}' uploaded successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to upload file: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 