from .. import schemas, models
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..oauth2 import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from ..utils import get_baby

router = APIRouter(
    prefix='/temperatures',
    tags=['Temperature Logs']
)


@router.get('/{baby_id}', response_model=schemas.TempResponse)
def get_temps(baby_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):

    baby = get_baby(baby_id, db=db, user=user)

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby {baby_id} not found for {user.email}")

    avg_temp = db.query(func.avg(models.Temperature.value).label("avg_temperature"))\
        .filter(models.Temperature.baby_id == baby_id)\
        .group_by(models.Temperature.baby_id)\
        .label("avg")

    temp = db.query(models.Temperature, avg_temp)\
        .filter(models.Temperature.baby_id == baby_id)\
        .order_by(models.Temperature.created_at.desc())\
        .first()

    return temp


@router.post('/{baby_id}')
def post_temps(baby_id: int, temp: schemas.TempValue, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):

    baby = get_baby(baby_id, db=db, user=user)

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Baby {baby_id} not found for {user.email}")

    new_temp = models.Temperature(
        baby_id=baby_id,
        value=temp.value
    )

    db.add(new_temp)
    db.commit()
    db.refresh(new_temp)

    avg_temp = db.query(func.avg(models.Temperature.value).label("avg_temperature")) \
        .filter(models.Temperature.baby_id == baby_id) \
        .group_by(models.Temperature.baby_id) \
        .label("avg")

    temp = db.query(models.Temperature, avg_temp) \
        .filter(models.Temperature.baby_id == baby_id) \
        .order_by(models.Temperature.created_at.desc()) \
        .first()

    return temp


