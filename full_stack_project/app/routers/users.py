from ..database import get_db
from ..oauth2 import current_user
from ..models import User
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated, List
from ..schemas import UserInput, UserOut, ChangePassword,ChangePhoneNum
from ..utils.crypt import hash, verify
from fastapi import APIRouter, status, Depends, HTTPException, Path, Request


# Create endpoint router
router = APIRouter(
    prefix='/v1',
    tags=['USERS']
)

# ENDPOINTS
# GET ALL USER
@router.get('/users/get_users', status_code=status.HTTP_200_OK, response_model=List[UserOut])
async def get_all_users(user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)]):

    # validations 
    if (not user) and (user.role != 'admin'):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = 'Not authorized to perform requested action.'
        )
    return db.query(User).all()

# get one user
@router.get('/users/get_user/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_one_user(user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)], id:int=Path(gt=0)):

    # query 
    query = db.query(User).filter(User.id == id)

    response = query.first()

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"User with id:{id}, Not found."
        )
    
    # validate current user and role
    if (not user) and (user.role != 'admin'):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = 'Not authorized to perform requested action.'
        )
    
    return response


@router.post('/users/create_user', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(db:Annotated[Session, Depends(get_db)], new_user:UserInput):

    print(new_user.model_dump())
    # instance 
    _new_user_password = hash(new_user.password)
    new_user.password = _new_user_password

    user_data = User(**new_user.model_dump())


    # add new user to db
    db.add(user_data)
    db.commit()
    db.refresh(user_data)

    return user_data



# change password 
@router.patch('/users/update_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:Annotated[User, Depends(current_user)],
                          db:Annotated[Session, Depends(get_db)],
                          update_password: ChangePassword):
     # query 
     query = db.query(User).filter(User.id == user.id)
     
     get_user = query.first()

     if get_user is None:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail='User not found'
          )
    
     # verify password
     if not verify(update_password.password, get_user.password):
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail='Not authorized to perform requested action.'
          )
     
     # update password
     get_user.password = hash(update_password.new_password)

     db.add(get_user)

     db.commit()

# change password 
@router.patch('/users/update_phone_number', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:Annotated[User, Depends(current_user)],
                              db:Annotated[Session, Depends(get_db)],
                              update_phone_num: ChangePhoneNum):
     
     # validate user
     if user is None:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail='Not authorized to perform requested action.',
          )
     
     # query 
     query = db.query(User).filter(User.id == user.id)
     
     get_user = query.first()

     
     # verify password
     if get_user.phone_number != update_phone_num.phone_number:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail='Not authorized to perform requested action.'
          )
     
     # update password
     get_user.phone_number = update_phone_num.new_phone_num

     db.add(get_user)

     db.commit()
     




