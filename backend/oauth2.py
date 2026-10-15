from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
from config import settings

# This tell FastAPI where the client should go to get the token. 
# Because our router has no prefix and the route is "/login", we just use "login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decode the token using exact same secret key and algorithm
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        # extract the user_id we embedded during login
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
    except jwt.PyJWTError:
        # If the token is expired, this catched the error
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    # return the user
    return user