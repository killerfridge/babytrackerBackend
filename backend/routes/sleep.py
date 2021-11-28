from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

# This needs to be changed to allow multiple babies
# Currently assuming only one child
BABY_CONSTANT = 1


router = APIRouter(
    prefix="/sleep"
)


@router.get("/")
def sleep_get():
    return {"message": "Sleeps!"}


@router.post("/", status_code=status.HTTP_200_OK)
def sleep_post(db: Session = Depends(get_db)):
    # get the baby
    baby_query = db.query(models.Baby).filter(models.Baby.id == BABY_CONSTANT)
    baby = baby_query.first()
    # if the baby is awake
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
        return {"message": "Baby is now asleep!"}
    else:
        # get the most recent sleep session
        sleep_session = db.query(models.SleepSession)\
            .filter(models.SleepSession.baby_id==BABY_CONSTANT)\
            .order_by(models.SleepSession.sleep_start.desc())\
            .first()
        # set the timestamp for baby waking
        sleep_session.set_sleep_length()
        # set a timestamp in the second baby sleep model
        sleep = models.Sleep(
            baby_id=BABY_CONSTANT,
            is_awake=True,
            sleep_id=1
        )
        # set the baby to awake
        baby.is_awake = True
        db.add(sleep)
        db.commit()
        return {"message": "Baby is now awake!"}

