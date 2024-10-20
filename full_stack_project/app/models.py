from .database import BASE
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


# Create User model
class User(BASE):
    __tablename__ = 'users'

    # Create db columns 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique = True, nullable=False)
    user_name = Column(String, unique =True, nullable=False)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    create_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

# Create model to Todos

class Todo(BASE):

     __tablename__ = 'todos'

     id = Column(Integer, primary_key=True, index=True)
     # other attributes
     title = Column(String, nullable=False)
     description = Column(String, nullable=False)
     priority = Column(Integer, nullable=False)
     complete = Column(Boolean, default= False, nullable=False)
     create_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=True)

     # Foreing key 
     owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

     owner = relationship('User')