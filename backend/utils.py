from passlib.context import CryptContext
from .database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .oauth2 import get_current_user
from . import models, schemas

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_baby(baby_id: int, user: schemas.User, db: Session):

    return db.query(models.Baby).filter(and_(models.Baby.id == baby_id, models.Baby.user_id == user.id)).first()
