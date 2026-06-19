from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import secrets

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    goal = Column(Text, nullable=False)
    domain = Column(String, nullable=True, index=True)  # AI-detected domain
    duration_weeks = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    public_id = Column(String, unique=True, index=True, nullable=True)

    # Relationships
    user = relationship("User", back_populates="roadmaps")
    week_plans = relationship("WeekPlan", back_populates="roadmap", cascade="all, delete-orphan")
    
    def generate_public_id(self):
        """Generate a unique public ID for sharing"""
        if not self.public_id:
            self.public_id = secrets.token_urlsafe(16)
