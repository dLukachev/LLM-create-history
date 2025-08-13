import os
from dotenv import load_dotenv
import jwt
from fastapi import Response

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_bearer_token(user_id: int):
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