from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    database_username:str
    database_password:str
    database_host:str
    database_port:str
    database_dbname:str
    secret_key:str
    algorithm:str
    access_token_expire:int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Create a instance 
settings = Settings()
