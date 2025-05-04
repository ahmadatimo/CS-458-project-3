from fastapi import APIRouter, Request, Response, HTTPException
from app.managers.AuthManager import AuthManager
from app.managers.SpotifyOAuthManager import SpotifyOAuthManager
from app.managers.LogoutManager import LogoutManager
from app.models.LoginRequest import LoginRequest

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest):
    """Handle the login request."""
    auth_manager = AuthManager()
    return auth_manager.process_login(request.email, request.password)

@router.get("/spotify/callback")
async def spotify_callback(request: Request, response: Response):
    """Handle the Spotify OAuth callback."""
    code = request.query_params.get("code")

    # Validate the authorization code
    SpotifyOAuthManager.validate_authorization_code(code)

    # Exchange the code for a token
    token_data = await SpotifyOAuthManager.exchange_code_for_token(code)

    # Validate the token response
    SpotifyOAuthManager.validate_token_response(token_data)

    # Validate the access token
    access_token = token_data.get("access_token")
    SpotifyOAuthManager.validate_access_token(access_token)

    # Fetch user data
    user_data = await SpotifyOAuthManager.fetch_user_data(access_token)

    # Set a cookie for the user session
    user_token = "some_generated_token"
    response.set_cookie(key="auth_token", value=user_token, httponly=True, max_age=3600)

    return {
        "message": "✅ Spotify login successful!",
        "user": {
            "spotify_id": user_data.get("id"),
            "display_name": user_data.get("display_name"),
            "email": user_data.get("email"),
        },
    }

@router.post("/logout")
def logout(response: Response):
    """Handle the logout request."""
    return LogoutManager.clear_user_session(response)