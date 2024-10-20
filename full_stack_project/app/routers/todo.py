from ..database import get_db
from ..models import User, Todo
from ..schemas import CreateTodo, TodosOut, Todos
from ..oauth2 import current_user
from .auth import path_templates
from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import status, HTTPException, Depends, Path, APIRouter, Request

# Instance
router = APIRouter(
    prefix='/v1',
    tags=['TODOS']
)


# create template 
temp = Jinja2Templates(directory=path_templates)

# redirect results to the login page
def redirect_to_login():

    redirect_response = RedirectResponse(url="/v1/login-page", status_code=status.HTTP_302_FOUND)
    #delete cookeis
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###
@router.get("/todo-page", response_class=HTMLResponse)
async def todo_page(request:Request, db:Annotated[Session, Depends(get_db)]):

    try:

        # get current user with the token from wed cookies
        user = current_user(request.cookies.get('access_token'), db)

        if user is None:
            return redirect_to_login()
        
        # Get todos
        todos = db.query(Todo).filter(Todos.owner_id == user.id).all()

        return temp.TemplateResponse(
            request=request,
            name="todo.html",
            context={
                "todos": todos,
                "user": user
            }
        )
    except:
        return redirect_to_login()

@router.get("/add-todo-page", response_class=HTMLResponse)
async def add_todo_page(request:Request, db:Annotated[Session, Depends(get_db)]):

    try:

        # get current user with the token from wed cookies
        user = current_user(request.cookies.get('access_token'), db)

        if user is None:
            return redirect_to_login()


        return temp.TemplateResponse(
            request=request,
            name="add-todo.html",
            context={
                "user": user
            }
        )
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}", response_class=HTMLResponse)
async def edit_todo_page(request:Request, db:Annotated[Session, Depends(get_db)], todo_id:int= Path(gt=0)):

    try:

        # get current user with the token from wed cookies
        user = current_user(request.cookies.get('access_token'), db)

        # Query
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if user is None:
            return redirect_to_login()


        return temp.TemplateResponse(
            request=request,
            name="add-todo.html",
            context={
                "todo": todo,
                "user": user
            }
        )
    except:
        return redirect_to_login()


### Endpoints ###

# Get all todos
@router.get('/todos', status_code=status.HTTP_200_OK, response_model=List[TodosOut])
async def get_all_todos(user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)]):

    # VERIFY USEr
    if not user:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action."
        )
    
    # query
    result = db.query(Todo).all()

    return result

# Get todo by ID
@router.get('/todos/{id}', status_code=status.HTTP_200_OK, response_model=TodosOut)
async def get_one_todo(user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)], id:int = Path(gt=0)):
    
    # query
    response = db.query(Todo).filter(Todo.id == id)\
        .filter(Todo.owner_id == user.id).first()
    
    if response is not None:
        return response
    else:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"The element with id:{id} is not found."
        )

# Create a todo
@router.post('/todos/create_todo', status_code=status.HTTP_201_CREATED, response_model=TodosOut)
async def create_todo(todo:CreateTodo, user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)]):

    # create an instance of todos 
    new_todo = Todo(owner_id = user.id, **todo.model_dump())

    # add new todo to database
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    # return new_todo




# Update todo
@router.put('/todos/update_todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)],
                update_todo:CreateTodo, id:int = Path(gt=0)):
    
    # Query 
    query = db.query(Todo).filter(Todo.id == id)

    # get results
    response = query.first()

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The element with id:{id} is not found."
        )
    
    # validate user 
    if response.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to perform requested action."
        )
    
    # update commit
    query.update(update_todo.model_dump(), synchronize_session=False)

    db.commit()

# delete 

@router.delete('/todos/delete_todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:Annotated[User, Depends(current_user)], db:Annotated[Session, Depends(get_db)],
                      id:int = Path(gt=0)):
    
    # Query 
    query = db.query(Todo).filter(Todo.id == id)

    # get results
    response = query.first()

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The element with id:{id} is not found."
        )
    
    # validate user 
    if response.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Not authorized to perform requested action."
        )
    
    # update commit
    query.delete(synchronize_session=False)

    db.commit()

