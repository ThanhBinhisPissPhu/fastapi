import pytest
from app import models

@pytest.fixture
def test_vote(test_posts, session, test_user):
    vote = models.Votes(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(vote)
    session.commit()
    return vote


def test_vote_one_post(authorized_client, test_posts):
    response = authorized_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 201


def test_vote_twice_one_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 409


def test_vote_post_non_exist(authorized_client, test_posts):
    response = authorized_client.post("/votes/", json={"post_id": 1000, "dir": 1})
    assert response.status_code == 404


def test_vote_unauthorized(client, test_posts):
    response = client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 401


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 0})
    assert response.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):
    response = authorized_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 0})
    assert response.status_code == 404
