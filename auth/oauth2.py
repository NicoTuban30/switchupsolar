from datetime import datetime, timedelta
from typing import Optional

from decouple import config
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from routes import user_route

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # print(username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_route.get_user_by_username(db, username)

    if user is None:
        raise credentials_exception

    return user