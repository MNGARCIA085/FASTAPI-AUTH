from fastapi import Depends
from .. import schemas,models
from sqlalchemy.orm import Session
from databases.config import get_db
from ..security import get_password_hash


def post_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    hash_password = get_password_hash(user.password)
    db_item = models.User(email=user.email,
                            hashed_password=hash_password,
                            rol="std",
                            username=user.username)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# return all groups
def get_users(
            skip: int = 0, 
            limit: int = 100, 
            db: Session = Depends(get_db)):   
    return db.query(models.User).offset(skip).limit(limit).all()