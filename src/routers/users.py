# routers/users.py
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
import schema
import models
from typing import List
from database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=['Users'])

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_users(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users', response_model=List[schema.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.get('/users/{id}', response_model=schema.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return user

@router.put("/users/{id}", response_model=schema.User)
def update_user(id: int, user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} does not exist")
    db_user.email = user.email
    db_user.password = pwd_context.hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user
