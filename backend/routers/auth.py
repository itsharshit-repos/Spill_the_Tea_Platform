from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models
import utils

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    # check if user exist? If not, raise 403 forbidden error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials."
        )
    is_password_correct = utils.verify_password(user_credentials.password, user.password)
    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials."
        )
    # if credentials match, pass the identifier payload dictionary to the token machine
    access_token = utils.create_access_token(data={"user_id": user.id})
    # return exactly the token payload dictionary configuration requested
    return {"access_token": access_token, "token_type": "bearer"}