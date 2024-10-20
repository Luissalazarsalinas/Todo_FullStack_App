import os
from pathlib import Path
from fastapi import FastAPI, status, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import BASE
from .routers import todo, users, auth
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# Base Path
BASE_PATH = Path(__file__).resolve(strict=True).parent

# Create models
BASE.metadata.create_all(bind=engine)

# Create api instance
app = FastAPI(
    title="TODO APP",
    version='0.001'
)

#add static folder 
app.mount('/static', StaticFiles(directory=f"{BASE_PATH}{os.sep}static"), name="static")


# TEST TEMPLATE WITH A ENDPOINT 
@app.get('/')
async def test(request:Request):
    return RedirectResponse(url="/v1/todo-page", status_code=status.HTTP_302_FOUND)


# healthy endpoint
@app.get('/healthy', status_code=status.HTTP_200_OK)
async def health_check():
    return{
        "status":"Healthy"
    }


# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# add routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todo.router)