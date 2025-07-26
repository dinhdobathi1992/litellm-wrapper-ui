# LiteLLM Chat App

A lightweight web chat application built with FastAPI and HTMX that connects to the LiteLLM API.

## Features

- 🤖 Chat interface similar to ChatGPT/Gemini
- 📋 Model selection dropdown (fetched from LiteLLM API)
- 💬 Real-time chat with AI models
- 🌙 Dark mode support with theme toggle
- 🎨 Modern UI with TailwindCSS
- 📱 Responsive design
- 🔄 Session-based chat history (in-memory)
- ⚡ HTMX for dynamic interactions
- 🚀 Ready for Vercel deployment

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create a `.env` file in the project root and add your LiteLLM configuration:
   ```bash
   cp env.example .env
   # Edit .env and add your actual API key and server URL
   ```

3. **Run the application:**
   
   **Option 1: Using startup script (recommended)**
   ```bash
   # For bash/zsh
   ./start.sh
   
   # For fish shell
   ./start.fish
   ```
   
   **Option 2: Manual activation**
   ```bash
   source venv/bin/activate  # or source venv/bin/activate.fish for fish
   python main.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8000`

## API Endpoints

- `GET /` - Main chat interface
- `GET /api/models` - Fetch available models from LiteLLM
- `POST /api/chat` - Send chat message and get AI response
- `GET /api/chat-history/{session_id}` - Get chat history for a session
- `POST /api/new-session` - Create a new chat session

## Usage

1. **Select a Model:** Choose from the dropdown of available models
2. **Start Chatting:** Type your message and press Send
3. **New Chat:** Click "New Chat" to start a fresh conversation
4. **View History:** Chat history is maintained during your session

## Technical Details

- **Backend:** FastAPI with async HTTP client (httpx)
- **Frontend:** HTML + JavaScript with HTMX
- **Styling:** TailwindCSS (CDN) with dark mode support
- **Storage:** In-memory session storage (no database required)
- **API:** Configurable LiteLLM API endpoint
- **Deployment:** Ready for Vercel deployment

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `jinja2` - Template engine
- `httpx` - Async HTTP client
- `python-multipart` - Form data handling

## Notes

- Chat history is stored in memory and will be lost when the server restarts
- No authentication or user management included
- API key is required and should be set in the `.env` file
- LiteLLM server URL is configurable via environment variables
- Dark mode preference is saved in browser localStorage

## Author

**ThiThi** - [GitHub](https://github.com/dinhdobathi1992) | [Portfolio](https://dinhdobathi.com)

Built with ❤️ using FastAPI, HTMX, and TailwindCSS

## Deployment

### Vercel Deployment

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel:**
   ```bash
   vercel
   ```

3. **Set Environment Variables:**
   In your Vercel dashboard, add the following environment variables:
   - `LITELLM_API_KEY`: Your LiteLLM API key
   - `LITELLM_API_BASE`: Your LiteLLM server URL (optional, defaults to the shared service)

4. **Redeploy:**
   ```bash
   vercel --prod
   ```

### Environment Variables

- `LITELLM_API_KEY` (required): Your LiteLLM API key
- `LITELLM_API_BASE` (optional): LiteLLM server URL (defaults to `https://litellm.shared-services.adb.adi.tech`)
- `APP_VERSION` (optional): Application version (defaults to `1.0.0`) 