from fastapi import status
from app.database import get_db
from app.oauth2 import current_user
from app.models import User
from app.main import app
from .utils import *



# Mock user and database connection
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[current_user] = override_current_user

# Test all endpoints

# Get all user
def test_get_all_user(test_user):

    # get response
    response = client.get('/v1/users/get_users')


    # Test
    assert response.status_code == 200
    assert response.json()[0]['email'] == 'test_user@gmail.com'
    assert response.json()[0]['user_name'] == 'test user'
    # assert response.json()[0]['first_name'] == 'user'
    # assert response.json()[0]['second_name'] == 'test'
    assert response.json()[0]['is_active'] == True
    assert response.json()[0]['role'] == 'admin'
    # assert response.json()[0]['phone_number'] == '(111)-111-1111'

def test_get_one_user(test_user):

    # response 
    response = client.get('/v1/users/get_user/1')

    # Test
    assert response.status_code == 200
    assert response.json()['email'] == 'test_user@gmail.com'
    assert response.json()['user_name'] == 'test user'
    # assert response.json()['first_name'] == 'user'
    # assert response.json()['second_name'] == 'test'
    assert response.json()['is_active'] == True
    assert response.json()['role'] == 'admin'
    # assert response.json()['phone_number'] == '(111)-111-1111'


def test_get_one_user_not_found(test_user):

    # response
    response = client.get('/v1/users/get_user/13424')

    assert response.status_code == 404
    assert response.json() == {'detail':'User with id:13424, Not found.'}

def test_create_user(test_user):

    # data payload
    payload = {
        'email':'lfdev@email.com',
        'user_name' : 'lfdev',
        'first_name' : 'Luis',
        'second_name' : 'Salazar',
        'password' : hash('123'),
        'is_active' :True,
        'role' : 'admin',
        'phone_number' : '(111)-111-1111'
    }

    # response
    response = client.post('/v1/users/create_user', json=payload)

    assert response.status_code == 201

    # test db
    db = TestSessionLocal()

    query = db.query(User).filter(User.id == 2).first()

    # test
    assert query.email == payload.get('email')
    assert query.user_name == payload.get('user_name')
    # assert query.first_name == payload.get('first_name')
    # assert query.second_name == payload.get('second_name ')
    # assert query.password == payload.get('password ')
    assert query.is_active == payload.get('is_active')
    assert query.role == payload.get('role')
    # assert query.phone_number == payload.get('phone_number')

# Test to update password
def test_change_password(test_user):
    
    # body
    payload = {
        'password':'12345',
        'new_password':'123'
    }
    # response
    response = client.patch('/v1/users/update_password', json=payload)

    assert response.status_code == 204

def test_change_phone(test_user):

    # body
    payload = {
        'phone_number':'(111)-111-1111',
        'new_phone_num':'(222)-222-2222'
    }
    # response 
    response = client.patch('/v1/users/update_phone_number', json=payload)

    assert response.status_code == 204