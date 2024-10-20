from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

# user schema

class UserInput(BaseModel):

    email: EmailStr
    user_name : str
    first_name : str 
    second_name : str
    password : str
    role: str
    phone_number: str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    user_name: str
    role: str

    class Config:
        orm_mode = True

# Base to create a Todo
class BaseTodo(BaseModel):
    title:str
    description:str
    priority:int
    # complete:bool

# model to create a todos
class CreateTodo(BaseTodo):
    pass

# Response when a todo was created
class Todos(BaseModel):

    title:str
    description:str
    priority:int
    complete:bool
    create_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class TodosOut(Todos):
    pass
    
    # todos: Todos
    
    # class Config:
    #     orm_mode = True
         

# JWT token schema
class Token(BaseModel):
    access_token:str
    token_type:str

# token data verify
class TokenData(BaseModel):
    id: int
    role: str

# change password schema
class ChangePassword(BaseModel):
    password:str
    new_password:str

# change password schema
class ChangePhoneNum(BaseModel):
    phone_number:str
    new_phone_num:str

