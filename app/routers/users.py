from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Response_User)
def create_user(user : schema.Create_User, db: Session = Depends(get_db) ):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict()) # same as models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schema.Response_User)
def get_users(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"user with id : {id} not found")
    return user