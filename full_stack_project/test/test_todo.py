from app.main import app
from fastapi import status
from app.database import get_db
from app.oauth2 import current_user
from app.models import Todo
from .utils import *

# override dependencies - 
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[current_user] = override_current_user

# Create the test
# create test function to test all todos
def test_read_all_authenticated(test_todo, test_user):
    response = client.get('/v1/todos')
    # test the status code
    assert response.status_code == status.HTTP_200_OK
    # TODO: MODIFY THIS ADD USER DATA
    # test endpoint result 
    assert response.json()[0]["title"] == "Learn to code in C#" 
    assert response.json()[0]["description"] == "Need to learn everyday!" 
    assert response.json()[0]["priority"] == 5
    assert response.json()[0]["complete"] == False 
    assert response.json()[0]["owner_id"] == 1
    assert response.json()[0]["owner"]["email"] ==  "test_user@gmail.com"
    assert response.json()[0]["owner"]["user_name"] == "test user"
    assert response.json()[0]["owner"]["is_active"] == True
    assert response.json()[0]["owner"]["role"] == "admin" 
    
    
    
# create test function to test one todo
def test_read_one_authenticated(test_todo, test_user):

    response = client.get('/v1/todos/1')
    
    assert response.status_code == 200
    assert response.json()["title"] == "Learn to code in C#" 
    assert response.json()["description"] == "Need to learn everyday!" 
    assert response.json()["priority"] == 5
    assert response.json()["complete"] == False 
    assert response.json()["owner_id"] == 1
    assert response.json()["owner"]["email"] ==  "test_user@gmail.com"
    assert response.json()["owner"]["user_name"] == "test user"
    assert response.json()["owner"]["is_active"] == True
    assert response.json()["owner"]["role"] == "admin" 
        
# When not fount the todo 
def test_read_one_authenticated_not_found():
    response = client.get('/v1/todos/11233')

    assert response.status_code == 404
    assert response.json() == {'detail':"The element with id:11233 is not found."}

# Test to create a todo 
def test_create_todo(test_todo, test_user):

    todo_data = {
        'title' : 'Learn to code',
        'description' : 'Need to learn everyday!',
        'priority' : 5,
        'complete' : False,
    }

    # request 
    response = client.post('/v1/todos/create_todo', json=todo_data)

    # Test state
    assert response.status_code == 201
    # test if the todo was created 
    db = TestSessionLocal()

    query = db.query(Todo).filter(Todo.id == 2).first()

    # Test
    assert query.title == todo_data.get('title')
    assert query.description == todo_data.get('description')
    assert query.priority == todo_data.get('priority')
    assert query.complete == todo_data.get('complete')

# Test put or update
def test_update_todo(test_todo):

    payload = {
        'title' : 'Learn to design pattern',
        'description' : 'Need to learn everyday!',
        'priority' : 5,
        'complete' : False,
    }

    # test endpoint 
    respose = client.put('/v1/todos/update_todo/1', json=payload)

    # status code
    assert respose.status_code == status.HTTP_204_NO_CONTENT

    # test if the todo was updated
    test_db = TestSessionLocal()

    query = test_db.query(Todo).filter(Todo.id == 1).first()

    #test 
    assert query.title == payload.get('title')

# test todo id not faund  
def test_update_todo_not_found(test_todo):

    payload = {
        'title' : 'Learn to design pattern',
        'description' : 'Need to learn everyday!',
        'priority' : 5,
        'complete' : False,
    }

    # test endpoint 
    response = client.put('/v1/todos/update_todo/1238', json=payload)

    assert response.status_code == 404
    assert response.json() == {'detail':'The element with id:1238 is not found.'}


def test_delete_todo(test_todo):

    # Test endpoint 
    response = client.delete('/v1/todos/delete_todo/1')

    # test 
    assert response.status_code == 204

    # test if was delete of the todo was susseful 
    test_db = TestSessionLocal()

    query = test_db.query(Todo).filter(Todo.id == 1).first()

    assert query is None