from . import schemas,models
from sqlalchemy.orm import Session


# get an user (returns a dict)
def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return schemas.UserInDB(**user.__dict__)
    else:
        return False









