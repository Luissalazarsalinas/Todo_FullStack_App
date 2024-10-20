from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

# Create url connection to postgresql
PROSTGRESQL_URL = (
    "postgresql://"
    f"{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_dbname}"
)

# Create connection engine
engine = create_engine(url= PROSTGRESQL_URL)

# Validate if the db exist or not 
if not database_exists(engine.url):
    create_database(engine.url)

# cREATE A LOCAL SESSION INSTANCE
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base to create models
BASE = declarative_base()

# open session, send transaction and close connection
def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
