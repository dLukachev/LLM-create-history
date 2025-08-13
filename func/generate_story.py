from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session

from utils.celery import app_celery
from utils.redis import redis_client
from database.models import Story
from func.openrouter_service import OpenRouterService

@app_celery.task
async def generate_story_task(session_id: UUID, prompt: str, role: str, db: Session):
    service = OpenRouterService()
    response = await service.call(prompt, role=role, session_id=session_id)
    try:
        story = db.query(Story).filter(Story.session_id == session_id).first()
        if story:
            story.text = response # type: ignore
            story.create_at = datetime.now() # type: ignore
            db.commit()
        else:
            user_story = Story(
                session_id=session_id,
                promt=prompt,
                text=response,
                parameters=role
            )
            db.add(user_story)
            db.commit()
            db.refresh(user_story)
        await redis_client.delete(f"history:{session_id}")
        await redis_client.close()
    finally:
        db.close()
    return response