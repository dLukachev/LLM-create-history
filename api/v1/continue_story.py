import json
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from api.deps import get_db
from database.models import Story
from database.schema import StoryContinueRequest
from func.continue_story import continue_story_task
from utils.redis import redis_client

continue_story_router = APIRouter()

@continue_story_router.post("/continue-story")
async def continue_story(request: StoryContinueRequest, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.session_id == request.session_id).first()
    if not story:
        raise HTTPException(404, "Story not found")

    result = await continue_story_task(session_id=request.session_id, prompt=request.promt, changes=request.changes, db=db)

    return result