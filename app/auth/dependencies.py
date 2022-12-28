from typing import List
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from . import schemas,crud
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from databases.config import get_db
from config import settings
from constants import ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") #http://127.0.0.1:8000/auth/token


async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
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