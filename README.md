# Zen's LiteLLM Chat Application

A modern, lightweight web chat application built with FastAPI and TailwindCSS that integrates with LiteLLM API for AI-powered conversations. Features Google OAuth2 authentication with email/domain access control, PDF processing, and AI image generation capabilities.

## ✨ Features

- 🔐 **Google OAuth2 Authentication** - Secure login with Google accounts
- 🛡️ **Access Control** - Restrict access by email addresses or domains
- 🤖 **AI Chat Interface** - Powered by LiteLLM API with multiple model support
- 📁 **Advanced File Upload Support** - Upload and analyze PDF, DOCX, Excel, images, and text files
- 🖼️ **AI Image Generation** - Generate images using DALL-E and other image models *(Work in Progress)*
- 🌙 **Dark Mode** - Toggle between light and dark themes
- 💾 **Session Management** - Persistent chat sessions with chat history sidebar
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Professional ChatGPT-like interface with sticky layout
- 🔄 **Real-time Chat** - Instant message sending and receiving
- 📊 **Markdown Rendering** - Rich formatting for AI responses with image support
- 🚀 **Performance Optimized** - Response caching and model parameter tuning
- 📋 **Chat History** - Left sidebar with session management
- 🎯 **Custom Model Selection** - ChatGPT-style dropdown for model selection

## 📁 Supported File Extensions

The application supports a wide range of file formats for analysis and processing:

### 📄 **Document Files**
- **PDF** (`.pdf`) - Extract and analyze text content from PDF documents
- **Word Documents** (`.docx`) - Process Microsoft Word documents
- **Excel Spreadsheets** (`.xlsx`, `.xls`) - Analyze Excel data and tables
- **Text Files** (`.txt`, `.md`, `.log`) - Process plain text and markdown files
- **Data Files** (`.json`, `.yaml`, `.yml`, `.csv`) - Analyze structured data

### 🖼️ **Image Files**
- **JPEG** (`.jpg`, `.jpeg`) - Extract image metadata and analyze content
- **PNG** (`.png`) - Process PNG images with metadata extraction
- **GIF** (`.gif`) - Handle animated GIF files
- **BMP** (`.bmp`) - Process bitmap images
- **WebP** (`.webp`) - Support for modern web image format

### 🔧 **File Processing Features**
- **Text Extraction** - Extract readable text from documents
- **Metadata Analysis** - Get file information and properties
- **Content Truncation** - Large files are automatically truncated to 4000 characters
- **Error Handling** - Graceful handling of unsupported or corrupted files
- **Base64 Encoding** - Secure file transmission to backend

### 📊 **Analysis Capabilities**
- **Document Analysis** - Extract key information from PDFs and Word docs
- **Data Analysis** - Process Excel spreadsheets and CSV files
- **Code Review** - Analyze JSON, YAML, and other structured data
- **Image Analysis** - Extract metadata and properties from images
- **Log Analysis** - Process and analyze log files

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google OAuth2 credentials (Client ID and Client Secret)

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
   APP_VERSION=2.0.0
   
   # Google OAuth2 Configuration
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   SECRET_KEY=your_secret_key_here_change_this_in_production
   
   # Access Control Configuration
   # Comma-separated list of allowed email addresses (leave empty to allow all)
   ALLOWED_EMAILS=user1@gmail.com,user2@company.com
   # Allowed domain (leave empty to allow all domains)
   ALLOWED_DOMAIN=yourcompany.com
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
| `APP_VERSION` | Application version | No | `2.0.0` |
| `GOOGLE_CLIENT_ID` | Google OAuth2 Client ID | Yes | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 Client Secret | Yes | - |
| `SECRET_KEY` | Session encryption key | Yes | Auto-generated |
| `ALLOWED_EMAILS` | Comma-separated allowed emails | No | Allow all |
| `ALLOWED_DOMAIN` | Allowed email domain | No | Allow all |

### Access Control Configuration

**Option 1: Restrict by Specific Emails**
```env
ALLOWED_EMAILS=user1@gmail.com,user2@company.com,admin@yourdomain.com
ALLOWED_DOMAIN=
```

**Option 2: Restrict by Domain**
```env
ALLOWED_EMAILS=
ALLOWED_DOMAIN=yourcompany.com
```

