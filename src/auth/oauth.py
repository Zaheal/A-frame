from httpx_oauth.clients.google import GoogleOAuth2

from src.config.auth_config import get_auth_settings

settings = get_auth_settings()

google_oauth_client = GoogleOAuth2(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET)
