from fastapi import Cookie
from fastapi import APIRouter, Request, HTTPException, Response


from datetime import datetime, timedelta

import os

import jwt

from jwt.exceptions import InvalidTokenError
from models.userModel import User, users_collection


jwt_secret_key = os.getenv("JWT_SECRET_KEY")


user_router = APIRouter()


# Endpoint to load authenticated user

@user_router.get("/users/")
async def load_signup_user(access_token: str = Cookie(None)):
    """
    Load signup user information based on the provided access token.

    Parameters:
    - access_token (str, optional): The access token obtained from the client's cookie.

    Returns:
    - dict: User information if the access token is valid and the user exists.
    - None: If not access token

    Raises:
    - HTTPException(401): If the access token is invalid or expired.
    - HTTPException(404): If the user is not found.
    """

    try:
        if access_token:

            # Decoding the access token to get the user_id
            payload = jwt.decode(
                access_token, jwt_secret_key, algorithms=["HS256"])
            user_id = payload.get("user_id")
            expiration = payload.get("exp")

            # Checking if the token has expired
            if expiration is not None and datetime.utcnow() > datetime.fromtimestamp(expiration):
                raise HTTPException(status_code=401, detail="Token expired")

            user = users_collection.find_one({"_id": user_id})
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {
                "user": user,
                "success": True
            }
        else:
            return None
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Endpoint to invalidate the access token

@user_router.post("/users/logout")
async def logout(request: Request, response: Response, access_token: str = Cookie(None)):
    """
    Invalidate the access token and perform a logout.

    Parameters:
    - request (Request): The incoming request object.
    - response (Response): The outgoing response object.
    - access_token (str, optional): The access token obtained from the client's cookie.

    Returns:
    - dict: A response indicating successful logout.

    Raises:
    - HTTPException(401): If the access token is invalid or not provided.
    """

    if access_token:

        # Perform any necessary actions to invalidate the token
        response.delete_cookie("access_token")

        # Return a response indicating successful logout
        return {"message": "Logged out successfully"}
    else:
        raise HTTPException(
            status_code=401, detail="Invalid token, NOT token sent")
