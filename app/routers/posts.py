import re
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.util import outerjoin
from sqlalchemy.sql.functions import func
from .. import models, schema, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schema.Post_Out])
def get_all_posts(db: Session = Depends(get_db), limit : int = 30, offset : int = 0, search : Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post)
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    
    return result

@router.get("/{id}",response_model=schema.Response_Post)
def get_post(id : int, response : Response, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    # cursor.execute(""" select * from posts where id = %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message" : f"post with id = {id} not available"})
    return post
            


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Response_Post)
def create_post(post : schema.Create_Post, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user) ):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # post = cursor.fetchone()
    # conn.commit()
    print(current_user)
    post = post.dict()
    post['owner_id'] = current_user.id
    new_post = models.Post(**post) # same as models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    # del_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message" : f"post with {id} not available"})
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message" : "Not authorised to perform action"})
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.Response_Post)
def update_post(post : schema.Create_Post, id : int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message" : f"post with {id} not available"})
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message" : "Not authorised to perform action"})
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()