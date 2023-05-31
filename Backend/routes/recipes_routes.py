from fastapi import APIRouter, HTTPException
from typing import List, Optional

# from pydantic import BaseModel, Field
from pymongo import ReturnDocument



from pymongo.errors import PyMongoError
from bson import json_util
from fastapi.encoders import jsonable_encoder


from models.recipeModel import Recipe, RecipeCreate, RecipeUpdate, recipes_collection

recipes_router = APIRouter()


# GET method to retrieve all recipes

# @recipes_router.get("/recipes", response_model=List[Recipe])
# async def get_recipes():
#     try:
#         recipes = recipes_collection.find({})

#         return list(recipes)
#     except PyMongoError as exc:
#         raise HTTPException(status_code=500, detail="MongoDB error occurred")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Internal server error")

@recipes_router.get("/recipes", response_model=List[Recipe])
async def get_recipes(limit: int = 10, category: Optional[str] = None):
    try:
        query = {}

        if category:
            query["category"] = category

        recipes = recipes_collection.find(query).limit(limit)

        return list(recipes)
    except PyMongoError as exc:
        raise HTTPException(status_code=500, detail="MongoDB error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# GET method to retrieve a recipe

@recipes_router.get("/recipes/{id}")
async def get_single_recipe(id: str):

    recipe = recipes_collection.find_one({"_id": id})
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"recipe": recipe}


# POST method to add a new recipe

@recipes_router.post("/recipes", response_model=Recipe)
async def add_recipe(recipe: RecipeCreate):
    try:
        new_recipe = Recipe(**recipe.dict())

        new_recipe_id = recipes_collection.insert_one(
            jsonable_encoder(new_recipe)).inserted_id

        new_recipe.id = str(new_recipe_id)
        return new_recipe
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# PUT method to update a recipe by ID

# @recipes_router.put("/recipes/{recipe_id}")
# async def update_recipe(recipe_id: str, recipe: RecipeUpdate):
#     existing_recipe = recipes_collection.find_one({"_id": recipe_id})
#     if existing_recipe is None:
#         raise HTTPException(status_code=404, detail="Recipe not found")
#     result = recipes_collection.update_one(
#         {"_id": recipe_id}, {"$set": jsonable_encoder(recipe)})
# # ************************** CREATE ERROR IN TEST FILE????  *****************
#     # Check the result of the update operation
#     print(result.modified_count)
#     # if result.modified_count == 0:
#     #     raise HTTPException(
#     #         status_code=500, detail="Failed to update document")
# # ***************************************************************************
#     return {"message": f"Recipe with id:{recipe_id} update successfully"}
@recipes_router.put("/recipes/{recipe_id}")
async def update_recipe(recipe_id: str, recipe: RecipeUpdate):
    existing_recipe = recipes_collection.find_one_and_update(
        {"_id": recipe_id},
        {"$set": jsonable_encoder(recipe)},
        return_document=ReturnDocument.AFTER
    )

    if existing_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"message": f"Recipe with id:{recipe_id} update successfully"}


# DELETE method to delete a recipe by ID

@recipes_router.delete("/recipes/{id}")
async def delete_recipe(id: str):
    recipe = recipes_collection.find_one({"_id": id})
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipes_collection.delete_one({"_id": id})
    return {"message": f"Recipe with id:{id} deleted successfully"}
