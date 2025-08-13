from fastapi import APIRouter, Depends
from uuid import uuid4
from sqlalchemy.orm import Session

from api.deps import get_db

from func.generate_story import generate_story_task
from database.schema import StoryCreateRequest

start_story = APIRouter()

@start_story.post("/create_story")
async def create_story(request: StoryCreateRequest, db: Session = Depends(get_db)):
    promt = request.promt
    role = request.role

    if promt == "" or role == "":
        return {"data": "Failed. Promt or role missing."}
    
    session_id = uuid4()

    result = await generate_story_task(session_id=session_id, prompt=promt, role=role, db=db)

    return {"data":result, "uuid":session_id}
