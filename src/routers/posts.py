# routers/posts.py
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
import schema
import models, oauth2
from database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user),
               limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # print(current_user.email, '\n', type(current_user))
    # print('limit : ', limit)

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get('/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Item {id} not found")
    return post

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    # check if the post user is deleting is a post by the same user, if not then raise error
    if post.user_id != current_user.id : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not Authorized to perform requested action")
    db.delete(post)
    db.commit()
    return None

@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == id).first()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    # check if the post user is deleting is a post by the same user, if not then raise error
    if db_post.user_id != current_user.id : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not Authorized to perform requested action")
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    db.commit()
    db.refresh(db_post)
    return db_post
