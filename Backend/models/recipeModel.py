from datetime import datetime
from pymongo import MongoClient

from pydantic import BaseModel, Field, validator
from typing import List, Optional
import uuid
import os

from enum import Enum

db_uri = os.getenv('DB_LOCAL_URI')

client = MongoClient(db_uri)
db = client['TastyTales']
recipes_collection = db['recipes']


class CategoryModel(str, Enum):
    Macedonian = "Macedonian"
    Italian = "Italian"
    Chinese = "Chinese"
    French = "French"
    Japanese = "Japanese"
    Indian = "Indian"
    Spanish = "Spanish"
    Mexican = "Mexican"
    Greek = "Greek"
    Thai = "Thai"
    Lebanese = "Lebanese",
    World = "World",
    Sweet = "Sweet"


class Recipe(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str
    category: Optional[CategoryModel]
    ingredients: List[str]
    instructions: List[str]
    approximate_time: str
    created_at: str = str(datetime.now())


class RecipeCreate(BaseModel):
    name: str
    category: str
    ingredients: List[str]
    instructions: List[str]
    approximate_time: str

    @validator('name', 'category', 'ingredients', 'instructions', 'approximate_time')
    def field_required(cls, value):
        if not value:
            raise ValueError("Field is required")
        return value


class RecipeUpdate(BaseModel):
    name: str
    category: Optional[CategoryModel]
    ingredients: List[str]
    instructions: List[str]
    approximate_time: str
