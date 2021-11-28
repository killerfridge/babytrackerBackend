from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models, database
from .sleep import BABY_CONSTANT


router = APIRouter(
    prefix="/feeds"
)


@router.get("/")
def feeds_get():
    return {"message": "Feeds Get"}


@router.post("/")
def feeds_post(db: Session = Depends(database.get_db)):
    # filter to get the correct baby
    # TODO: replace BABY_CONSTANT with a changeable id
    # TODO: add filtering based on user
    baby = db.query(models.Baby).filter(models.Baby.id == BABY_CONSTANT).first()
    # Check if the baby is feeding
    if not baby.is_feeding:
        # create a new feeding session
        feed_session = models.FeedSession(
            baby_id=baby.id
        )
        # set the is_feeding tag to true
        baby.is_feeding = True
        # add the feed session to the database
        db.add(feed_session)
        # create a feed instance - may be deprecated
        feed = models.Feed(
            baby_id=baby.id,
            is_start=True,
            feed_id=1
        )
        # add instance to the database
        db.add(feed)
        db.commit()
        # TODO: either return nothing or something meaningful
        return {'message': 'baby is feeding'}
    else:
        # get the last feeding session
        feed_session = db.query(models.FeedSession)\
            .filter(models.FeedSession.baby_id == baby.id)\
            .order_by(models.FeedSession.feed_start.desc())\
            .first()
        # create a new feed instance - to be deprecated
        feed = models.Feed(
            baby_id = baby.id,
            is_start = False,
            feed_id = 1
        )
        # set the feed ending point
        feed_session.set_feed_length()
        # set the is_feeding tag to False
        baby.is_feeding = False
        # add to the database
        db.add(feed)

        db.commit()
        # TODO: return a meaningful response
        return {"message": "baby is now not feeding"}
