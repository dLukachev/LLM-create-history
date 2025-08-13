from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session, sessionmaker
import json

from utils.redis import redis_client
from utils.arq import REDIS_SETTINGS
from database.models import Story
from database.base import engine
from func.openrouter_service import OpenRouterService

service = OpenRouterService()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def continue_story_task(ctx, session_id: UUID, prompt: str, changes: str):
    db = SessionLocal()

    cache = await redis_client.get(f"session:{session_id}")
    if cache:
        print('_____________Кеш нашел!_____________')
        old_data = json.loads(cache)
    else:
        print('_____________Дату в дб нашел!_____________')
        story = db.query(Story).filter(Story.session_id == session_id).first()
        if story:
            old_data = f"Текст запроса: {story.text}, промпт: {story.promt}"
        else:
            return {"Error 404": "Story not found"}
    
    response = await service.call(prompt=prompt, changes=changes, old_data=old_data, session_id=session_id) # type: ignore

    try:
        # Обновление истории в БД
        story = db.query(Story).filter(Story.session_id == session_id).first()
        if not story:
            story_obj = Story(session_id=session_id, text=response, promt=prompt, created_at=datetime.now())
            db.add(story_obj)
        else:
            db.query(Story).filter(Story.session_id == session_id).update({"text": str(response)})
        db.commit()
        await redis_client.set(f"session:{session_id}", json.dumps(response).encode('utf-8'), ex=3600)  # Кэш на 1 час
    except Exception as e:
        db.rollback()
        raise Exception(f"Database error: {str(e)}")
    finally:
        db.close()

    return response


class WorkerSettings:
    functions = [continue_story_task]
    redis_settings = REDIS_SETTINGS