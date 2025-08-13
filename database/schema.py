from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class GetStory(BaseModel):
    id: int
    text: str
    create_at: datetime

class DevStory(GetStory):
    promt: str
    parameters: str
    session_id: UUID


class StoryCreateRequest(BaseModel):
    promt: str
    role: str


class StoryContinueRequest(BaseModel):
    session_id: UUID
    promt: str
    changes: str