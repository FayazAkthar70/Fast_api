from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime,timedelta
from sqlalchemy.orm.session import Session
from starlette import status
from app import database, models
from . import schema
from fastapi.security import OAuth2PasswordBearer
from .config import setting
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credentials_exceptions):
    
    try:
        decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM] )
        id : str = decoded_jwt.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = schema.TokenData(id= id)
    except JWTError:
        raise credentials_exceptions
    return token_data

def get_current_user (token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate" : "Bearer"})
    token = verify_access_token(token,credential_exception)
    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return current_user