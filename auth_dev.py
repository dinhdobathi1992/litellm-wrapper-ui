import os
import secrets
import httpx
from typing import Optional
from fastapi import HTTPException, Request
from starlette.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv('.env.dev')

# Session management
SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

# Developer mode configuration
DEV_MODE = os.getenv('DEV_MODE', 'false').lower() == 'true'
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'dinhdobathi@gmail.com')
DEMO_REQUEST_LIMIT = int(os.getenv('DEMO_REQUEST_LIMIT', '2'))
DEMO_TOKEN_LIMIT = int(os.getenv('DEMO_TOKEN_LIMIT', '100'))

# In-memory user storage and usage tracking
users = {}
user_usage = {}  # Track API usage for demo users

def is_admin_user(email: str) -> bool:
    """Check if user is admin (unlimited access)"""
    return email == ADMIN_EMAIL

def get_user_usage(email: str) -> dict:
    """Get current usage for a user"""
    if email not in user_usage:
        user_usage[email] = {
            'request_count': 0,
            'token_count': 0,
            'last_reset': None
        }
    return user_usage[email]

def check_demo_limits(email: str) -> tuple[bool, str]:
    """
    Check if demo user has exceeded limits.
    Returns (can_proceed, error_message)
    """
    if is_admin_user(email):
        return True, ""
    
    usage = get_user_usage(email)
    
    # Check request limit
    if usage['request_count'] >= DEMO_REQUEST_LIMIT:
        return False, f"Demo limit reached ({DEMO_REQUEST_LIMIT} requests). Contact admin for full access."
    
    # Check token limit (approximate)
    if usage['token_count'] >= DEMO_TOKEN_LIMIT:
        return False, f"Demo token limit reached ({DEMO_TOKEN_LIMIT} tokens). Contact admin for full access."
    
    return True, ""

def increment_usage(email: str, estimated_tokens: int = 50):
    """Increment usage counters for demo users"""
    if is_admin_user(email):
        return
    
    usage = get_user_usage(email)
    usage['request_count'] += 1
    usage['token_count'] += estimated_tokens

def get_current_user(request: Request) -> Optional[dict]:
    """Get current user from session"""
    user = request.session.get('user')
    if not user:
        return None
    return user

def require_auth(request: Request) -> dict:
    """Require authentication - redirect to login if not authenticated"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

async def login_google(request: Request):
    """Initiate Google OAuth login"""
    # Generate state parameter for security
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    
    # Build Google OAuth URL
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"scope=openid%20email%20profile&"
        f"response_type=code&"
        f"state={state}"
    )
    
    return RedirectResponse(url=auth_url, status_code=302)

async def auth_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        # Get authorization code and state from query parameters
        code = request.query_params.get('code')
        state = request.query_params.get('state')
        
        # Verify state parameter
        if state != request.session.get('oauth_state'):
            return RedirectResponse(url='/login?error=invalid_state', status_code=302)
        
        if not code:
            return RedirectResponse(url='/login?error=no_code', status_code=302)
        
        # Exchange code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': GOOGLE_REDIRECT_URI
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            token_info = token_response.json()
            
            # Get user info using access token
            userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f"Bearer {token_info['access_token']}"}
            user_response = await client.get(userinfo_url, headers=headers)
            user_response.raise_for_status()
            user_info = user_response.json()
            
            # Store user in session (no access restrictions in dev mode)
            user = {
                'id': user_info['id'],
                'email': user_info['email'],
                'name': user_info.get('name', ''),
                'picture': user_info.get('picture', ''),
                'is_admin': is_admin_user(user_info['email']),
                'usage': get_user_usage(user_info['email'])
            }
            
            # Debug: Print user info
            print(f"🔍 Debug: User info received from Google:")
            print(f"  - ID: {user['id']}")
            print(f"  - Email: {user['email']}")
            print(f"  - Name: {user['name']}")
            print(f"  - Is Admin: {user['is_admin']}")
            print(f"  - Usage: {user['usage']}")
            
            if user['is_admin']:
                print(f"✅ Admin access granted for {user['email']}")
            else:
                print(f"🎭 Demo access granted for {user['email']} (limited to {DEMO_REQUEST_LIMIT} requests)")
            
            request.session['user'] = user
            
            # Store in memory
            users[user['id']] = user
            
            # Clear OAuth state
            request.session.pop('oauth_state', None)
            
            return RedirectResponse(url='/', status_code=302)
            
    except Exception as e:
        print(f"OAuth error: {e}")
        return RedirectResponse(url='/login?error=auth_failed', status_code=302)

async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return RedirectResponse(url='/login', status_code=302) 