import time
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body, Depends
from typing import Optional, List
from pydantic import BaseModel
import app.config as my_config
#import psycopg2
#from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models,schemas
from .database import SessionLocal, engine, get_db

#create our posts table if its not present
models.Base.metadata.create_all(bind=engine)

# aplication instance
app = FastAPI()

'''
# connect to postgress server instance and database with the psycopg2 adapter
while True:
    try:
        conn = psycopg2.connect(host=my_config.database_host,dbname=my_config.database_name,user=my_config.database_user,password=my_config.database_password,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to database successful!")
        break
    except Exception as e:
        print("Unable to connect to database!")
        print("Error: ",e)
        time.sleep(1)
'''

#path operations - synonymous to routes
#root 
@app.get("/")
async def root():
    message = "Hello am learning FastAPI!!"
    return{"message":f"{message}"}

# get endpoint to get all posts
@app.get("/posts",response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# post endpoint to create a post
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
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
@app.get("/posts/latest",response_model=schemas.PostResponse)
async def get_latest(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post


# get endpoint to get a post by id as a path parameter
@app.get("/posts/{post_id}",response_model=schemas.PostResponse)
async def get_post(post_id: int, response: Response,db: Session = Depends(get_db)):
    #cursor.execute(F"""SELECT * FROM posts WHERE id= {str(post_id)}""")
    #test_post = cursor.fetchone()
    #test_post = db.query(models.Post).get(post_id)
    test_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} was not found")
    return test_post

# post end point to delete a post
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
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
@app.put("/posts/{post_id}",response_model=schemas.PostResponse)
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