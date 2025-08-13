from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session, sessionmaker
from database.base import engine

from utils.arq import REDIS_SETTINGS, get_redis_pool
from database.models import Story
from func.openrouter_service import OpenRouterService

service = OpenRouterService()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def generate_story_task(ctx, session_id: UUID, prompt: str, role: str, user_id: str | None = None):
    db = SessionLocal()
    try:
        response = await service.call(prompt, role=role, session_id=session_id)
        story = db.query(Story).filter(Story.session_id == session_id).first()
        if story:
            story.text = response # type: ignore
            story.create_at = datetime.now() # type: ignore
            db.commit()
        if user_id == None:
            user_story = Story(
                session_id=session_id,
                promt=prompt,
                text=response,
                parameters=role
            )
        else:
            user_story = Story(
                session_id=session_id,
                promt=prompt,
                text=response,
                parameters=role,
                user_id=user_id
            )
        db.add(user_story)
        db.commit()
        db.refresh(user_story)
    except Exception as e:
        db.rollback()
        raise Exception(f"Ошибка базы данных: {str(e)}")
    finally:
        db.close()
    return response


class WorkerSettings:
    functions = [generate_story_task]
    redis_settings = REDIS_SETTINGS