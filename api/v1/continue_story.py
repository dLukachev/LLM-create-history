from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from api.deps import get_db
from database.models import Story
from database.schema import DevStory, StoryContinueRequest
from uuid import UUID

continue_story_router = APIRouter()

@continue_story_router.post("/continue-story", response_model=DevStory)
async def continue_story(request: StoryContinueRequest, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.session_id == request.session_id).first()
    if not story:
        raise HTTPException(404, "Story not found")
    return story