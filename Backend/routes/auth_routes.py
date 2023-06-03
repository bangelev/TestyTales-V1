
import jwt
import httpx
from utils.save_user_in_db import save_GitHub_user_in_DB
import os
from datetime import datetime, timedelta
import json
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv


load_dotenv()


jwt_secret_key = os.getenv("JWT_SECRET_KEY")

auth_router = APIRouter()


# GitHub settings
client_id = os.getenv('github_client_id')

client_secret = os.getenv('githib_client_secret')
redirect_uri = "http://localhost:4000/auth/callback"
token_url = "https://github.com/login/oauth/access_token"
scope = ["user:email"]
authorization_base_url = f"https://github.com/login/oauth/authorize?client_id={client_id}&scope={scope}"


@auth_router.get("/auth/github")
async def gitHub_login(request: Request):
    """
    Initiate GitHub login.

    - `request`: The request object.

    Returns a redirect response to the GitHub authorization URL.
    """

    return RedirectResponse(authorization_base_url)


@auth_router.get("/auth/callback")
async def callback(request: Request, code: str = None):
    """
    Handle GitHub login callback.

    - `request`: The request object.
    - `code`: The authorization code received from GitHub.

    Returns a redirect response with an access token with DB user information as a cookie.
    """

    if code is None:
        raise HTTPException(
            status_code=400, detail="Authorization code not provided")

    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,

    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, params=params, headers=headers)

    response_json = json.loads(response.text)
    if "access_token" not in response_json:
        raise HTTPException(
            status_code=400, detail="Access token not found in response")

    access_token = response_json["access_token"]

    headers.update({'Authorization': f'Bearer {access_token}'})
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/user", headers=headers)
        user_info = response.json()
        if "login" not in user_info:
            raise HTTPException(
                status_code=400, detail="User login name not found in response")

        user_id = save_GitHub_user_in_DB(user_info)

    # Generate JWT token
    token_data = {
        "user_id": str(user_id),
        "token_type": "bearer",
        # Set an appropriate expiration time
        "exp": (datetime.utcnow() + timedelta(days=7)),
    }
    token = jwt.encode(token_data, jwt_secret_key, algorithm="HS256")

    # Create a redirect response

    redirect_url = "http://localhost:4000/"
    redirect_response = RedirectResponse(
        url=f"{redirect_url}")

    # Set the token as a cookie in the response
    redirect_response.set_cookie(key="access_token", value=token)

    # Return the RedirectResponse
    return redirect_response
