import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


@pytest.fixture
def access_token():
    # Replace with a valid access token for testing
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTk5MWVjZTgtNGM1Mi00YjcxLThmN2UtZWJjYjk1Y2JjMWM0IiwidG9rZW5fdHlwZSI6ImJlYXJlciIsImV4cCI6MTY4NjMzNjk5OX0.8M6gQbIxakYt6jSVDpFHH--S844q0PPP1QVtZ0IppZU"


@pytest.fixture
def expected_user_data():
    # Replace with a valid user data for testing
    return {
        "_id": "1991ece8-4c52-4b71-8f7e-ebcb95cbc1c4",
        "user_name": "bangelev",
        "name": "Blagoja Angelevski",
        "email": None,
        "avatar_url": "https://avatars.githubusercontent.com/u/60876733?v=4",
        "role": "user",
        "created_at": "2023-06-02T19:51:44.195139"
    }


def test_load_signup_user_with_valid_token(access_token, expected_user_data):
    response = client.get(
        "/users/", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == {"user": expected_user_data, "success": True}


def test_load_signup_user_without_token():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == None


def test_load_signup_user_with_invalid_token():
    response = client.get("/users/", cookies={"access_token": "invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}


def test_logout_with_valid_token(access_token):
    response = client.post(
        "/users/logout", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}


def test_logout_without_token():
    response = client.post("/users/logout")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token, NOT token sent"}
