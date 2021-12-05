from fastapi import Response,status,HTTPException, APIRouter
from fastapi.params import  Depends
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas

#create a router object
router = APIRouter()

# get endpoint to get all posts
@router.get("/posts",response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# post endpoint to create a post
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# get endpoint to get the latest post
@router.get("/posts/latest",response_model=schemas.PostResponse)
async def get_latest(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post


# get endpoint to get a post by id as a path parameter
@router.get("/posts/{post_id}",response_model=schemas.PostResponse)
async def get_post(post_id: int, response: Response,db: Session = Depends(get_db)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id= {str(post_id)}""")
    #test_post = cursor.fetchone()
    #test_post = db.query(models.Post).get(post_id)
    test_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} was not found")
    return test_post

# post end point to delete a post
@router.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id:int,db: Session=Depends(get_db)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id={str(post_id)}""")
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() == None:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    else:
        #delete post
        #cursor.execute(F"""DELETE FROM posts WHERE id={str(post_id)}""")
        #conn.commit()
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

# put endpoint to update a post
@router.put("/posts/{post_id}",response_model=schemas.PostResponse)
async def update_post(post_id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id={str(post_id)}""")
    #update_post = cursor.fetchone()
    update_post = db.query(models.Post).filter(models.Post.id==post_id)
    if not update_post.first():
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    else:
        #cursor.execute("""UPDATE posts SET title= %s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(post_id)))
        #updated_post = cursor.fetchone()
        #conn.commit()
        update_post.update(post.dict(),synchronize_session=False)
        db.commit()
        updated_post = update_post.first()
        return updated_post
