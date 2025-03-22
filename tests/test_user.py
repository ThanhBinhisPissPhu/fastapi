import pytest
from app import schemas
from app.config import settings
from jose import jwt


def test_create_user(client):
    response = client.post("/users/", json={"email": "new@gmail.com", "password": "new"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "new@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, settings.ALGORITHM)
    id = payload.get("user_id")

    assert response.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@gmail.com", "new", 403),
    ("new@gmail.com", "wrong", 403),
    ("wrong@gmail.com", "wrong", 403),
    ("", "new", 422),
    (None, "new", 422),
    ("new@gmail.com", "", 422),
    ("new@gmail.com", None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})

    assert response.status_code == status_code 
    assert response.json().get("detail") == "Invalid credentials" if status_code == 403 else "Username and password are required"