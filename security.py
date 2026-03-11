from passlib.context import CryptContext

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#CryptContext configura el algoritmo de hash
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#Transforma la contraseña a codigo hash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


#Los Token habilitan al usuario a usar endpoints protegidos

#El JWT se inserta en el encabezado de las peticiones que realizamos del front para validar identidad
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

    