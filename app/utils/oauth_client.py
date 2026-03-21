from app.core.config import settings
import httpx
from app.models.user_model import User


google_client_id = settings.GOOGLE_CLIENT_ID
google_secret = settings.GOOGLE_SECRET
google_uri = settings.GOOGLE_REDIRECT_URI

async def exchange_code_for_code(code:str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post("https://oauth2.googleapis.com/token", data = {
            "code" : code,
            "client_id" : google_client_id,
            "cliend_secret" : google_secret,
            "redirect uri" : google_uri,
            "grant_type" : "authorization_code",


        })
        response.raise_for_status()
        return response.json()["access_token"]
    
async def get_google_user(access_token:str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.googleapis.com/oauth2/v2/userinfo", headers = {
            "Authorization" : f"Bearer {access_token}"
        })
        response.raise_for_status()
        response.json()
