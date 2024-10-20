from app.models import BASE
from app.models import Todo, User
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, text
from app.utils.crypt import hash, verify
from app.main import app
import pytest


# Create a url to test db
URL_TEST_DB = 'sqlite:///./test.db'

# Create engine 
test_engine = create_engine(
    url = URL_TEST_DB,
    connect_args = {"check_same_thread": False},
    poolclass=StaticPool,
)

# Create session db
TestSessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=test_engine
)

# Mock tables from production db
BASE.metadata.create_all(bind=test_engine)

# OVERRRIDE db - Mock
def override_get_db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()

# Override user
def override_current_user():
    return User(
        id = 1,
        email = 'test_user@gmail.com',
        user_name = 'test user',
        first_name = 'user',
        second_name = 'test',
        password = '12345',
        is_active = True,
        role = 'admin',
        phone_number = '(111)-111-1111',
    )

# put the api in client mode
client = TestClient(app)

# Create a todo into the database
@pytest.fixture
def test_todo():

    # Create todo instance
    todo = Todo(
        title = 'Learn to code in C#',
        description = 'Need to learn everyday!',
        priority = 5,
        complete = False,
        owner_id = 1,
    )

    # add todo to the database
    db = TestSessionLocal()

    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo
    # Delete all todos into the test database
    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# Create a test user
@pytest.fixture
def test_user():

    # Create todo instance
    user = User(
        email = 'test_user@gmail.com',
        user_name = 'test user',
        first_name = 'user',
        second_name = 'test',
        password = hash('12345'),
        is_active = True,
        role = 'admin',
        phone_number = '(111)-111-1111',
    )


    # add todo to the database
    db = TestSessionLocal()

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user
    # Delete all todos into the test database
    with test_engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()



