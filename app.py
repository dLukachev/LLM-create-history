from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.start_story import start_story

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(start_story)