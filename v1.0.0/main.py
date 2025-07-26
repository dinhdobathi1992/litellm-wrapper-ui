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
        
        # If file content is provided, append it to the message
        if file_content and file_name:
            try:
                # Decode base64 content
                file_data = base64.b64decode(file_content).decode('utf-8', errors='ignore')
                user_content = f"{message}\n\nFile: {file_name}\nContent:\n{file_data}"
            except Exception as e:
                user_content = f"{message}\n\nFile: {file_name} (content could not be decoded)"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": user_content}
            ],
            "stream": False
        }
        
        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        
        # Send request to LiteLLM API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{LITELLM_API_BASE}/chat/completions",
                json=payload,
                headers=headers
            )
            
            result = response.json()
            
            # Check for errors in the response body
            if "error" in result:
                error_msg = result["error"].get("message", "Unknown error")
                if "NotFoundError" in error_msg and "Model Group=" in error_msg:
                    # Extract model name from error message
                    model_match = re.search(r'Model Group=([^\n]+)', error_msg)
                    if model_match:
                        model_name = model_match.group(1)
                        return {"error": f"Model '{model_name}' not found. Please select a different model from the dropdown."}
                    else:
                        return {"error": f"Model '{model}' not found. Please select a different model from the dropdown."}
                else:
                    return {"error": f"API Error: {error_msg}"}
            
            # Extract the assistant's response
        assistant_message = result.get("choices", [{}])[0].get("message", {}).get("content", "No response received")
        
        # Store in session (if session_id provided)
        if session_id:
            if session_id not in chat_sessions:
                chat_sessions[session_id] = []
            
            chat_sessions[session_id].extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": assistant_message}
            ])
        
        return {
            "role": "assistant",
            "content": assistant_message,
            "session_id": session_id
        }
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"error": f"Model '{model}' not found. Please select a different model from the dropdown."}
        elif e.response.status_code == 401:
            return {"error": "Authentication failed. Please check your API key."}
        else:
            return {"error": f"API error ({e.response.status_code}): {e.response.text}"}
    except Exception as e:
        return {"error": f"Failed to get response: {str(e)}"}

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