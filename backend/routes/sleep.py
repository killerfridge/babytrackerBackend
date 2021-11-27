from fastapi import Depends, status, HTTPException, APIRouter


router = APIRouter(
    prefix="/sleep"
)


@router.get("/")
def sleep_get():
    return {"message": "Sleeps!"}
