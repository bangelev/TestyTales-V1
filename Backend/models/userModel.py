from pymongo import MongoClient
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


import os

db_uri = os.getenv('DB_LOCAL_URI')
client = MongoClient(db_uri)
db = client['TastyTales']
users_collection = db['users']


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_name: str
    name: str = None
    email: str = None
    avatar_url: str = None
    role: str = 'user'
    created_at: datetime = Field(default_factory=datetime.now)