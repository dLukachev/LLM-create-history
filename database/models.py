from .base import Base
from sqlalchemy import Column, String, Integer, DateTime


class Story(Base):
    __tablename__ = "story"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    parameters = Column(String, nullable=True)
    create_at = Column(DateTime, nullable=False)