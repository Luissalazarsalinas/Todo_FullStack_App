from .database import get_db
from .schemas import TokenData
from .models import User
from .config import settings
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError

# Variable to stored the token when the user is logged 
bearer_token = OAuth2PasswordBearer(tokenUrl='v1/login')

# Global variables to create the jwt
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def create_token(data:dict) -> str:

    # expire token time
    expire_token = datetime.utcnow() + timedelta(minutes=settings.access_token_expire)

    # inclue toke expire time into the data dict
    data.update({"exp":expire_token})

    # create token
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token:str, credential_exception:HTTPException):

    try:
        
        # Get pyload
        pyload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # GET ID AND USER ROLE
        user_id = pyload.get("id")
       
        user_role = pyload.get("role")
    

        if user_id is None:
            raise credential_exception
        
        # Validate token data
        token_data = TokenData(id=user_id, role=user_role)
    except JWTError:
        raise credential_exception
    
    return token_data

def current_user(token:Annotated[str, Depends(bearer_token)], db: Annotated[Session, Depends(get_db)]):

    # Create credential exception
    credential_excep = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validated credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    # Verify token and get user data
    user_data = verify_token(token, credential_excep)

    # get current user with the token data
    user = db.query(User).filter(User.id == user_data.id, User.role == user_data.role).first()

    return user
