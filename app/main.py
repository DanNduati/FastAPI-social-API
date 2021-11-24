from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
import app.config as my_config
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# aplication instance
app = FastAPI()

# request body pydantic model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

#connect to postgress server instance and database
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

#path operations - synonymous to routes
#root 
@app.get("/")
async def root():
    message = "Hello am learning FastAPI!!"
    return{"message":f"{message}"}

# get endpoint to get all posts
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    #print(posts)
    return {"data":posts}

# post endpoint to add a post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

# get endpoint to get the latest post
@app.get("/posts/latest")
def get_latest():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    posts = cursor.fetchall()
    post = posts[len(posts)-1]
    return {"data":post}


# get endpoint to get a post by id as a path parameter
@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    cursor.execute(F"""SELECT * FROM posts WHERE id= {str(post_id)}""")
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} was not found")
    return {"data":test_post}

# post end point to delete a post
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int):
    cursor.execute(F"""SELECT * FROM posts WHERE id={str(post_id)}""")
    post = cursor.fetchone()
    if not post:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    else:
        #delete post
        cursor.execute(F"""DELETE FROM posts WHERE id={str(post_id)}""")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

# put endpoint to update a post
@app.put("/posts/{post_id}")
def update_post(post_id:int,post:Post):
    cursor.execute(F"""SELECT * FROM posts WHERE id={str(post_id)}""")
    update_post = cursor.fetchone()
    if not update_post:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    else:
        cursor.execute(F"""UPDATE posts SET title={post.title}, content={post.content}, published={post.published} WHERE id={str(post_id)} RETURNING *""")
        updated_post = cursor.fetchone()
        return{"data":update_post,"message":f"Successfully updated post wihth id {post_id}"}