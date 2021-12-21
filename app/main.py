from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from . import models
from .database import engine
from .routers import posts, users, auth, votes

#create our posts table if its not present
models.Base.metadata.create_all(bind=engine)

# aplication instance
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#path operations - synonymous to routes
#routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

#root 
@app.get("/")
async def root():
    message = "Hello am learning FastAPI!!"
    return{"message":f"{message}"}