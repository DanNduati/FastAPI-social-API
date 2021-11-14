from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel

# aplication instance
app = FastAPI()

# request json body pydantic model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#dummy in memory posts
posts = [{
    "title": "title of post 1",
    "content": "content of post 1",
    "id": 1,
    "published": True,
    "rating": 8
    },
    {
    "title": "title of post 2",
    "content": "content of post 2",
    "id": 2,
    "published": True,
    "rating": 6.5 
    }
]

def find_post(id):
    for i,post in enumerate(posts):
        if post["id"] == id:
            return post

#path operations - synonymous to routes

#root 
@app.get("/")
def root():
    message = "Hello am learning FastAPI!!"
    return{"message":f"{message}"}

# get endpoint to get all posts
@app.get("/posts")
def get_posts():
    return {"data":f"{posts}"}

# post endpoint to add a post
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post): 
    last_id = int(posts[-1]['id'])
    #print(last_id)
    payload = post.dict()
    payload["id"] = last_id+1
    #print(payload)
    posts.append(payload)
    return {"data":f"{payload}"}

# get endpoint to get the latest post
@app.get("/posts/latest")
def get_latest():
    post = posts[len(posts)-1]
    return {"data":f"{post}"}


# get endpoint to get a post by id as a path parameter
@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id: {post_id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": }
    return {"data":post}

# post end point to delete a post
@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int):
    post = find_post(post_id)
    if not post:
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    else:
        # delete the post
        posts.pop(post_id-1)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

# put endpoint to update a post
@app.put("/posts/{post_id}")
def update_post(post_id:int,post:Post):
    if not find_post(post_id):
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} was not found"))
    else:
        #update the post
        for key,value in post.dict().items():
            #print(f"{key} : {value}")
            posts[post_id-1][key] = value
        return{"data":f"{posts[post_id-1]}","message":f"Successfully updated post wihth id {post_id}"}
