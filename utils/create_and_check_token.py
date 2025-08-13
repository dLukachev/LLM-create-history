import os
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from database.models import Story

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_bearer_token(user_id: str):
    # Бессрочный токен с user_id
    payload = {"sub": str(user_id)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return token


def set_token_cookie(response: Response, token: str):
    # Устанавливаем токен в cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,  # Защита от XSS
        samesite="strict",  # Защита от CSRF
        max_age=None  # Бессрочный
    )


def check_token(token: str, db: Session):
    try:
        user = db.query(Story).filter_by(user_id=token).all()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")