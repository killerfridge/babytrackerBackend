from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Logs in the user and returns a JWT token"""
    user = db.query(models.User).filter(models.User.email == user_credentials.username.lower()).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if not user.verify_password(user_credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    # create token
    token = oauth2.create_access_token(data={"user_id": user.id})
    # return token
    return {"access_token": token, "token_type": "bearer"}


@router.get('/login', status_code=status.HTTP_200_OK)
def authenticated(user: schemas.User = Depends(oauth2.get_current_user)):
    return {"detail": "authenticated"}
