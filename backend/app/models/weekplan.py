from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base

class WeekPlan(Base):
    __tablename__ = "weekplans"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    focus_title = Column(String, nullable=False)
    topics_json = Column(JSON, nullable=False)
    tasks_json = Column(JSON, nullable=False)
    target_problems = Column(Integer, nullable=False, default=0)

    # Relationships
    roadmap = relationship("Roadmap", back_populates="week_plans")
    progress = relationship("Progress", back_populates="week_plan", cascade="all, delete-orphan")
