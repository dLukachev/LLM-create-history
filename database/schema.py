from pydantic import BaseModel
from datetime import datetime


class GetStory(BaseModel):
    id: int
    text: dict
    create_at: datetime

class DevStory(GetStory):
    promt: str
    parameters: str
    session_id: str


class StoryCreateRequest(BaseModel):
    promt: str
    role: str


class StoryContinueRequest(BaseModel):
    session_id: str
    promt: str
    changes: str