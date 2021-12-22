from ..schemas import User, UserCreate
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from typing import List


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    users = db.query(models.User)

    emails = users.where(models.User.email == user.email.lower()).first()

    if emails:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email {user.email} already in use. Do you wish to reset password?")

    new_user = models.User(
        email=user.email.lower()
    )
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users


@router.get('/{id}', response_model=User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found')

    return user


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} was not found')

    db.delete(user)

    db.commit()

    return {"message": f"User {id} successfully deleted"}


# @router.post('/login')
# def validate_user(user: UserValidate, db: Session = Depends(get_db)):
#     """Validates the user by checking the password against the hashed password in the database"""
#     user_val = db.query(models.User).filter(models.User.username == user.username).first()
#
#     if not user_val:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect")
#
#     if user_val.check_password(user.password):
#         return {"msg": "User successfully validated"}
#     else:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect")