**Option 3: Both (must match either)**
```env
ALLOWED_EMAILS=admin@gmail.com,ceo@company.com
ALLOWED_DOMAIN=yourcompany.com
```

**Option 4: Allow All (default)**
```env
ALLOWED_EMAILS=
ALLOWED_DOMAIN=
```

### Features Configuration

- **Default Model**: The application automatically selects GPT-4o as the default model when available
- **File Upload**: Supports PDF, DOCX, Excel, images, and text files up to 4000 characters (truncated if larger)
- **Image Generation**: Supports DALL-E and other image generation models *(Work in Progress)*
- **Session Storage**: Chat sessions are stored in memory (replace with database for production)
- **Response Caching**: In-memory cache for faster repeated queries
- **Model Optimization**: Optimized parameters for faster AI responses

## 🚧 Work in Progress (WIP)

### 🖼️ **Image Generation Feature**
The image generation feature is currently in development and may have limitations:

#### ✅ **What's Working:**
- **Image Generation Button**: Purple toggle button in the chat interface
- **DALL-E Integration**: Support for DALL-E models via LiteLLM API
- **Prompt Enhancement**: Automatic enhancement of user prompts for better image generation
- **Error Handling**: Graceful fallback when image generation fails
- **UI Integration**: Image mode toggle with visual indicators

#### 🔧 **Current Limitations:**
- **API Compatibility**: Some LiteLLM endpoints may not support image generation
- **Model Availability**: DALL-E models may not be available in all LiteLLM deployments
- **Error Handling**: 400 Bad Request errors may occur with certain API configurations
- **Fallback Behavior**: Falls back to text generation when image generation fails

#### 🚀 **Planned Improvements:**
- **Better Error Messages**: More specific error handling for different failure scenarios
- **Model Detection**: Automatic detection of available image generation models
- **Alternative Endpoints**: Support for different image generation API endpoints
- **Image Quality Options**: Configurable image size and quality settings
- **Batch Generation**: Support for generating multiple images at once

#### 💡 **Usage Tips:**
- **For Best Results**: Use clear, descriptive prompts for image generation
- **Model Selection**: Try different models if image generation fails
- **File Uploads**: Image generation works best without file uploads
- **Error Recovery**: If image generation fails, try regular chat mode instead

## 🏗️ Architecture

### Backend (FastAPI)
- **Authentication**: Google OAuth2 with session management and access control
- **API Integration**: LiteLLM API for AI model access and image generation
- **File Handling**: Multi-format file processing (PDF, DOCX, Excel, images, text)
- **Image Generation**: DALL-E and other image model integration *(Work in Progress)*
- **Session Management**: In-memory storage with UUID-based sessions
- **Response Caching**: In-memory cache for improved performance

### Frontend (HTML/JavaScript)
- **UI Framework**: TailwindCSS for styling
- **Theme Support**: Dark/light mode toggle
- **Markdown Rendering**: Custom markdown parser for AI responses with image support
- **File Upload**: Multi-format drag-and-drop and click-to-upload support
- **Image Generation**: Toggle button for image generation mode *(Work in Progress)*
- **Chat History**: Left sidebar with session management
- **Sticky Layout**: Fixed sidebar and header with scrollable chat area

## 🔒 Security Features

- **OAuth2 Authentication**: Secure Google login
- **Access Control**: Email and domain-based restrictions
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
├── auth.py              # Authentication module with access control
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── env.example          # Environment template
├── templates/           # HTML templates
│   ├── chat.html       # Main chat interface
│   └── login.html      # Login page
├── v1.0.0/             # Backup of v1.0.0
├── v1.1.0/             # Backup of v1.1.0
├── v1.2.0/             # Backup of v1.2.0
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

- **v2.0.0** - Added PDF support, image generation, multi-format file processing, DALL-E integration
- **v1.3.0** - Added email/domain access control, sticky layout, chat history sidebar, performance optimizations
- **v1.2.0** - Added Google OAuth2 authentication, enhanced UI
- **v1.1.0** - Enhanced UI, file upload, session management
- **v1.0.0** - Initial release with basic chat functionality

## 🆘 Support

If you encounter any issues:
1. Check the environment variables are correctly set
2. Verify Google OAuth2 credentials are valid
3. Ensure LiteLLM API is accessible
4. Check the server logs for detailed error messages
5. Verify access control settings if users can't log in

---

**Powered by LiteLLM • v2.0.0** 