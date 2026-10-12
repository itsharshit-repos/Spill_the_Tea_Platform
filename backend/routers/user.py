from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
import utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # checking if user already exist or not
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken."
        )
    # takes the raw password and convert it to secure hash
    secure_hash = utils.hash_password(user.password)
    # creating new user
    new_user = models.User(
        username = user.username,
        password = secure_hash
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user