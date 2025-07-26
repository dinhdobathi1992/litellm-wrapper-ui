# Zen's LiteLLM Chat - Developer Demo

A demo version of Zen's LiteLLM Chat Application with usage restrictions for non-admin users. Perfect for showcasing the application without incurring high API costs.

## 🎭 Demo Features

- **🔐 Google OAuth2 Authentication** - Secure login with Google accounts
- **👑 Admin Access** - Unlimited access for admin users (dinhdobathi@gmail.com)
- **🎪 Demo Mode** - Limited access for other users (1-2 requests, 100 tokens)
- **🤖 AI Chat Interface** - Powered by LiteLLM API with multiple model support
- **📁 File Upload Support** - Upload and analyze PDF, DOCX, Excel, images, and text files
- **🖼️ AI Image Generation** - Generate images using DALL-E and other image models
- **🌙 Dark Mode** - Toggle between light and dark themes
- **💾 Session Management** - Persistent chat sessions with chat history sidebar
- **📱 Responsive Design** - Works on desktop and mobile devices
- **📊 Usage Tracking** - Real-time usage monitoring for demo users

## 🚀 Quick Start (Developer Demo)

### Prerequisites

- Python 3.8+
- Google OAuth2 credentials (Client ID and Client Secret)
- LiteLLM API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dinhdobathi1992/litellm-wrapper-ui.git
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

4. **Set up developer environment variables**
   ```bash
   cp env.dev.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   # LiteLLM API Configuration
   LITELLM_API_KEY=your_api_key_here
   LITELLM_API_BASE=https://your-litellm-proxy.com
   
   # Application Configuration
   APP_VERSION=3.0.0-dev
   
   # Google OAuth2 Configuration
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   SECRET_KEY=your_secret_key_here_change_this_in_production
   
   # Developer Demo Configuration
   DEV_MODE=true
   ADMIN_EMAIL=dinhdobathi@gmail.com
   DEMO_REQUEST_LIMIT=2
   DEMO_TOKEN_LIMIT=100
   
   # Google OAuth2 Redirect URI (for development)
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
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

2. **Update Environment Variables**
   - Copy the Client ID and Client Secret to your `.env` file
   - Generate a secure SECRET_KEY (you can use `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

### Running the Developer Demo

1. **Start the developer server**
   ```bash
   # Using bash
   chmod +x start_dev.sh && ./start_dev.sh
   
   # Using fish shell
   chmod +x start_dev.fish && ./start_dev.fish
   
   # Or directly
   source venv/bin/activate && python main_dev.py
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - You'll be redirected to the login page
   - Click "Sign in with Google" to authenticate
   - After successful authentication, you'll be redirected to the chat interface

## 👑 User Access Levels

### Admin Users (dinhdobathi@gmail.com)
- ✅ **Unlimited requests** - No restrictions
- ✅ **Unlimited tokens** - No token limits
- ✅ **Full features** - All functionality available
- ✅ **Priority access** - No rate limiting

### Demo Users (All other emails)
- 🎪 **Limited requests** - 2 requests maximum (configurable)
- 🎪 **Limited tokens** - 100 tokens maximum (configurable)
- 🎪 **Full UI experience** - All features visible but limited usage
- 🎪 **Usage tracking** - Real-time usage monitoring

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LITELLM_API_KEY` | Your LiteLLM API key | Yes | - |
| `LITELLM_API_BASE` | LiteLLM API base URL | No | `https://your-litellm-proxy.com` |
| `APP_VERSION` | Application version | No | `3.0.0-dev` |
| `GOOGLE_CLIENT_ID` | Google OAuth2 Client ID | Yes | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 Client Secret | Yes | - |
| `SECRET_KEY` | Session encryption key | Yes | Auto-generated |
| `DEV_MODE` | Enable developer mode | No | `true` |
| `ADMIN_EMAIL` | Admin user email | No | `dinhdobathi@gmail.com` |
| `DEMO_REQUEST_LIMIT` | Demo request limit | No | `2` |
| `DEMO_TOKEN_LIMIT` | Demo token limit | No | `100` |
| `GOOGLE_REDIRECT_URI` | OAuth redirect URI | No | `http://localhost:8000/auth/callback` |

### Customizing Demo Limits

You can adjust the demo limits by modifying these environment variables:

