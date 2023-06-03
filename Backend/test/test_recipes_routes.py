from app import app
from fastapi.testclient import TestClient
from pymongo.errors import PyMongoError
from fastapi.encoders import jsonable_encoder
from unittest.mock import MagicMock
from models.recipeModel import recipes_collection, Recipe

from fastapi.encoders import jsonable_encoder

client = TestClient(app)

# **************************************************************
# GET /recipes/{id}


def test_get_single_recipe():
    existing_recipe_data = {
        "name": "Spaghetti",
        "category": "Italian",
        "ingredients": ["pasta", "sauce", "meat"],
        "instructions": ["Step 1", "Step 2", "Step 3"],
        "approximate_time": "40 minutes"
    }
    existing_recipe = Recipe(**existing_recipe_data)
    existing_recipe_id = recipes_collection.insert_one(
        jsonable_encoder(existing_recipe)).inserted_id

    response = client.get(f"/recipes/{existing_recipe_id}")
    assert response.status_code == 200
    assert "recipe" in response.json()
    recipes_collection.delete_one({"_id": existing_recipe_id})


def test_get_single_recipe_not_found():

    recipe_id = "non_existent_id"
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"

# ******************************************************************
# GET /recipes


def test_get_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) > 0

    assert isinstance(response.json(), list)


def test_get_recipes_with_limit():
    response = client.get("/recipes?limit=5")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 5
    assert isinstance(response.json(), list)


def test_get_recipes_by_category():
    response = client.get("/recipes?category=Italian")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) > 0
    for recipe in recipes:
        assert recipe["category"] == "Italian"


def test_get_recipes_with_limit_and_category():
    response = client.get("/recipes?limit=3&category=World")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 3
    for recipe in recipes:
        assert recipe["category"] == "World"


def test_get_recipes_mongodb_error(mocker):
    mocker.patch.object(recipes_collection, "find", side_effect=PyMongoError)
    response = client.get("/recipes")
    assert response.status_code == 500
    assert response.json() == {"detail": "MongoDB error occurred"}


def test_get_recipes_internal_server_error(mocker):
    mocker.patch.object(recipes_collection, "find",
                        side_effect=Exception("Some error"))
    response = client.get("/recipes")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

# ******************************************************************
# POST /recipes  CREATE


def test_add_recipe():
    recipe_data = {
        "name": "Omelette",
        "category": "World",
        "ingredients": ["3 eggs", "1/4 cup milk"],
        "instructions": ["Step 1", "Step 2"],
        "approximate_time": "10-15 minutes"
    }

    response = client.post("/recipes", json=recipe_data)

    assert response.status_code == 200
    assert response.json()["name"] == "Omelette"
    assert response.json()["category"] == "World"
    assert response.json()["ingredients"] == ["3 eggs", "1/4 cup milk"]
    assert response.json()["instructions"] == ["Step 1", "Step 2"]
    assert "_id" in response.json()
    recipes_collection.delete_one({"_id": response.json()["_id"]})


def test_add_recipe_validation_error():
    invalid_recipe_data = {
        "name": "Omelette",
        "category": "World",
        "instructions": ["Step 1", "Step 2"],
        "approximate_time": "10-15 minutes"
    }

    response = client.post("/recipes", json=invalid_recipe_data)

    assert response.status_code == 422
    assert "detail" in response.json()
    assert "ingredients" in response.json()["detail"][0].get("loc")


def test_add_recipe_internal_server_error(mocker):
    mocker.patch.object(recipes_collection, "insert_one",
                        side_effect=Exception("Some error"))

    recipe_data = {
        "name": "Omelette",
        "category": "World",
        "ingredients": ["3 eggs", "1/4 cup milk"],
        "instructions": ["Step 1", "Step 2"],
        "approximate_time": "10-15 minutes"
    }

    response = client.post("/recipes", json=recipe_data)

    assert response.status_code == 500
    assert response.json() == {"detail": "Some error"}

# ******************************************************************
# PUT /recipes  UPDATE


def test_update_recipe():

    updated_recipe_data = {
        "name": "Spaghetti Bolognese",
        "category": "Italian",
        "ingredients": ["pasta", "sauce", "meat"],
        "instructions": ["Step 1", "Step 2", "Step 3"],
        "approximate_time": "45 minutes"
    }
    existing_recipe = {
        "name": "Spaghetti",
        "category": "Italian",
        "ingredients": ["pasta", "sauce", "meat"],
        "instructions": ["Step 1", "Step 2", "Step 3"],
        "approximate_time": "40 minutes"
    }
    existing_recipe = Recipe(**updated_recipe_data)
    existing_recipe_id = recipes_collection.insert_one(
        jsonable_encoder(existing_recipe)).inserted_id

    response = client.put(
        f"/recipes/{existing_recipe_id}", json=updated_recipe_data)

    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Recipe with id:{existing_recipe_id} update successfully"
    assert recipes_collection.find_one({"_id": existing_recipe_id})[
        "name"] == "Spaghetti Bolognese"
    recipes_collection.delete_one({"_id": existing_recipe_id})


def test_update_recipe_not_found():
    non_existing_recipe_id = "non_existing_recipe_id"
    updated_recipe_data = {
        "name": "Spaghetti Bolognese",
        "category": "Italian",
        "ingredients": ["pasta", "sauce", "meat"],
        "instructions": ["Step 1", "Step 2", "Step 3"],
        "approximate_time": "45 minutes"
    }

    response = client.put(
        f"/recipes/{non_existing_recipe_id}", json=updated_recipe_data)

    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}


# ****************************************************************
# /recepis/{id}  DELETE

def test_delete_recipe():

    existing_recipe_data = {
        "name": "Spaghetti",
        "category": "Italian",
        "ingredients": ["pasta", "sauce", "meat"],
        "instructions": ["Step 1", "Step 2", "Step 3"],
        "approximate_time": "40 minutes"
    }
    existing_recipe = Recipe(**existing_recipe_data)
    existing_recipe_id = recipes_collection.insert_one(
        jsonable_encoder(existing_recipe)).inserted_id

    response = client.delete(f"/recipes/{existing_recipe_id}")
    assert response.status_code == 200
    assert response.json()[
        "message"] == f"Recipe with id:{existing_recipe_id} deleted successfully"


def test_delete_recipe_not_found():
    response = client.delete("/recipes/non_existing_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"
