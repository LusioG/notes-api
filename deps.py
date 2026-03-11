from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from database import get_db
from models import User
from sqlalchemy.orm import Session
from security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



def get_current_user(
  token: str = Depends(oauth2_scheme),
  db: Session = Depends(get_db)      
):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(401,"Token inválido")

    #EL campo "sub" dentro del token guarda la ID del usuario 
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)

    if not user:
        raise HTTPException(401, "Usuario no existe")
    return user
