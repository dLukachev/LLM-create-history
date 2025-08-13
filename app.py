from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.v1.start_story import start_story
from api.v1.continue_story import continue_story_router
from api.v1.get_story_by_id import get_story
from api.v1.get_my_story import get_my_story

from database.base import Base, engine

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(start_story)
app.include_router(continue_story_router)
app.include_router(get_story)
app.include_router(get_my_story)