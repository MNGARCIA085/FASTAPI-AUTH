from fastapi import Depends, APIRouter
from .. import schemas
from . import crud
from sqlalchemy.orm import Session
from databases.config import get_db


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


# add an user
# create a new group
@router.post("/register",status_code=201)
def create_user(user:schemas.UserLogin,db: Session = Depends(get_db)):
    return crud.post_user(user,db)



# ver los usuarios
@router.get("/users")
def get_users(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(get_db)):
    return crud.get_users(skip,limit,db)