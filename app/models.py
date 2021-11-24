from datetime import timezone
from sqlalchemy import Column, Boolean, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.sql.expression import false,func
from .database import Base

#define orm models
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())

    def __repr__(self) -> str:
        return F"Post(s): {self.id} {self.title} {self.content} {self.published}"