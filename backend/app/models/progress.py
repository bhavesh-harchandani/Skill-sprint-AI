from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    weekplan_id = Column(Integer, ForeignKey("weekplans.id"), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    # Relationships
    week_plan = relationship("WeekPlan", back_populates="progress")
