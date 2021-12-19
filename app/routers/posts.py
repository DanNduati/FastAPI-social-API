from fastapi import Response,status,HTTPException, APIRouter
from fastapi.params import  Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import func
from ..database import get_db
from .. import models,schemas,oauth2

#create a router object
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# get endpoint to get all posts
#@router.get("/",response_model=List[schemas.PostResponse])
@router.get("/",response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),current_user: dict = Depends(oauth2.get_current_user),limit: Optional[int]=10, skip: Optional[int]=0,search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results

# post endpoint to create a post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #add the user_id from the token 
    new_post = models.Post(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get endpoint to get the latest post
@router.get("/latest",response_model=schemas.PostOut)
async def get_latest(db: Session = Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    latest_post = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).order_by(models.Post.id.desc()).first()
    return latest_post


# get endpoint to get a post by id
@router.get("/{post_id}",response_model=schemas.PostOut)
async def get_post(post_id: int, response: Response,db: Session = Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id= {str(post_id)}""")
    #test_post = cursor.fetchone()
    #test_post = db.query(models.Post).get(post_id)
    test_post = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} was not found")
    return test_post

# post end point to delete a post
@router.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int,db: Session=Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id={str(post_id)}""")
    #post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    #check to see if the post belongs to the current user before deletion
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action on this post")
    #delete post
    #cursor.execute(F"""DELETE FROM posts WHERE id={str(post_id)}""")
    #conn.commit()
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# put endpoint to update a post
@router.put("/{post_id}",response_model=schemas.PostResponse)
async def update_post(post_id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user: dict = Depends(oauth2.get_current_user)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id={str(post_id)}""")
    #update_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id==post_id)
    u_post = post_query.first()
    if not u_post:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    #check to see if the post belongs to the current user before update
    if u_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action on this post")
    #cursor.execute("""UPDATE posts SET title= %s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(post_id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    updated_post = post_query.first()
    return updated_post
