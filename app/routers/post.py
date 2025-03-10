from typing import Optional

from httpx import post
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=list[schemas.PostWithVote])
async def get_posts(db: Session = Depends(get_db), 
                    current_user: models.Users = Depends(oauth2.get_current_user),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts_with_votes = db.query(models.Posts, func.count(models.Votes.post_id) \
                                .label("votes")).outerjoin(models.Votes) \
                                .group_by(models.Posts.id) \
                                .filter(models.Posts.title.contains(search)) \
                                .limit(limit) \
                                .offset(skip) \
                                .all()

    return posts_with_votes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    """
    Not doing this because there might be a SQL injection attack
    cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ('{post.title}', '{post.content}', {post.published}) RETURNING *")
    """
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Posts(title=post.title, content=post.content, published=post.published)
    print(current_user.id, current_user.email)
    new_post = models.Posts(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostWithVote)
async def get_post(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # post = cursor.fetchone()
    print(current_user.id)
    posts_with_votes = db.query(models.Posts, func.count(models.Votes.post_id) \
                                .label("votes")).outerjoin(models.Votes) \
                                .group_by(models.Posts.id) \
                                .filter(models.Posts.id == id) \
                                .first()
    if posts_with_votes is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    return posts_with_votes



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    deleted_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this post")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    """here we return a response with status code 204 because conventionally when you delete something, 
    you should not return any data, you just return a status code 204. 
    If you return anything, FastAPI will raise an error: h11._util.LocalProtocolError: Too much data for declared Content-Length"""
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    updated_post_query = db.query(models.Posts).filter(models.Posts.id == id)
    updated_post = updated_post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this post")
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post_query.first()