from fastapi import APIRouter,status,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,oauth2

router = APIRouter(
    tags=["auth"]
)

@router.post("/login")
async def login(user_credentials:schemas.UserLogin, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid user credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid user credentials")
    #create the jwt -> payload --> user_id
    access_token = oauth2.create_access_token({"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}