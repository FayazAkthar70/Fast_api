from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr

class UserBase(BaseModel):
    email : EmailStr
    password : str

class Create_User(UserBase):
    pass

class Response_User(BaseModel):
    id : int
    email : EmailStr
    class Config:
        orm_mode = True   
        
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    class Config:
        orm_mode = True
class BasePost(BaseModel):
    title: str
    content: str
    published : bool = True
        
class Create_Post(BasePost):
    pass

class Response_Post(BasePost):
    id : int
    created_at: datetime
    owner_id : int
    owner : Response_User
    class Config:
        orm_mode = True
 
class Post_Out(BaseModel):
    Post : Response_Post
    votes : int
    class Config:
        orm_mode = True
         
class Token(BaseModel):
    jwt_token : str
    token_type : str
    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : Optional[str] = None
    
class Vote(BaseModel):
    post_id : int
    dir : bool
    