from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt
import httpx, os

app = FastAPI(title="THE DIGZOPIAN VISION")

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
CALLBACK_URL = os.getenv("OAUTH_CALLBACK_URL")
AUTH_DOMAIN = "https://github.com"

@app.get("/")
def root():
    return {"message": "🌟 Welcome to THE DIGZOPIAN VISION – Freedom Engine Online"}

@app.get("/login")
def login():
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={CALLBACK_URL}&scope=read:user"
    )

@app.get("/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "redirect_uri": CALLBACK_URL,
            },
            headers={"Accept": "application/json"},
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return {"user": user_resp.json(), "message": "Liberation confirmed"}
