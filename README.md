# LiteLLM Chat Application

A modern, lightweight web chat application built with FastAPI and TailwindCSS that integrates with LiteLLM API for AI-powered conversations. Features Google OAuth2 authentication for secure user access.

## ✨ Features

- 🔐 **Google OAuth2 Authentication** - Secure login with Google accounts
- 🤖 **AI Chat Interface** - Powered by LiteLLM API with multiple model support
- 📁 **File Upload Support** - Upload and analyze files in conversations
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 💾 **Session Management** - Persistent chat sessions during browser session
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Professional ChatGPT-like interface
- 🔄 **Real-time Chat** - Instant message sending and receiving
- 📊 **Markdown Rendering** - Rich formatting for AI responses

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google OAuth2 credentials (Client ID and Client Secret)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd litellm-wrapper-ui
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   # LiteLLM API Configuration
   LITELLM_API_KEY=your_api_key_here
   LITELLM_API_BASE=https://litellm.shared-services.adb.adi.tech
   
   # Application Configuration
   APP_VERSION=1.2.0
   
   # Google OAuth2 Configuration
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   SECRET_KEY=your_secret_key_here_change_this_in_production
   ```

### Google OAuth2 Setup

1. **Create Google OAuth2 Credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google+ API
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:8000/auth/callback` (for development)
     - `https://yourdomain.com/auth/callback` (for production)

2. **Update Environment Variables**
   - Copy the Client ID and Client Secret to your `.env` file
   - Generate a secure SECRET_KEY (you can use `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### Running the Application

1. **Start the server**
   ```bash
   python main.py
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - You'll be redirected to the login page
   - Click "Sign in with Google" to authenticate
   - After successful authentication, you'll be redirected to the chat interface

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LITELLM_API_KEY` | Your LiteLLM API key | Yes | - |
| `LITELLM_API_BASE` | LiteLLM API base URL | No | `https://litellm.shared-services.adb.adi.tech` |
| `APP_VERSION` | Application version | No | `1.0.0` |
| `GOOGLE_CLIENT_ID` | Google OAuth2 Client ID | Yes | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 Client Secret | Yes | - |
| `SECRET_KEY` | Session encryption key | Yes | Auto-generated |

### Features Configuration

- **Default Model**: The application automatically selects GPT-4o as the default model when available
- **File Upload**: Supports text files up to 4000 characters (truncated if larger)
- **Session Storage**: Chat sessions are stored in memory (replace with database for production)

## 🏗️ Architecture

### Backend (FastAPI)
- **Authentication**: Google OAuth2 with session management
- **API Integration**: LiteLLM API for AI model access
- **File Handling**: Base64 encoding for file uploads
- **Session Management**: In-memory storage with UUID-based sessions

### Frontend (HTML/JavaScript)
- **UI Framework**: TailwindCSS for styling
- **Theme Support**: Dark/light mode toggle
- **Markdown Rendering**: Custom markdown parser for AI responses
- **File Upload**: Drag-and-drop and click-to-upload support

## 🔒 Security Features

- **OAuth2 Authentication**: Secure Google login
- **Session Management**: Encrypted session storage
- **State Parameter**: CSRF protection for OAuth flow
- **Input Validation**: Server-side validation for all inputs
- **Error Handling**: Secure error messages without information leakage

## 🚀 Deployment

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   ./deploy.sh
   ```

### Environment Variables for Production

Make sure to update your Google OAuth2 redirect URIs to include your production domain:
- `https://yourdomain.com/auth/callback`

## 📝 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Main chat interface | Yes |
| `/login` | GET | Login page | No |
| `/auth/google` | GET | Initiate Google OAuth | No |
| `/auth/callback` | GET | OAuth callback handler | No |
| `/logout` | GET | Logout user | Yes |
| `/api/models` | GET | Get available models | Yes |
| `/api/chat` | POST | Send chat message | Yes |
| `/api/chat-history/{session_id}` | GET | Get chat history | Yes |
| `/api/new-session` | POST | Create new session | Yes |

## 🛠️ Development

### Project Structure
```
litellm-wrapper-ui/
├── main.py              # FastAPI application
├── auth.py              # Authentication module
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── env.example          # Environment template
├── templates/           # HTML templates
│   ├── chat.html       # Main chat interface
│   └── login.html      # Login page
├── v1.1.0/             # Backup of previous version
└── README.md           # This file
```

### Running Tests
```bash
# Test the application
curl http://localhost:8000/login
curl http://localhost:8000/  # Should redirect to login
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**ThiThi**
- GitHub: [dinhdobathi1992](https://github.com/dinhdobathi1992/litellm-wrapper-ui)
- Portfolio: [dinhdobathi.com](https://dinhdobathi.com)

## 🔄 Version History

- **v1.2.0** - Added Google OAuth2 authentication
- **v1.1.0** - Enhanced UI, file upload, session management
- **v1.0.0** - Initial release with basic chat functionality

## 🆘 Support

If you encounter any issues:
1. Check the environment variables are correctly set
2. Verify Google OAuth2 credentials are valid
3. Ensure LiteLLM API is accessible
4. Check the server logs for detailed error messages

---

**Powered by LiteLLM • v1.2.0** 