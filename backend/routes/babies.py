from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..oauth2 import get_current_user
from .. import models, schemas
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/babies'
)


@router.get('/', response_model=List[schemas.Baby])
def get_babies(db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):

    babies = db.query(models.Baby)\
        .filter(models.Baby.user_id == user.id)\
        .all()

    if not babies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No babies found for user {user.id}")

    return babies


@router.post('/', response_model=schemas.Baby, status_code=status.HTTP_201_CREATED)
def post_babies(baby: schemas.BabyCreate, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):

    new_baby = baby.dict()
    new_baby.update({"user_id": user.id})

    baby_model = models.Baby(**new_baby)

    db.add(baby_model)
    db.commit()
    db.refresh(baby_model)

    first_sleep_session = models.SleepSession(
        baby_id = baby_model.id,
    )
    first_feed_session = models.FeedSession(
        baby_id = baby_model.id
    )
    db.add(first_sleep_session)
    db.add(first_feed_session)
    db.commit()
    db.refresh(first_sleep_session)
    db.refresh(first_feed_session)
    first_sleep_session.set_sleep_length()
    first_feed_session.set_feed_length()
    db.commit()
    return baby_model


@router.delete('/{baby_id}', status_code=status.HTTP_200_OK)
def delete_baby(baby_id, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):

    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby_id, models.Baby.user_id == user.id)).first()

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby {baby_id} not found for user {user.id}")

    db.delete(baby)
    db.commit()

    return {"message": f"Baby {baby_id} successfully deleted"}


@router.get('/{baby_id}')
def get_baby(baby_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby_id, models.Baby.user_id == user.id)).first()
