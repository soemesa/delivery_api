
from datetime import timedelta, datetime, timezone

from jose import jwt
from passlib.context import CryptContext

from src.settings import Settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

settings = Settings()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

