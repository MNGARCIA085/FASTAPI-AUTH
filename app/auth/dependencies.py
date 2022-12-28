from typing import List
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from . import schemas,crud
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from databases.config import get_db


# to get a string like this run:
# openssl rand -hex 32
# luego serán vars. de entorno
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") #http://127.0.0.1:8000/auth/token


async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username=token_data.username)  
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


#
class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: schemas.User = Depends(get_current_active_user)):
        if user.rol not in self.allowed_roles:
            #logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")