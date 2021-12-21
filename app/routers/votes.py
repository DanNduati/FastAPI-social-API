from fastapi import status,HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from .. import schemas,models,oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote,db: Session = Depends(get_db),current_user:dict = Depends(oauth2.get_current_user)):
    """
    Vote for post by its id, vote direction: 1 -> upvote/like 0-> delete upvote/like
    """
    #check whether the post exists
    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=F"Post with id of {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()
    if(vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= F"User {current_user.id} has already voted on the post: {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message":"vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"vote deleted successfully"}