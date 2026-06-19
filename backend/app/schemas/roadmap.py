from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WeekPlanBase(BaseModel):
    week_number: int
    focus_title: str
    topics_json: List[str]
    tasks_json: List[str]
    target_problems: int

class WeekPlanCreate(WeekPlanBase):
    roadmap_id: int

class WeekPlanResponse(WeekPlanBase):
    id: int
    roadmap_id: int

    class Config:
        from_attributes = True

class RoadmapCreate(BaseModel):
    goal: str
    duration_weeks: int

class RoadmapSummary(BaseModel):
    id: int
    goal: str
    duration_weeks: int
    created_at: datetime
    progress_percent: float = 0.0

    class Config:
        from_attributes = True

class RoadmapResponse(BaseModel):
    id: int
    goal: str
    duration_weeks: int
    created_at: datetime
    public_id: Optional[str] = None
    week_plans: List[WeekPlanResponse] = []

    class Config:
        from_attributes = True

class ShareResponse(BaseModel):
    roadmap_id: int
    public_id: str
    share_url: str
