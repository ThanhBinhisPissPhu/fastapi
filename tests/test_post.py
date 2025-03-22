import pytest
from app import schemas

#---------------------Get Post---------------------
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    # print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostWithVote(**res.json())
    # print(post)
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.title == test_posts[0].title
    assert post.Posts.content == test_posts[0].content
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_posts_non_existent(authorized_client, test_posts):
    res = authorized_client.get("/posts/100")
    assert res.status_code == 404


#---------------------Create Post---------------------
@pytest.mark.parametrize("title, content, published, status_code", [
    ("Post 4", "Content 4", True, 201),
    ("", "Content 5", False, 201),
    ("Post 6", "", True, 201),
    ("", "", True, 201),
])
def test_create_post(authorized_client, test_user, title, content, published, status_code):
    post_data = {"title": title, "content": content, "published": published}
    res = authorized_client.post("/posts/", json=post_data)
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == status_code
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user):
    post_data = {"title": "Post 7", "content": "Content 7"}
    res = authorized_client.post("/posts/", json=post_data)
    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "Post 7"
    assert created_post.content == "Content 7"
    assert created_post.owner_id == test_user["id"]
    assert created_post.published == True
    

def test_unauthorized_create_post(client):
    post_data = {"title": "Post 7", "content": "Content 7", "published": True}
    res = client.post("/posts/", json=post_data)
    assert res.status_code == 401


#---------------------Delete Post---------------------
def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete("/posts/100")
    assert res.status_code == 404


def test_unauthorized_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


#---------------------Update Post---------------------
def test_update_post(authorized_client, test_posts):
    post_data = {"title": "Post 1 Updated", "content": "Content 1 Updated"}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == post_data["title"]
    assert updated_post.content == post_data["content"]


def test_update_post_non_exist(authorized_client):
    post_data = {"title": "Post 1 Updated", "content": "Content 1 Updated"}
    res = authorized_client.put("/posts/100", json=post_data)
    assert res.status_code == 404


def test_unauthorized_update_post(client, test_posts):
    post_data = {"title": "Post 1 Updated", "content": "Content 1 Updated"}
    res = client.put(f"/posts/{test_posts[0].id}", json=post_data)
    assert res.status_code == 401


def test_update_other_user_post(authorized_client, test_posts):
    post_data = {"title": "Post 3 Updated", "content": "Content 3 Updated"}
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post_data)
    assert res.status_code == 403