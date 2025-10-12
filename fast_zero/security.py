from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select

from fast_zero.database import SessionDep
from fast_zero.models import User

SECRET_KEY = 'your_secret_key_here'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):
    crendentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, detail='could not validate credentials', headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        subject_email = payload.get('sub')
        if not subject_email:
            raise crendentials_exception
    except DecodeError:
        raise crendentials_exception

    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise crendentials_exception

    return user
