from pydantic import BaseModel
from typing import List, Dict, Any

class GenerateRoadmapRequest(BaseModel):
    goal: str
    answers: Dict[str, Any]
    duration_weeks: int

class WeekPlanData(BaseModel):
    week: int
    focus: str
    topics: List[str]
    practice_tasks: List[str]
    target_problems: int

class GeneratedRoadmap(BaseModel):
    title: str
    duration_weeks: int
    weeks: List[WeekPlanData]

class GenerateRoadmapResponse(BaseModel):
    roadmap_id: int
    title: str
    goal: str
    duration_weeks: int
    weeks: List[WeekPlanData]
