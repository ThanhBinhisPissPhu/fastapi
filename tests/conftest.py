from venv import create
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    # keep the table so that we can debug any error
    # you can choose alemic to create and drop the table. but here we use sqlalchemy to create and drop the table
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        


## When you use a fixture with a yield, the code before the yield is executed before the test (if you have any setup there), 
## and the code after the yield runs after the test completes.
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    

@pytest.fixture
def test_user(client):
    user_data = {"email": "new@gmail.com", "password": "new"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def different_test_user(client):
    user_data = {"email": "new0@gmail.com", "password": "new0"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, different_test_user, session):
    post_data = [
        {"title": "Post 1", "content": "Content 1", "owner_id": test_user["id"]},
        {"title": "Post 2", "content": "Content 2", "owner_id": test_user["id"]},
        {"title": "Post 3", "content": "Content 3", "owner_id": test_user["id"]},
        {"title": "Post 3", "content": "Content 3", "owner_id": different_test_user["id"]},
    ]

    def create_post_model(post):
        return models.Posts(**post)
    
    posts = [create_post_model(post) for post in post_data]
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Posts).all()
    return posts