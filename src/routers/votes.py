from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, oauth2, schema

router = APIRouter(prefix='/vote', tags=["Vote"])

@router.post('/', status_code= status.HTTP_201_CREATED)
def like_post(vote : schema.Vote, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # Check to see whether the post exist or not 
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")

    # Check to see if the post has been liked by the user or not :
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    # If a user want to like the post , first check that if the user has already liked or not:
    if vote.dir == 1 : 
        if found_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= 
                                f"user {current_user.id} has already liked the post {vote.post_id}")
        new_vote = models.Votes(user_id =  current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added a vote"}
    
    # If the vote_dir == 0 that means we need to delete the vote
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
        

        
