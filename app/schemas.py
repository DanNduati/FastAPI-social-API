from pydantic import BaseModel

# request body pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass