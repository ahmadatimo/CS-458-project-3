from fastapi import Response
from fastapi.responses import JSONResponse

class LogoutManager:
    @staticmethod
    def clear_user_session(response: Response):
        """Clear the user's session (e.g., delete the auth token)."""
        response.delete_cookie(
            key="auth_token",
            path="/",  # Ensure the cookie is deleted for all paths
            domain="localhost",  # Match the domain where the cookie was set
            secure=False,  # Set to True if using HTTPS
            httponly=True,  # Ensure the cookie is HTTP-only
            samesite="lax",  # Prevent CSRF attacks
        )
        return JSONResponse(content={"message": "✅ Successfully logged out!"})