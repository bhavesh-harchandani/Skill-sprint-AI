from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class PracticeItem(Base):
    __tablename__ = "practice_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    domain = Column(String, nullable=False, index=True)  # DSA, React, DevOps, ML, etc.
    topic = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False)  # easy, medium, hard
    link = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(JSONB, nullable=True, default=[])  # Additional metadata
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PracticeItem {self.domain}/{self.title} ({self.difficulty})>"
