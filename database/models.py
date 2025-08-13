from .base import Base
from sqlalchemy import Column, String, Integer, DateTime, UUID
from datetime import datetime


class Story(Base):
    __tablename__ = "story"
    id = Column(Integer, primary_key=True)
    promt = Column(String, nullable=False)
    text = Column(String, nullable=False)
    parameters = Column(String, nullable=True)
    create_at = Column(DateTime, nullable=False, default=datetime.now())
    session_id = Column(UUID, nullable=False)
    user_id = Column(String, nullable=False)