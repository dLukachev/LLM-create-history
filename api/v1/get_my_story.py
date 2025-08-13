from fastapi import APIRouter, Depends, Response, Request
from uuid import uuid4
from sqlalchemy.orm import Session
from database.schema import UserStory
from database.models import Story

from api.deps import get_db

from utils.create_and_check_token import check_token, create_bearer_token, set_token_cookie

get_my_story = APIRouter()

@get_my_story.get("/my")
async def create_story(response: Response, request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get('access_token')

    if token:
        user = check_token(token.lstrip("Bearer").strip(), db)
    else:
        token = create_bearer_token(str(uuid4().hex))
        set_token_cookie(response, token)

    token = token.lstrip("Bearer").strip()

    result = db.query(Story).filter_by(user_id=token).all()

    return result