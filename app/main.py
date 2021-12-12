from fastapi import FastAPI

from app.routers import auth
from . import models
from .database import SessionLocal, engine
from .routers import posts, users, auth

#create our posts table if its not present
models.Base.metadata.create_all(bind=engine)

# aplication instance
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
#path operations - synonymous to routes
#root 
@app.get("/")
async def root():
    message = "Hello am learning FastAPI!!"
    return{"message":f"{message}"}