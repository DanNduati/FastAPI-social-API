from base64 import encode
from jose import JWSError,jwt
from datetime import datetime,timedelta

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