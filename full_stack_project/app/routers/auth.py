import os
from pathlib import Path
from ..database import get_db
from ..models import User
from ..schemas import Token
from ..utils.crypt import verify
from ..oauth2 import create_token
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

BASE_PATH = Path(__file__).resolve(strict=True).parent.parent

# instance of the endpoins router
router = APIRouter(
    prefix='/v1',
    tags=['LOGIN']
)

path_templates = f"{BASE_PATH}{os.sep}templates"

# Create template to render html
templates = Jinja2Templates(directory=path_templates)

# Pages
@router.get('/login-page')
def login_page(request:Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )

@router.get("/register-page")
def register_user(request:Request):
     return templates.TemplateResponse(
          request=request, name="register.html"
     )

### ENDPOINT
# Create post endpoint to login user
@router.post('/login', status_code=status.HTTP_201_CREATED, response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Annotated[Session, Depends(get_db)]):

    # Validate if the user is logging with user name or email
    if '@' not in form_data.username:
        user = db.query(User).filter(User.user_name == form_data.username).first()

    else:
        user = db.query(User).filter(User.email == form_data.username).first()

    # Validate that user exist 
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials'
        )
    
    # Validate password
    if not verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid credentials'
        )
    
    # Create user token
    token = create_token({"id":user.id, "role":user.role})

    return {
        "access_token":token,
        "token_type":"bearer"
    }