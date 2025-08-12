from pydantic import BaseModel
from datetime import datetime


class GetStory(BaseModel):
    id: int
    text: str
    parameters: str | None = None
    create_at: datetime


class StoryCreateRequest(BaseModel):
    promt: str
    role: str