from base64 import encode
from fastapi import HTTPException,status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime,timedelta
from jose.exceptions import JWTError
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#secret key generated by ```openssl rand -hex 32```
SECRET_KEY = "f16b7835d65785cf0afe34b314742cfb4baa347062548f3fc537f6dcac73422c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    #create expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        #extract payload data
        id:str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credentials_exception)