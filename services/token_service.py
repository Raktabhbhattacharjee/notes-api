import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict) -> str:
    """
    Generate a signed JWT token.
    - Copies the data dict to avoid mutating the original
    - Adds expiry time (exp) to the payload
    - Signs it with SECRET_KEY using HS256
    """
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT token.
    - Verifies the signature using SECRET_KEY
    - Raises JWTError if token is invalid or expired
    - Returns the payload dict if valid
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])