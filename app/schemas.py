from pydantic import BaseModel
from datetime import datetime

# request body pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#response pydantic model
class PostResponse(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True