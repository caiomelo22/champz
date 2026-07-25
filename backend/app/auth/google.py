import os

from httpx_oauth.clients.google import GoogleOAuth2

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

google_oauth_client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
