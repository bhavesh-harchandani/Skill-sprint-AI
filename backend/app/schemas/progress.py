from pydantic import BaseModel

class WeekCompleteResponse(BaseModel):
    week_id: int
    completed: bool

class WeekStatusResponse(BaseModel):
    week_id: int
    completed: bool

class RoadmapProgressResponse(BaseModel):
    roadmap_id: int
    completed_weeks: int
    total_weeks: int
    progress_percent: float
