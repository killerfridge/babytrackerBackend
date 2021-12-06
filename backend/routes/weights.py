from .. import database, schemas, models, oauth2, utils
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import plotly.express as px
import plotly as plt
import numpy as np
import pandas as pd


router = APIRouter(prefix='/weights',
                   tags=['Weight Management'])


@router.get('/{baby_id}')
def get_weight(baby_id: int, user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):

    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby_id, models.Baby.user_id == user.id))

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND(f"Baby {baby_id} not found for {user.email}"))

    # avg_weight = db.query(func.avg(models.Weight.value).label('avg_weight'))\
    #     .filter(models.Weight.baby_id == baby_id)\
    #     .group_by(models.Weight.baby_id).label('avg')

    weights = db.query(models.Weight)\
        .filter(models.Weight.baby_id == baby_id)\
        .order_by(models.Weight.created_at.desc())\
        .first()

    return weights


@router.get('/{baby_id}/plot', response_model=List[schemas.WeightPlot])
def weight_plot(baby_id: int, user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):
    baby = utils.get_baby(baby_id, user=user, db=db)
    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND(f"Baby {baby_id} not found for {user.email}"))

    weights = db.query(models.Weight) \
        .filter(models.Weight.baby_id == baby_id) \
        .order_by(models.Weight.created_at.desc()) \
        .all()

    if not weights:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    weight_values = [w.value for w in weights]
    dates = [w.created_at for w in weights]

    return weights


@router.post('/{baby_id}')
def post_weight(baby_id: int, weight: schemas.WeightValue, user: schemas.User = Depends(oauth2.get_current_user), db: Session = Depends(database.get_db)):

    print(weight.value)

    baby = db.query(models.Baby).filter(and_(models.Baby.id == baby_id, models.Baby.user_id == user.id))

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND(f"Baby {baby_id} not found for {user.email}"))

    new_weight = models.Weight(
        value=weight.value,
        baby_id=baby_id
    )

    db.add(new_weight)
    db.commit()
    db.refresh(new_weight)

    return new_weight


