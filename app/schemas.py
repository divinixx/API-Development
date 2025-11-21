import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
    
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime.datetime
    class Config:
        from_attributes = True

class Post(PostBase):   #Repsone Model 
    id: int 
    created_at: datetime.datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: str
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore
