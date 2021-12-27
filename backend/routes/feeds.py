from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .. import models, database, schemas, utils
from datetime import timedelta, datetime, timezone
from ..oauth2 import get_current_user
from typing import List


router = APIRouter(
    prefix="/feeds"
)


@router.get("/")
def feeds_get():
    return {"message": "Feeds Get"}


@router.get('/{baby}', response_model=schemas.Feed)
def get_latest_feed(baby: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby, models.Baby.user_id == user.id)).first()

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby for user {user.email} not found.")

    feed_session = db.query(models.FeedSession) \
        .filter(models.FeedSession.baby_id == baby.id) \
        .order_by(models.FeedSession.feed_start.desc()) \
        .first()

    if feed_session:
        return feed_session
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No feeds logged for this baby")


@router.get('/{baby_id}/plot', response_model=List[schemas.Feed])
def get_plots(baby_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(get_current_user)):
    baby = utils.get_baby(baby_id, user, db)

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Baby for user {user.email} not found.')

    feeds = db.query(models.FeedSession) \
        .filter(models.FeedSession.baby_id == baby_id) \
        .order_by(models.FeedSession.feed_start.asc()) \
        .all()

    response = []
    for feed in feeds:
        if feed.feed_start.day != feed.feed_end.day:
            print(f"Hello there {feed.id}")
            new_end = datetime(
                feed.feed_start.year,
                feed.feed_start.month,
                feed.feed_start.day,
                0, 0, tzinfo=timezone.utc) + timedelta(days=1)
            new_length = new_end - feed.feed_start
            response.append(
                schemas.Feed(
                    id = feed.id,
                    feed_start = feed.feed_start,
                    feed_end = new_end,
                    feed_length = new_length
                )
            )

            response.append(
                schemas.Feed(
                    id = feed.id,
                    feed_start = new_end,
                    feed_end = feed.feed_end,
                    feed_length = feed.feed_end - new_end
                )
            )
        else:
            response.append(schemas.Feed(
                id = feed.id,
                feed_start = feed.feed_start,
                feed_end = feed.feed_end,
                feed_length = feed.feed_length
            ))
    print(response)

    if not feeds:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Sleep Sessions")

    return response


@router.post("/{baby}", response_model=schemas.Feed)
def feeds_post(baby: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_user)):
    # filter to get the correct baby
    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby, models.Baby.user_id == user.id)).first()

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby for user {user.email} not found.")
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
        return feed_session
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
        db.refresh(feed_session)
        return feed_session
