from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..database import get_db
from .. import models, schemas, oauth2, utils
from typing import List
import datetime


router = APIRouter(
    prefix="/sleep"
)


@router.get("/")
def sleep_get():
    return {"message": "Sleeps!"}


@router.get('/{baby_id}', response_model=schemas.Sleep)
def get_latest_feed(baby_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):

    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby_id, models.Baby.user_id == user.id)).first()

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby for user {user.email} not found.")

    sleep_session = db.query(models.SleepSession) \
        .filter(models.SleepSession.baby_id == baby.id) \
        .order_by(models.SleepSession.sleep_start.desc()) \
        .first()

    if sleep_session:
        return sleep_session
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sleeps logged for this baby")


@router.get('/{baby_id}/plot', response_model=List[schemas.Sleep])
def get_plot(baby_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):

    baby = utils.get_baby(baby_id, user, db)

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby {baby_id} not found for {user.email}.")

    sleeps = db.query(models.SleepSession)\
        .filter(and_(models.SleepSession.baby_id == baby_id, models.SleepSession.sleep_length > datetime.timedelta(0)))\
        .order_by(models.SleepSession.sleep_start.asc())\
        .all()

    if not sleeps:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Sleep Sessions")

    return sleeps


@router.post("/{baby_id}", status_code=status.HTTP_200_OK, response_model=schemas.Sleep)
def sleep_post(baby_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    # get the baby
    baby_query = db.query(models.Baby).filter(
        and_(models.Baby.user_id == user.id, models.Baby.id == baby_id)
    )
    baby = baby_query.first()
    # if the baby is awake
    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby {baby_id} for {user.email} not found")
    if baby.is_awake:
        # create a new sleep session
        sleep_session = models.SleepSession(
            baby_id=baby.id
        )
        # log the sleep in the sleep model
        sleep = models.Sleep(
            baby_id=baby.id,
            is_awake=False,
            sleep_id=1
        )
        # set the baby to asleep
        baby.is_awake = False
        # commit everything
        db.add(sleep_session)
        db.add(sleep)
        db.commit()
        db.refresh(sleep_session)
        return sleep_session
    else:
        # get the most recent sleep session
        sleep_session = db.query(models.SleepSession)\
            .filter(models.SleepSession.baby_id == baby_id)\
            .order_by(models.SleepSession.sleep_start.desc())\
            .first()
        # set the timestamp for baby waking
        sleep_session.set_sleep_length()
        # set a timestamp in the second baby sleep model
        sleep = models.Sleep(
            baby_id=baby_id,
            is_awake=True,
            sleep_id=1
        )
        # set the baby to awake
        baby.is_awake = True
        db.add(sleep)
        db.commit()
        db.refresh(sleep_session)
        return sleep_session

