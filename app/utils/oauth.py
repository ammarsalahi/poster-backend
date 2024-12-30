from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.config import settings

config = Config("../.env")

# Set up OAuth
oauth = OAuth(config)
google = oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={
        "scope": "openid email profile",
    },
)
