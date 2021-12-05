from fastapi import status,HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import session
from .. import utils,schemas,models
from ..database import get_db

router = APIRouter()

# post endpoint to create users
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_user(user:schemas.UserCreate,db : session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# get endpoint for user details
@router.get("/users/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id: int,db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=F"User with id {user_id} not found")
    return user