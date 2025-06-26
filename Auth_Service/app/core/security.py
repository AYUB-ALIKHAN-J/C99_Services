from passlib.context import CryptContext
from jose import JWTError ,jwt
from datetime import datetime , timedelta
from app.core.config import Settings


pwd_context = CryptContext(schemes=["bcrypt"],deprecated ="auto")

def verify_password(plain ,hashed):
    return pwd_context.verify(plain,hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data:dict,expires_delta:timedelta=None):
    to_encode = data.copy()
    expires = datetime.utcnow() + (expires_delta or timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expires})
    encoded_jwt = jwt.encode(to_encode , Settings.SECRET_KEY,algorithm=Settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str):
    try:
        payload = jwt.decode(token , Settings.SECRET_KEY,algorithms=[Settings.ALGORITHM])
        return payload
    except JWTError:
        return None