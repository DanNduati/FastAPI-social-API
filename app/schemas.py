from typing import Optional
from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint

#posts schemas
# request body pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#users schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserpostResponse(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

#post response pydantic model
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserpostResponse
    class Config:
        # Pydantic's orm_mode will tell the pydantic model to 
        # read the data even if it is not a dict but an ORM model 
        # or any other arbitrary object with attributes
        orm_mode = True

class PostOut(BaseModel):
    Post : PostResponse
    votes: int
    class Config:
        orm_mode = True

#user auth schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#access token schema
class Token(BaseModel):
    access_token:str
    token_type:str

#access token payload schema
class TokenData(BaseModel):
    id:Optional[str] = None

#votes schema
class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)#bool