```env
# More generous demo limits
DEMO_REQUEST_LIMIT=5
DEMO_TOKEN_LIMIT=200

# Stricter demo limits
DEMO_REQUEST_LIMIT=1
DEMO_TOKEN_LIMIT=50
```

## 📊 Usage Monitoring

### API Endpoints

- **`/api/usage`** - Get current usage for authenticated user
  - Returns usage statistics and limits
  - Different response for admin vs demo users

### Usage Tracking

The application tracks:
- **Request count** - Number of API calls made
- **Token count** - Estimated tokens consumed
- **User type** - Admin or demo user
- **Limit status** - Whether limits have been reached

## 🚀 Deployment

### Vercel Deployment (Demo Environment)

1. **Create a new Vercel project** for the demo
2. **Set environment variables** in Vercel dashboard
3. **Update Google OAuth2 redirect URIs** to include your Vercel domain
4. **Deploy using the developer files**

### Environment Variables for Production Demo

```env
# Production demo settings
GOOGLE_REDIRECT_URI=https://your-demo-domain.vercel.app/auth/callback
DEMO_REQUEST_LIMIT=3
DEMO_TOKEN_LIMIT=150
```

## 🎯 Use Cases

### Perfect For:
- **🎪 Demo presentations** - Showcase features without costs
- **🧪 Testing environments** - Safe testing with limited usage
- **📚 Educational purposes** - Teach AI concepts with controlled access
- **🔍 Proof of concepts** - Demonstrate capabilities to stakeholders
- **💰 Cost control** - Prevent unexpected API charges

### Demo User Experience:
- **Full UI access** - Users see all features
- **Limited functionality** - Restricted API calls
- **Clear feedback** - Usage limits clearly communicated
- **Graceful degradation** - Friendly error messages when limits reached

## 🔒 Security Features

- **OAuth2 Authentication** - Secure Google login
- **Usage tracking** - Monitor and limit API consumption
- **Session management** - Encrypted session storage
- **Input validation** - Server-side validation for all inputs
- **Error handling** - Secure error messages without information leakage

## 📝 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Main chat interface | Yes |
| `/login` | GET | Login page | No |
| `/auth/google` | GET | Initiate Google OAuth | No |
| `/auth/callback` | GET | OAuth callback handler | No |
| `/logout` | GET | Logout user | Yes |
| `/api/models` | GET | Get available models | Yes |
| `/api/chat` | POST | Send chat message | Yes (with limits) |
| `/api/chat-history/{session_id}` | GET | Get chat history | Yes |
| `/api/new-session` | POST | Create new session | Yes |
| `/api/usage` | GET | Get user usage statistics | Yes |

## 🛠️ Development

### Project Structure (Developer Version)
```
litellm-wrapper-ui/
├── main_dev.py           # Developer version of main application
├── auth_dev.py           # Developer authentication with usage tracking
├── env.dev.example       # Developer environment template
├── start_dev.sh          # Developer startup script (bash)
├── start_dev.fish        # Developer startup script (fish)
├── README_DEV.md         # This file
├── main.py              # Production version
├── auth.py              # Production authentication
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   ├── chat.html       # Main chat interface
│   └── login.html      # Login page
└── README.md           # Production README
```

### Running Tests
```bash
# Test the developer application
curl http://localhost:8000/login
curl http://localhost:8000/  # Should redirect to login
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with both admin and demo users
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**ThiThi**
- GitHub: [dinhdobathi1992](https://github.com/dinhdobathi1992/litellm-wrapper-ui)
- Portfolio: [dinhdobathi.com](https://dinhdobathi.com)

## 🔄 Version History

- **v3.0.0-dev** - Added developer demo mode with usage restrictions
- **v2.0.0** - Added PDF support, image generation, multi-format file processing
- **v1.3.0** - Added email/domain access control, sticky layout, chat history sidebar
- **v1.2.0** - Added Google OAuth2 authentication, enhanced UI
- **v1.1.0** - Enhanced UI, file upload, session management
- **v1.0.0** - Initial release with basic chat functionality

## 🆘 Support

If you encounter any issues:
1. Check the environment variables are correctly set
2. Verify Google OAuth2 credentials are valid
3. Ensure LiteLLM API is accessible
4. Check the server logs for detailed error messages
5. Verify demo limits if users can't make requests

---

**Powered by LiteLLM • v3.0.0-dev (Developer Demo)** 🎭 