from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import false,func, null
from sqlalchemy.sql.schema import ForeignKey
from .database import Base

#define orm models
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    user_id = Column(Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)

    def __repr__(self) -> str:
        return F"Post(s): {self.id} {self.title} {self.content} {self.published}"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())