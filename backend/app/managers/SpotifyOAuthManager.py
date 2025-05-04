import httpx
from fastapi import HTTPException

class SpotifyOAuthManager:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.SPOTIFY_CLIENT_ID = client_id
        self.SPOTIFY_CLIENT_SECRET = client_secret
        self.SPOTIFY_REDIRECT_URI = redirect_uri

    async def exchange_code_for_token(self, code):
        """Exchange the authorization code for an access token."""
        async with httpx.AsyncClient() as client:
            try:
                token_response = await client.post(
                    "https://accounts.spotify.com/api/token",
                    data={
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": self.SPOTIFY_REDIRECT_URI,
                        "client_id": self.SPOTIFY_CLIENT_ID,
                        "client_secret": self.SPOTIFY_CLIENT_SECRET,
                    },
                )
                token_response.raise_for_status()
                return token_response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=400, detail=f"Failed to exchange code for token: {e.response.text}")

    async def fetch_user_data(self, access_token):
        """Fetch user data using the access token."""
        async with httpx.AsyncClient() as client:
            try:
                user_response = await client.get(
                    "https://api.spotify.com/v1/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                user_response.raise_for_status()
                return user_response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=400, detail=f"Failed to fetch user data: {e.response.text}")