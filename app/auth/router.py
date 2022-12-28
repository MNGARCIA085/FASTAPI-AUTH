from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas,dependencies,security
from sqlalchemy.orm import Session
from databases.config import get_db
from .users import router as users_routes
from constants import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/auth",
    responses={404: {"description": "Not found"}},
)

router.include_router(users_routes.router,tags=['users'])

# AUTH


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = security.authenticate_user(form_data.username, form_data.password,db )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




# ejemplos de uso de las dependencias
@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: schemas.User = Depends(dependencies.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
