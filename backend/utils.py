import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "spill_the_tea_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Takes a raw password and returns the bcrypt hash."""
    # convert string to bytes
    pwd_bytes = password.encode('utf-8')
    # generate a random salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    # converting the resulting bytes back to string for the database
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares the raw password against a hash to see if they match."""
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    # bcrypt check if they match safely
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password_byte_enc)

def create_access_token(data: dict):
    """Creates a mathematically signed JWT containing user data."""
    to_encode = data.copy()
    # Set the token to expire in 30 minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Generate the JWT string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt