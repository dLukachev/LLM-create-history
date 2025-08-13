from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
import json

from utils.celery import app_celery
from utils.redis import redis_client
from database.models import Story
from func.openrouter_service import OpenRouterService

service = OpenRouterService()

@app_celery.task
async def continue_story_task(session_id: UUID, prompt: str, changes: str, db: Session):

    cache = await redis_client.get(f"session:{session_id}")
    if cache:
        print('_____________Кеш нашел!_____________')
        decode_cache = json.loads(cache)
    else:
        story = db.query(Story).filter(Story.session_id == session_id).first()
        if story:
            story.text = response # type: ignore
            story.create_at = datetime.now() # type: ignore
            db.commit()
        else:
            return {"Error 404": "Story not found"}
    
    response = await service.call(prompt=prompt, changes=changes, old_data=decode_cache, session_id=session_id) # type: ignore
    return response