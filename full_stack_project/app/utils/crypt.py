from passlib.context import CryptContext

# Create instance 
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

# hash password
def hash(password:str) -> str:
    return bcrypt_context.hash(password)

# validate plaint password
def verify(plain_password:str, hash_password:str) -> bool:
    return bcrypt_context.verify(plain_password, hash_password)