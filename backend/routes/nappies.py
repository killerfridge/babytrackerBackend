from ..oauth2 import get_current_user
from ..utils import get_baby
from ..database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from ..models import NappyChanges, Nappy
from ..schemas import User, NappyBase
import datetime

router = APIRouter(
    prefix='/nappies',
)


@router.get("/{baby_id}")
def get_nappies(baby_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    baby = get_baby(baby_id, user, db)

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Baby {id} for {user.email} not found')

    nappies = db.query(NappyChanges).filter(NappyChanges.baby_id == baby_id).all()

    if not nappies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No nappy changes for {baby.name}')

    return nappies


@router.get('/{baby_id}/latest')
def get_latest(baby_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    baby = get_baby(baby_id, user, db)
    today = datetime.datetime.now() - datetime.timedelta(hours=24)

    if not baby:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Baby {id} for {user.email} not found')

    wet = db.query(NappyChanges.created_at) \
        .filter(and_(
            or_(NappyChanges.nappy_type == Nappy.wee, NappyChanges.nappy_type == Nappy.wee_poo),
            NappyChanges.baby_id == baby_id
        )) \
        .order_by(NappyChanges.created_at.desc()) \
        .first()

    if not wet:
        wet = {'created_at': None}

    solid = db.query(NappyChanges.created_at) \
        .filter(and_(
            or_(NappyChanges.nappy_type == Nappy.poo, NappyChanges.nappy_type == Nappy.wee_poo),
            NappyChanges.baby_id == baby_id
        )) \
        .order_by(NappyChanges.created_at.desc()) \
        .first()

    if not solid:
        solid = {'created_at': None}

    wet_today = db.query(func.count(NappyChanges.baby_id).label('wet_count')) \
        .filter(and_(
            or_(NappyChanges.nappy_type == Nappy.wee, NappyChanges.nappy_type == Nappy.wee_poo),
            NappyChanges.created_at > today
        )).group_by(NappyChanges.baby_id).first()

    solid_today = db.query(func.count(NappyChanges.baby_id).label('solid_count')) \
        .filter(and_(
            or_(NappyChanges.nappy_type == Nappy.poo, NappyChanges.nappy_type == Nappy.wee_poo),
            NappyChanges.created_at > today
    )).group_by(NappyChanges.baby_id).first()

    if not wet_today:
        wet_today = {'wet_count': 0}

    if not solid_today:
        solid_today = {'solid_count': 0}

    return {'wet': wet, 'solid': solid, 'wet_today': wet_today, 'solid_today': solid_today}


@router.post('/{baby_id}', status_code=status.HTTP_201_CREATED)
def post(nappy: NappyBase, baby_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_nappy = NappyChanges(
        baby_id=baby_id,
        nappy_type=nappy.nappy_type
    )

    db.add(new_nappy)
    db.commit()
    db.refresh(new_nappy)
    return new_nappy
