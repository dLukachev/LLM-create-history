from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from api.deps import get_db
from database.models import Story
from database.schema import SessionId, GetStory

get_story = APIRouter()

@get_story.post("/get-story", response_model=GetStory)
async def get_story_by_id(request: SessionId, db: Session = Depends(get_db)):
    if not request.session_id:
        raise HTTPException(status_code=400, detail="Session ID is required.")

    result = db.query(Story).filter_by(session_id=request.session_id).one_or_none()

    # Если запись не найдена, возвращаем 404
    if result is None:
        raise HTTPException(status_code=404, detail="Story not found.")

    return result