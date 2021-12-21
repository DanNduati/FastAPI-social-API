from fastapi import status,HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import utils,schemas,models
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# post endpoint to create users
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_user(user:schemas.UserCreate,db : Session = Depends(get_db)):
    """
    Create/Register a user
    """
    if not (db.query(models.User).filter(models.User.email == user.email).first()):
        hashed_pwd = utils.hash(user.password)
        user.password = hashed_pwd
        new_user = models.User(**user.dict())
        db.add(new_user)    
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already exists please login") 


# get endpoint for user details
@router.get("/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id: int,db: Session = Depends(get_db)):
    """
    Get user details
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=F"User with id {user_id} not found")
    return user