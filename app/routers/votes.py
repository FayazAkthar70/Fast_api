from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from app import database, oauth2, schema, models

router = APIRouter(
    prefix="/votes",
    tags=['voting']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_present = vote_query.first()
    if vote.dir:
        if vote_present : 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return "message: {voted successfully}"
    else : 
        if not vote_present :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote by user {current_user.id} for post {vote.post_id} not present")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return "message : {delete vote successful}"