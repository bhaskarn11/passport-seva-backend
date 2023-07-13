from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from settings import get_settings
from dependencies import get_db
from models import User
from jwt import PyJWTError as JWTError
import jwt
from passlib.hash import pbkdf2_sha256


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

config = get_settings()

ALGORITHM = "HS256"


def get_user(username: str, db: Session):
    user = db.query(User).where(User.email == username).first()
    return user


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username, db)
    if not user:
        return False
    if not pbkdf2_sha256.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expire_time_minutes: int = 15):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expire_time_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token():
    pass


def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = get_user(username, db)
    if user is None:
        raise credentials_exception
    return user
