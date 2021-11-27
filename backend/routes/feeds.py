from fastapi import Depends, status, HTTPException, APIRouter


router = APIRouter(
    prefix="/feeds"
)


@router.get("/")
def feeds_get():
    return {"message": "Feeds Get"}
