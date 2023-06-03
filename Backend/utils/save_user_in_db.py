
from fastapi.encoders import jsonable_encoder
from models.userModel import User, users_collection


# GITHUB USER


def save_GitHub_user_in_DB(user_info):
    user_exists = users_collection.find_one(
        {"user_name": user_info.get("login")})

    if user_exists:
        print("User  already exists in the database.")
        return user_exists['_id']
    else:
        print("User does NOT exist in the database.")
        user_data = User(
            user_name=user_info.get("login"),
            name=user_info.get("name"),
            email=user_info.get("email"),
            avatar_url=user_info.get("avatar_url"),
            role='user'
        )
        user_id = users_collection.insert_one(
            jsonable_encoder(user_data)).inserted_id
        return user_id
