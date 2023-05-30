import json
from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

from fastapi.encoders import jsonable_encoder


from enum import Enum


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


try:
    # Establish a connection to MongoDB
    client = MongoClient('mongodb://localhost:27017')
    db = client['TastyTales']
    collection = db['recipes']

    # Delete all documents in the collection
    collection.delete_many({})
    print("Documents in collection deleted")

    # Load the JSON data from the file
    with open('./recipes.json', "rb") as file:
        data = json.load(file)

    # Create Recipe objects from the JSON data
    recipes = []
    for item in data:
        recipe = Recipe(

            name=item.get('name'),
            category=item.get('category'),
            ingredients=item.get('ingredients'),
            instructions=item.get('preparations'),
            approximate_time=item.get('approximate_time')
        )
        # recipes.append(recipe.dict())
        collection.insert_one(jsonable_encoder(recipe))

    # Insert the recipes into the collection
    # collection.insert_many(recipes)

    # Close the MongoDB connection
    client.close()
    print('Database successfully seeded')
except Exception as e:
    print("An error occurred:", e)
